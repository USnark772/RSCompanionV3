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
from time import time, sleep as tsleep
from asyncio import futures, Event, get_event_loop, sleep
from Devices.Camera.Model import cam_defs as defs
from Model.app_helpers import await_event


class StreamReader:
    def __init__(self, index: int = 0, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self.index = index
        self._running = False
        self._closing_flag = Event()
        self._timeout_limit = 0
        self._stream = VideoCapture(index, defs.cap_backend)
        self.set_resolution(self.get_resolution())
        self._fps_test_status = 0
        self._fps_limit = float("inf")
        self._frame_rate_limiter = 1/self._fps_limit
        self._use_limiter = False
        self._new_frame_event = Event()
        self._err_event = Event()
        self._internal_frame_q = SimpleQueue()
        self._loop = get_event_loop()
        self._read_loop_task = None
        self._logger.debug("Initialized")

    def cleanup(self) -> None:
        """
        Cleanup this object and prep for app closure.
        :return None:
        """
        self._closing_flag.set()
        self.stop()
        self._stream.release()

    def _calc_timeout(self) -> None:
        """
        Get small sample of reads and pick longest read time for timeout.
        :return None:
        """
        tries = list()
        for i in range(10):
            start = time()
            self._stream.read()  # Prime camera for reading.
            end = time()
            tries.append(end - start)
        self._timeout_limit = max(tries) + 1.5  # + 1.5 to handle possible lag spikes.

    def start(self) -> None:
        """
        Reset internal frame queue so we have no leftover frames and run read_cam in thread.
        :return None:
        """
        self._running = True
        self._internal_frame_q = SimpleQueue()
        self._read_loop_task = self._loop.run_in_executor(None, self._read_cam)

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
        self._running = False
        if self._read_loop_task is not None:
            self._read_loop_task.cancel()
            self._read_loop_task = None

    def _read_cam(self) -> None:
        """
        Continuously check camera for new frames and put into queue. Raise error event if camera fails.
        :return None:
        """
        self._calc_timeout()
        prev = time()
        while self._running:
            if self._use_limiter:
                elapsed = time() - prev
                if elapsed >= self._frame_rate_limiter:
                    prev = time()
                    if not self._get_a_frame(prev):
                        break
                else:
                    self._stream.grab()
                    tsleep(.0001)
            else:
                if not self._get_a_frame(time()):
                    break

    def _get_a_frame(self, prev: time) -> bool:
        """
        Helper function for self._read_cam.
        :param prev: The current time()
        :return bool: If frame was read successfully.
        """
        ret, frame = self._stream.read()
        end = time()
        dt = datetime.now()
        time_taken = end - prev
        timeout = time_taken > self._timeout_limit
        if not ret or frame is None or timeout:
            self._logger.warning("cam_stream_reader.py _read_cam(): Camera failed. "
                                 + "ret: " + str(ret)
                                 + ". Frame is None: " + str(frame is None)
                                 + ". Time taken: " + str(time_taken))
            self._loop.call_soon_threadsafe(self._err_event.set)
            return False
        self._internal_frame_q.put((frame, dt))
        self._loop.call_soon_threadsafe(self._new_frame_event.set)
        return True

    def get_fps(self) -> float:
        """
        Return the current fps limit for this camera.
        :return int: The current fps limit.
        """
        return self._fps_limit

    def set_fps(self, new_fps: float) -> None:
        """
        Set read speed of this camera as fps
        :param new_fps: The new rate to read at.
        :return None:
        """
        if new_fps == float("inf"):
            self._use_limiter = False
        else:
            self._use_limiter = True
        self._fps_limit = new_fps
        self._frame_rate_limiter = 1 / self._fps_limit - .001

    def get_next_new_frame(self) -> (bool, (ndarray, datetime)):
        """
        Get next frame from queue if it exists and return it, else return None.
        :return (bool, (ndarray, datetime)): (Whether there is a frame, (frame/None, datetime/None))
        """
        self._logger.debug("running")
        if not self._internal_frame_q.empty():
            self._logger.debug("done with next element")
            return True, self._internal_frame_q.get()
        self._logger.debug("done with None")
        return False, (None, None)

    def test_resolution(self, size: (float, float)) -> (bool, (float, float)):
        """
        Test given frame size to see if camera supports it.
        :param size: The size to test.
        :return (bool, (float, float)): Whether test succeeded and what the resultant resolution is.
        """
        ret1 = self._stream.set(CAP_PROP_FRAME_WIDTH, size[0])
        ret2 = self._stream.set(CAP_PROP_FRAME_HEIGHT, size[1])
        ret, frame = self._stream.read()
        y, x = frame.shape[0], frame.shape[1]
        if ret1 and ret2 and size[0] == x and size[1] == y:
            return True, size
        else:
            return False, (self._stream.get(CAP_PROP_FRAME_WIDTH), self._stream.get(CAP_PROP_FRAME_HEIGHT))

    def get_resolution(self) -> (float, float):
        """
        :return (float, float): The current camera frame size.
        """
        return self._stream.get(CAP_PROP_FRAME_WIDTH), self._stream.get(CAP_PROP_FRAME_HEIGHT)

    def set_resolution(self, size: (float, float)) -> None:
        """
        Handle changing frame size on this camera.
        :param size: The new frame size to use.
        :return None:
        """
        was_running = self._running
        if was_running:
            self.stop()
        self._internal_frame_q = SimpleQueue()
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
        self._stream.set(CAP_PROP_FRAME_WIDTH, size[0])
        self._stream.set(CAP_PROP_FRAME_HEIGHT, size[1])

    def _set_fourcc(self) -> None:
        """
        Reset fourcc on this camera. Generally done after changing frame size.
        :return None:
        """
        self._stream.set(CAP_PROP_FOURCC, defs.cap_temp_codec)
        self._stream.set(CAP_PROP_FOURCC, defs.cap_codec)

    def get_fps_status(self) -> int:
        """
        :return int: The current percentage of testing done.
        """
        return self._fps_test_status

    async def calc_max_fps(self, res_to_test: (float, float), num_reads: int = 180) -> int:
        """
        Calculate this camera's actual max fps.
        :return int: The max supported fps.
        """
        self._logger.debug("running")
        self._fps_test_status = 0
        cur_res = self.get_resolution()
        self.set_resolution(res_to_test)
        self._stream.read()
        divisor = num_reads / 100
        s = time()
        for i in range(num_reads):
            if self._closing_flag.is_set():
                return 0
            self._stream.read()
            self._fps_test_status = int(i / divisor)
            await sleep(0)
        e = time()
        self.set_resolution(cur_res)
        time_taken = e - s
        if time_taken > 0:
            ret = round(num_reads / time_taken)
            self.set_fps(ret)
        else:
            ret = -1
        self._logger.debug("done with: " + str(ret))
        return ret
