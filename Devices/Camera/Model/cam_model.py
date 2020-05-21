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

from logging import getLogger, StreamHandler
from datetime import datetime
from asyncio import create_task, Event, sleep, set_event_loop, new_event_loop, get_event_loop
from multiprocessing.connection import Connection
from cv2 import COLOR_BGR2RGB, cvtColor
from numpy import ndarray
from queue import SimpleQueue
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt
from Model.app_helpers import await_event, end_tasks, format_current_time
from Devices.Camera.Model import cam_defs as defs
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_stream_writer import StreamWriter


class CamModel:
    def __init__(self, msg_pipe: Connection, img_pipe: Connection, cam_index: int = 0):
        set_event_loop(new_event_loop())
        self._msg_pipe = msg_pipe
        self._img_pipe = img_pipe
        self._cam_reader = StreamReader(cam_index)
        self._stop_event = Event()
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter(self._write_q)
        self._awaitable_tasks = []
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
        self._using_cam = Event()
        self._using_cam.set()
        self._loop = get_event_loop()
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
                await sleep(.1)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

    def cleanup(self) -> None:
        """
        Cleanup this code and prep for app closure.
        :return None:
        """
        self._running = False
        self._stop_event.set()
        self._cam_reader.cleanup()
        self._cam_writer.cleanup()

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
        filename = path + "CAM_" + format_current_time(datetime.now(), save=True) + ".avi"
        fps = 30  # TODO: Make this dynamic
        size = self._cam_reader.get_current_frame_size()
        size = (int(size[0]), int(size[1]))
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter(self._write_q)
        self._cam_writer.start(filename, fps, size)
        self._writing = True

    def _stop_writing(self) -> None:
        """
        Destroy writer and set boolean to stop putting frames in write queue.
        :return None:
        """
        self._cam_writer.cleanup()
        self._writing = False

    async def _start_loop(self) -> None:
        """
        Run all async tasks in this model and wait for stop signal. (This method is the main loop for this process)
        :return None:
        """
        create_task(self._handle_pipe())
        create_task(self._handle_new_frame())
        await self._stop_event.wait()

    async def _handle_new_frame(self) -> None:
        """
        Handle frames from camera
        :return None:
        """
        while self._running:
            await self._using_cam.wait()
            await self._cam_reader.await_new_frame()
            frame = self._cam_reader.get_next_new_frame()
            if self._writing:
                self._write_q.put(frame)
            if self._show_feed:
                self._img_pipe.send(self.convert_frame_to_qt_image(frame))

    @staticmethod
    def convert_frame_to_qt_image(frame: ndarray) -> QPixmap:
        """
        Convert image to suitable format for display in Qt.
        :param frame: The image to convert.
        :return QPixmap: The converted image.
        """
        print("in convert()")
        rgb_image = cvtColor(frame, COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        res = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888).scaled(248, 186, Qt.KeepAspectRatio)
        print("here 1")
        ret = QPixmap.fromImage(res)  # TODO: Figure out why this hangs.
        print("here 2")
        return ret
