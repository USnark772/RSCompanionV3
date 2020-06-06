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
from cv2 import VideoCapture, CAP_PROP_FOURCC, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from queue import SimpleQueue
from numpy import ndarray
from time import time
from asyncio import futures, Event, get_event_loop
from Devices.Camera.Model import cam_defs as defs
from Model.app_helpers import await_event


class StreamReader:
    def __init__(self, index: int = 0, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self.running = False
        self.stream = VideoCapture(index, defs.cap_backend)
        self.set_resolution(self.get_resolution())
        start = time()
        a, b = self.stream.read()  # Prime camera for reading.
        end = time()
        self._fps_limit = 120
        self._frame_rate_limiter = 1/self._fps_limit
        self.timeout_limit = end - start + 1  # + 1 to handle random uncommon slight discrepancies.
        self._new_frame_event = Event()
        self._err_event = Event()
        self._tasks = list()
        self._internal_frame_q = SimpleQueue()
        self._loop = get_event_loop()

        self.index = index

        self._logger.debug("Initialized")

    def cleanup(self) -> None:
        """
        Cleanup this object and prep for app closure.
        :return None:
        """
        self.stop()
        self.stream.release()

    def start(self) -> None:
        """
        Reset internal frame queue so we have no leftover frames and run read_cam in thread.
        :return None:
        """
        self.running = True
        self._internal_frame_q = SimpleQueue()
        self._tasks.append(self._loop.run_in_executor(None, self._read_cam))

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

    def stop(self) -> None:
        """
        End any looping tasks.
        :return None:
        """
        self.running = False
        for task in self._tasks:
            task.cancel()

    def _read_cam(self) -> None:
        """
        Continuously check camera for new frames and put into queue. Raise error event if camera fails.
        :return None:
        """
        prev = time()
        while self.running:
            elapsed = time() - prev
            if elapsed > self._frame_rate_limiter:
                prev = time()
                start = prev
                ret, frame = self.stream.read()
                end = time()
                time_taken = end - start
                timeout = time_taken > self.timeout_limit
                # TODO: Make the timout bigger to handle computers that once in a while lag just a little too much?
                if not ret or frame is None or timeout:
                    self._logger.warning("cam_stream_reader.py _read_cam(): Camera failed. "
                                         + "ret: " + str(ret)
                                         + ". Frame is None: " + str(frame is None)
                                         + ". Time taken: " + str(time_taken))
                    self._loop.call_soon_threadsafe(self._err_event.set)
                    break
                self._internal_frame_q.put((frame, datetime.now()))
                self._loop.call_soon_threadsafe(self._new_frame_event.set)
            else:
                self.stream.grab()

    def get_fps(self) -> int:
        """
        Return the current fps limit for this camera.
        :return int: The current fps limit.
        """
        return self._fps_limit

    def set_fps(self, new_fps: int) -> None:
        """
        Set read speed of this camera as fps
        :param new_fps: The new rate to read at.
        :return None:
        """
        self._fps_limit = new_fps
        self._frame_rate_limiter = 1 / self._fps_limit

    def get_next_new_frame(self) -> ndarray:
        """
        Get next frame from queue if it exists and return it, else return None.
        :return ndarray or None:
        """
        self._logger.debug("running")
        if not self._internal_frame_q.empty():
            self._logger.debug("done with ndarray")
            return self._internal_frame_q.get()
        self._logger.debug("done with None")
        return None

    def test_resolution(self, size: (float, float)) -> (bool, (float, float)):
        """
        Test given frame size to see if camera supports it.
        :param size: The size to test.
        :return (bool, (float, float)): Whether test succeeded and what the resultant frame size is.
        """
        ret1 = self.stream.set(CAP_PROP_FRAME_WIDTH, size[0])
        ret2 = self.stream.set(CAP_PROP_FRAME_HEIGHT, size[1])
        if ret1 and ret2:
            return True, size
        else:
            return False, (self.stream.get(CAP_PROP_FRAME_WIDTH), self.stream.get(CAP_PROP_FRAME_HEIGHT))

    def get_resolution(self) -> (float, float):
        """
        :return (float, float): The current camera frame size.
        """
        return self.stream.get(CAP_PROP_FRAME_WIDTH), self.stream.get(CAP_PROP_FRAME_HEIGHT)

    def set_resolution(self, size: (float, float)) -> None:
        """
        Handle changing frame size on this camera.
        :param size: The new frame size to use.
        :return None:
        """
        was_running = self.running
        if was_running:
            self.stop()
        self._set_fourcc()
        self._set_resolution(size)
        if was_running:
            self.start()

    def _set_resolution(self, size: (float, float)) -> None:
        """
        Set camera frame size to new size.
        :param size: The new size to use.
        :return none:
        """
        self.stream.set(CAP_PROP_FRAME_WIDTH, size[0])
        self.stream.set(CAP_PROP_FRAME_HEIGHT, size[1])

    def _set_fourcc(self) -> None:
        """
        Reset fourcc on this camera. Generally done after changing frame size.
        :return None:
        """
        self.stream.set(CAP_PROP_FOURCC, defs.cap_temp_codec)
        self.stream.set(CAP_PROP_FOURCC, defs.cap_codec)
