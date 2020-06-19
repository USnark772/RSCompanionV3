""" 
Licensed under GNU GPL-3.0-or-later

This file is part of RS Companion.

RS Companion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RS Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RS Companion.  If not, see <https://www.gnu.org/licenses/>.

Author: Phillip Riskin
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

import time
from datetime import datetime
from asyncio import create_task, Event, sleep, set_event_loop, new_event_loop, get_event_loop
from multiprocessing.connection import Connection
from cv2 import putText, FONT_HERSHEY_COMPLEX as FONT_FACE, LINE_AA as LINE_TYPE, resize, INTER_AREA
from queue import SimpleQueue
from Model.app_helpers import format_current_time
from Devices.Camera.Model import cam_defs as defs
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_stream_writer import StreamWriter
from Devices.Camera.Model.cam_size_getter import SizeGetter
from Devices.Camera.Resources.cam_strings import LangEnum, strings, StringsEnum


class CamModel:
    def __init__(self, msg_pipe: Connection, img_pipe: Connection, cam_index: int = 0):
        set_event_loop(new_event_loop())
        self._msg_pipe = msg_pipe
        self._img_pipe = img_pipe
        self._cam_index = cam_index
        self._cam_reader = StreamReader(cam_index)
        self.size_gtr = SizeGetter(self._cam_reader)
        self._stop_event = Event()
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter()
        self._tasks = []
        self._switcher = {defs.ModelEnum.STOP: self._stop_writing,
                          defs.ModelEnum.START: self._start_writing,
                          defs.ModelEnum.SET_USE_CAM: self._use_cam,
                          defs.ModelEnum.SET_USE_FEED: self._use_feed,
                          defs.ModelEnum.CLEANUP: self.cleanup,
                          defs.ModelEnum.INITIALIZE: self.init_cam,
                          defs.ModelEnum.GET_FPS: self._get_fps,
                          defs.ModelEnum.SET_FPS: self._set_fps,
                          defs.ModelEnum.GET_RES: self._get_res,
                          defs.ModelEnum.SET_RES: self._set_res,
                          defs.ModelEnum.COND_NAME: self._update_cond_name,
                          defs.ModelEnum.BLOCK_NUM: self._update_block_num,
                          defs.ModelEnum.KEYFLAG: self._update_keyflag,
                          defs.ModelEnum.EXP_STATUS: self._update_exp_status,
                          defs.ModelEnum.LANGUAGE: self.set_lang,
                          }
        self._running = True
        self._writing = False
        self._show_feed = False
        self._pipe_handler_task = None
        self._frame_handler_task = None
        self._frame_size = self._cam_reader.get_resolution()
        self._handle_frames = Event()
        self._loop = get_event_loop()

        self._strings = strings[LangEnum.ENG]
        self._sizes = list()
        self._fps = 30
        self._cam_name = "CAM_" + str(self._cam_index)
        self._cond_name = str()
        self._exp_status = "Not running"
        self._block_num = 0
        self._keyflag = str()
        self._lines_to_write = []
        self._first_line_loc = (10, 20)
        self._font_scale = .6
        self._font_thickness = 1
        r = 211
        g = 250
        b = 10
        self._color = (b, g, r)
        self.set_lang()
        self._loop.run_until_complete(self._start_loop())

    async def _handle_pipe(self) -> None:
        """
        Handle msgs from model.
        :return None:
        """
        try:
            while self._running:
                if self._msg_pipe.poll():
                    msg = self._msg_pipe.recv()
                    if msg[0] in self._switcher.keys():
                        if msg[1] is not None:
                            self._switcher[msg[0]](msg[1])
                        else:
                            self._switcher[msg[0]]()
                await sleep(.01)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass
        except Exception as e:
            raise e

    def cleanup(self, discard: bool) -> None:
        """
        Cleanup this code and prep for app closure.
        :param discard: Quit without saving.
        :return None:
        """
        create_task(self._cleanup(discard))

    def init_cam(self) -> None:
        """
        Begin initializing camera.
        :return None:
        """
        create_task(self._run_tests())

    def set_lang(self, lang: LangEnum = LangEnum.ENG) -> None:
        """
        Set this camera's language.
        :param lang: The new language enum.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    async def _run_tests(self) -> None:
        """
        Run each camera test in order.
        :return None:
        """
        prog_tracker = create_task(self._monitor_init_progress())
        sizes = await self.size_gtr.get_sizes()
        if len(sizes) < 1:
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))
            prog_tracker.cancel()
            return
        max_fps = await self._cam_reader.calc_max_fps(max(sizes))
        if max_fps < 0:
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))
            prog_tracker.cancel()
            return
        self._msg_pipe.send((defs.ModelEnum.START, (max_fps, sizes)))
        prog_tracker.cancel()

    async def _monitor_init_progress(self) -> None:
        """
        Periodically update controller on init progress.
        :return None:
        """
        while True:
            status = (self._cam_reader.get_fps_status() / 2) + (self.size_gtr.status / 2)
            if status >= 100:
                break
            self._msg_pipe.send((defs.ModelEnum.STAT_UPD, status))
            await sleep(.5)

    async def _await_reader_err(self) -> None:
        """
        Handle if reader fails.
        :return None:
        """
        while self._running:
            await self._cam_reader.await_err()
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))

    async def _cleanup(self, discard: bool) -> None:
        self._running = False
        self.size_gtr.stop()
        await create_task(self._stop())
        self._cam_reader.cleanup()
        self._cam_writer.cleanup(discard)
        self._msg_pipe.send((defs.ModelEnum.CLEANUP, None))

    def _update_block_num(self, num: int) -> None:
        """
        Update the block num shown on camera details.
        :param num: The new num to show.
        :return None:
        """
        self._lines_to_write[4] = self._strings[StringsEnum.OVERLAY_BLOCK_NUM_LABEL] + " " + str(num)

    def _update_cond_name(self, name: str) -> None:
        """
        Update the condition name shown on camera details.
        :param name: The new name to show.
        :return None:
        """
        self._lines_to_write[0] = self._strings[StringsEnum.OVERLAY_COND_NAME_LABEL] + " " + str(name)

    def _update_keyflag(self, flag: str) -> None:
        """
        Update the key flag shown on camera details.
        :param flag: The new key flag to show.
        :return None:
        """
        self._lines_to_write[5] = self._strings[StringsEnum.OVERLAY_KEYFLAG_LABEL] + " " + str(flag)

    def _update_exp_status(self, status: bool) -> None:
        """
        Update the experiment status shown on the camera details.
        :param status: The new status to show.
        :return None:
        """
        output = str()
        if status:
            output = "Running"
        else:
            output = "Not running"
        self._lines_to_write[3] = self._strings[StringsEnum.OVERLAY_EXP_STATUS_LABEL] + " " + str(output)

    def _get_res(self) -> None:
        """
        Send the current resolution of this camera.
        :return None:
        """
        self._msg_pipe.send((defs.ModelEnum.CUR_RES, self._cam_reader.get_resolution()))

    def _set_res(self, new_res: (float, float)) -> None:
        """
        Change the resolution on this camera.
        :param new_res: The new resolution to use.
        :return None:
        """
        self._show_feed = False
        self._cam_reader.stop()
        self._cam_reader.set_resolution(new_res)
        self._times = list()
        time.sleep(1)
        self._cam_reader.start()
        self._show_feed = True

    def _use_cam(self, is_active: bool) -> None:
        """
        Toggle whether this cam is being used.
        :param is_active: Whether this cam is being used.
        :return None:
        """
        if is_active:
            self._cam_reader.start()
            self._handle_frames.set()
        else:
            self._cam_reader.stop()
            self._handle_frames.clear()

    def _use_feed(self, is_active: bool) -> None:
        """
        Toggle whether this cam feed is being passed to the view.
        :param is_active: Whether this cam feed is being passed to the view.
        :return None:
        """
        self._show_feed = is_active

    def _start_writing(self, path: str) -> None:
        """
        Create new writer and set boolean to start putting frames in write queue.
        :return None:
        """
        filename = path + "CAM_" + str(self._cam_index) + "_" + format_current_time(datetime.now(), save=True) + ".avi"
        self._frame_size = self._cam_reader.get_resolution()
        self._frame_size = (int(self._frame_size[0]), int(self._frame_size[1]))
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter()
        self._cam_writer.start(filename, int(self._fps), self._frame_size, self._write_q)
        self._writing = True

    def _stop_writing(self) -> None:
        """
        Destroy writer and set boolean to stop putting frames in write queue.
        :return None:
        """
        self._cam_writer.cleanup()
        self._writing = False

    async def signal_done_writing(self) -> None:
        """
        Signal when writer is done writing to file.
        :return None:
        """
        while self._running:
            await self._cam_writer.await_done_writing()
            self._msg_pipe.send((defs.ModelEnum.STOP, None))

    async def _start_loop(self) -> None:
        """
        Run all async tasks in this model and wait for stop signal. (This method is the main loop for this process)
        :return None:
        """
        # TODO: Consider putting these in threads like in cam_controller.
        self._tasks.append(create_task(self._handle_pipe()))
        self._tasks.append(create_task(self._handle_new_frame()))
        self._tasks.append(create_task(self._await_reader_err()))
        # self._tasks.append(create_task(self.signal_done_writing()))
        await self._stop_event.wait()

    async def _stop(self) -> None:
        """
        Stop all async tasks.
        :return None:
        """
        for task in self._tasks:
            task.cancel()
        self._stop_event.set()

    def _get_fps(self) -> None:
        """
        Send the current fps of this camera.
        :return None:
        """
        self._msg_pipe.send((defs.ModelEnum.CUR_FPS, self._cam_reader.get_fps()))

    def _set_fps(self, new_fps: float) -> None:
        """
        Set new fps and reset fps tracking.
        :param new_fps: The new fps to use.
        :return None:
        """
        self._times = list()
        self._cam_reader.set_fps(new_fps)

    async def _handle_new_frame(self) -> None:
        """
        Handle frames from camera
        :return None:
        """
        self._times = list()
        num_to_keep = 60
        prev_time = time.time()
        while self._running:
            await self._handle_frames.wait()
            await self._cam_reader.await_new_frame()
            ret, (frame, timestamp) = self._cam_reader.get_next_new_frame()
            if not ret:
                continue
            now = time.mktime(timestamp.timetuple()) + timestamp.microsecond / 1E6
            diff = now - prev_time
            self._times.append(diff)
            while len(self._times) > num_to_keep:
                self._times.pop(0)
            prev_time = now
            self._fps = round(len(self._times) / sum(self._times))
            self._lines_to_write[1] = format_current_time(timestamp, day=True, time=True, mil=True)
            self._lines_to_write[2] = self._strings[StringsEnum.OVERLAY_FPS_LABEL] + " " + str(self._fps)
            x, y = self._first_line_loc
            for line in self._lines_to_write:
                if len(line) > 0:
                    putText(frame, line, (x, y), FONT_FACE, self._font_scale, self._color, self._font_thickness,
                            LINE_TYPE)
                y += 30
            if self._writing:
                self._write_q.put(frame)
            if self._show_feed:
                to_send = self.image_resize(frame, width=640)
                self._img_pipe.send(to_send)

    # from https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    @staticmethod
    def image_resize(image, width=None, height=None, inter=INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def _set_texts(self) -> None:
        """
        Set the initial texts for this camera.
        :return None:
        """
        self._lines_to_write = [self._strings[StringsEnum.OVERLAY_COND_NAME_LABEL] + " " + self._cond_name,
                                "",
                                "",
                                self._strings[StringsEnum.OVERLAY_EXP_STATUS_LABEL] + " " + self._exp_status,
                                self._strings[StringsEnum.OVERLAY_BLOCK_NUM_LABEL] + " " + str(self._block_num),
                                self._strings[StringsEnum.OVERLAY_KEYFLAG_LABEL] + " " + self._keyflag,
                                ]
