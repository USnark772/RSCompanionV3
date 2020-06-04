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
from cv2 import putText, FONT_HERSHEY_COMPLEX as FONT_FACE, LINE_AA as LINE_TYPE
from queue import SimpleQueue
from Model.app_helpers import format_current_time
from Devices.Camera.Model import cam_defs as defs
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_stream_writer import StreamWriter
from Devices.Camera.Model.cam_size_getter import SizeGetter


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
                          defs.ModelEnum.SET_FPS: self._cam_reader.set_fps}
        self._running = True
        self._writing = False
        self._show_feed = False
        self._pipe_handler_task = None
        self._frame_handler_task = None
        self._frame_size = self._cam_reader.get_current_frame_size()
        self._using_cam = Event()
        self._loop = get_event_loop()

        self._sizes = list()
        self._fps = 30
        self._fps_status = 0
        self._cam_name = "CAM_" + str(self._cam_index)
        self._name_time_loc = (30, 50)
        self._fps_loc = (30, 80)
        self._font_scale = .6
        self._font_thickness = 1
        r = 211
        g = 250
        b = 10
        self._color = (b, g, r)
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
                    if msg[1] is not None:
                        self._switcher[msg[0]](msg[1])
                    else:
                        self._switcher[msg[0]]()
                await sleep(.01)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

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

    async def _run_tests(self) -> None:
        """
        Run each camera test in order.
        :return None:
        """
        create_task(self._monitor_init_progress())
        sizes = await self.size_gtr.get_sizes()
        max_fps = await self._get_fps()
        self._msg_pipe.send((defs.ModelEnum.START, (max_fps, sizes)))

    async def _get_fps(self) -> int:
        """
        Get this camera's base fps.
        :return None:
        """
        num_frames = 0
        time_to_take = 30
        self._cam_reader.stream.read()
        s = time.time()
        elapsed = time.time() - s
        while elapsed < time_to_take:
            self._cam_reader.stream.read()
            num_frames += 1
            elapsed = time.time() - s
            self._fps_status = int(elapsed / 10 * 100)
            await sleep(0)
        ret = round(num_frames / time_to_take)
        return ret

    async def _monitor_init_progress(self) -> None:
        """
        Periodically update controller on init progress.
        :return None:
        """
        while True:
            status = (self._fps_status / 2) + (self.size_gtr.status / 2)
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
        await create_task(self._stop())
        self._cam_reader.cleanup()
        self._cam_writer.cleanup(discard)
        self._msg_pipe.send((defs.ModelEnum.CLEANUP, None))

    def _use_cam(self, is_active: bool) -> None:
        """
        Toggle whether this cam is being used.
        :param is_active: Whether this cam is being used.
        :return None:
        """
        if is_active:
            self._cam_reader.start()
            self._using_cam.set()
        else:
            self._cam_reader.stop()
            self._using_cam.clear()

    def _use_feed(self, is_active: bool) -> None:
        """
        Toggle whether this cam feed is being used.
        :param is_active: Whether thsi cam feed is being used.
        :return None:
        """
        self._show_feed = is_active

    def _start_writing(self, path: str) -> None:
        """
        Create new writer and set boolean to start putting frames in write queue.
        :return None:
        """
        filename = path + "CAM_" + str(self._cam_index) + "_" + format_current_time(datetime.now(), save=True) + ".avi"
        self._frame_size = self._cam_reader.get_current_frame_size()
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
        # TODO: Consider putting these in threads like in cam_controller?
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

    async def _handle_new_frame(self) -> None:
        """
        Handle frames from camera
        :return None:
        """
        times = list()
        num_to_keep = 60
        prev_time = time.time()
        while self._running:
            await self._using_cam.wait()
            await self._cam_reader.await_new_frame()
            (frame, timestamp) = self._cam_reader.get_next_new_frame()
            now = time.mktime(timestamp.timetuple()) + timestamp.microsecond / 1E6
            times.append(now - prev_time)
            while len(times) > num_to_keep:
                times = times[1:]
            prev_time = now
            self._fps = round(num_to_keep / sum(times))
            fps = "FPS: " + str(self._fps)
            str_time = format_current_time(timestamp, True, True, True)
            time_and_name = str_time + " " + self._cam_name
            putText(frame, time_and_name, self._name_time_loc, FONT_FACE, self._font_scale, self._color,
                    self._font_thickness, LINE_TYPE)
            putText(frame, fps, self._fps_loc, FONT_FACE, self._font_scale, self._color, self._font_thickness, LINE_TYPE)
            if self._writing:
                self._write_q.put(frame)
            if self._show_feed:
                self._img_pipe.send(frame)
