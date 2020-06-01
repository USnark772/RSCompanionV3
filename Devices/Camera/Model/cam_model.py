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

from datetime import datetime
from asyncio import create_task, Event, sleep, set_event_loop, new_event_loop, get_event_loop
from multiprocessing.connection import Connection
from cv2 import putText, FONT_HERSHEY_COMPLEX as FONT_FACE, LINE_AA as LINE_TYPE
from queue import SimpleQueue
from Model.app_helpers import format_current_time
from Devices.Camera.Model import cam_defs as defs
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_stream_writer import StreamWriter


class CamModel:
    def __init__(self, msg_pipe: Connection, img_pipe: Connection, cam_index: int = 0, frame_skip: int = 1):
        set_event_loop(new_event_loop())
        self._msg_pipe = msg_pipe
        self._img_pipe = img_pipe
        self._cam_index = cam_index
        self._cam_reader = StreamReader(cam_index, frame_skip)
        self._stop_event = Event()
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter()
        self._tasks = []
        self._cancellable_tasks = []
        self._switcher = {defs.ModelEnum.STOP: self._stop_writing,
                          defs.ModelEnum.START: self._start_writing,
                          defs.ModelEnum.SET_USE_CAM: self._use_cam,
                          defs.ModelEnum.SET_USE_FEED: self._use_feed,
                          defs.ModelEnum.CLEANUP: self.cleanup}
        self._running = True
        self._writing = False
        self._show_feed = True
        self._pipe_handler_task = None
        self._frame_handler_task = None
        self._frame_size = self._cam_reader.get_current_frame_size()
        self._using_cam = Event()
        self._using_cam.set()
        self._loop = get_event_loop()

        self._cam_name = "CAM_" + str(self._cam_index)
        self._text_loc = (30, 50)
        self._font_scale = .8
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

    def cleanup(self) -> None:
        """
        Cleanup this code and prep for app closure.
        :return None:
        """
        create_task(self._cleanup())

    async def _await_reader_err(self) -> None:
        """
        Handle if reader fails.
        :return None:
        """
        while self._running:
            await self._cam_reader.await_err()
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))

    async def _cleanup(self) -> None:
        self._running = False
        await create_task(self._stop())
        self._cam_reader.cleanup()
        self._cam_writer.cleanup(False)
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
        fps = 30  # TODO: Make this not hardcoded.
        self._frame_size = self._cam_reader.get_current_frame_size()
        self._frame_size = (int(self._frame_size[0]), int(self._frame_size[1]))
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter()
        self._cam_writer.start(filename, fps, self._frame_size, self._write_q)
        self._writing = True

    def _stop_writing(self) -> None:
        """
        Destroy writer and set boolean to stop putting frames in write queue.
        :return None:
        """
        self._cam_writer.cleanup(True)
        self._writing = False

    async def _start_loop(self) -> None:
        """
        Run all async tasks in this model and wait for stop signal. (This method is the main loop for this process)
        :return None:
        """
        # TODO: Consider putting these in threads like in cam_controller?
        self._tasks.append(create_task(self._handle_pipe()))
        self._tasks.append(create_task(self._handle_new_frame()))
        self._tasks.append(create_task(self._await_reader_err()))
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
        while self._running:
            await self._using_cam.wait()
            await self._cam_reader.await_new_frame()
            (frame, timestamp) = self._cam_reader.get_next_new_frame()
            str_time = format_current_time(timestamp, True, True, True)
            image_text = str_time + " " + self._cam_name
            putText(frame, image_text, self._text_loc, FONT_FACE, self._font_scale, self._color, self._font_thickness,
                    LINE_TYPE)
            if self._writing:
                self._write_q.put(frame)
            if self._show_feed:
                self._img_pipe.send(frame)
