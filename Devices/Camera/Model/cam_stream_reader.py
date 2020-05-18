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
from cv2 import VideoCapture, CAP_PROP_FOURCC, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from queue import SimpleQueue
from time import time
from asyncio import futures, Event, create_task, get_running_loop, Queue, sleep
from Devices.Camera.Model import cam_defs as defs
from Model.app_helpers import await_event, end_tasks


# TODO: Update this to use async
class StreamReader:
    def __init__(self, index: int = 0, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self.running = False
        self.stream = VideoCapture(index, defs.cap_backend)
        ret, self.latest_frame = self.stream.read()
        self._new_frame_event = Event()
        self._err_event = Event()
        self._awaitable_tasks = []
        self._cancellable_tasks = []
        self._internal_frame_q = SimpleQueue()
        self._loop = get_running_loop()
        self._logger.debug("Initialized")

    def cleanup(self):
        self.stop()
        self.stream.release()

    def start(self):
        self.running = True
        self._awaitable_tasks.append(self._loop.run_in_executor(None, self._read_cam))
        self._awaitable_tasks.append(create_task(self._update()))

    def await_new_frame(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._new_frame_event)

    def await_err(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._err_event)

    async def _update(self):
        while self.running:
            if not self._internal_frame_q.empty():
                ret, frame = self._internal_frame_q.get()
                if not ret:
                    self._err_event.set()
                    self.running = False
                    break
                self.latest_frame = frame
                self._new_frame_event.set()
            else:
                await sleep(.0001)

    def stop(self):
        self.running = False
        for task in self._cancellable_tasks:
            task.cancel()
        create_task(end_tasks(self._awaitable_tasks))

    def _read_cam(self) -> None:
        while self.running:
            start = time()
            ret, frame = self.stream.read()
            end = time()
            time_taken = end - start
            if not ret or frame is None or time_taken > 0.2:
                self._internal_frame_q.put((False, None))
                break
            else:
                self._internal_frame_q.put((ret, frame))

    def get_latest_frame(self):
        return self.latest_frame

    def test_frame_size(self, size: (float, float)):
        ret1 = self.stream.set(CAP_PROP_FRAME_WIDTH, size[0])
        ret2 = self.stream.set(CAP_PROP_FRAME_HEIGHT, size[1])
        if ret1 and ret2:
            return True, size
        else:
            return False, (self.stream.get(CAP_PROP_FRAME_WIDTH), self.stream.get(CAP_PROP_FRAME_HEIGHT))

    def get_current_frame_size(self):
        return self.stream.get(CAP_PROP_FRAME_WIDTH), self.stream.get(CAP_PROP_FRAME_HEIGHT)

    def change_frame_size(self, size: (float, float)):
        was_running = self.running
        if was_running:
            self.stop()
        self._set_fourcc()
        self._set_size(size)
        if was_running:
            self.start()

    def _set_size(self, size: (float, float)):
        self.stream.set(CAP_PROP_FRAME_WIDTH, size[0])
        self.stream.set(CAP_PROP_FRAME_HEIGHT, size[1])

    def _set_fourcc(self):
        self.stream.set(CAP_PROP_FOURCC, defs.cap_temp_codec)
        self.stream.set(CAP_PROP_FOURCC, defs.cap_codec)
