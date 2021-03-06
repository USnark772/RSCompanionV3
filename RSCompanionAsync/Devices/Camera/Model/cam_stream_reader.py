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
from numpy import ndarray
from time import time, sleep as tsleep
from asyncio import futures, Event, get_event_loop, sleep as asyncsleep
from threading import Event as TEvent, Lock
from RSCompanionAsync.Devices.Camera.Model import cam_defs as defs
from RSCompanionAsync.Model.app_helpers import await_event
from RSCompanionAsync.Devices.Camera.Model.fps_tracker import FPSTracker


class InternalFrameQueue:
    def __init__(self):
        self._lock = Lock()
        self._q = list()

    def reset_q(self) -> None:
        with self._lock:
            self._q = list()

    def add_to_q(self, item) -> None:
        with self._lock:
            self._q.append(item)

    def get_from_q(self) -> object:
        ret = None
        with self._lock:
            if len(self._q) > 0:
                ret = self._q.pop(0)
        return ret


class StreamReader:
    def __init__(self, index: int = 0, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self.index = index
        self._tracker = FPSTracker()
        self._internal_frame_q = InternalFrameQueue()
        self._running = TEvent()
        self._running.clear()
        self._lock = Lock()
        self._closing_flag = Event()
        self._timeout_limit = 0
        self._stream = VideoCapture(index, defs.cap_backend)
        self.set_resolution(self.get_resolution())
        self._fps_test_status = 0
        self._fps_target = 30
        self._spf_target = 1 / self._fps_target
        self._buffer = 5
        self._use_limiter = False
        self._finalized = False
        self._end = TEvent()
        self._end.clear()
        self._err_event = Event()
        self._num_frms = 0
        self._start = time()
        self._loop = get_event_loop()
        self._logger.debug("Initialized")

    def cleanup(self) -> None:
        """
        Cleanup this object and prep for app closure.
        :return None:
        """
        self._closing_flag.set()
        self._end.set()
        self.stop_reading()
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

    def _finalize(self) -> None:
        self._calc_timeout()
        self._loop.run_in_executor(None, self._read_cam)
        self._finalized = True

    def start_reading(self) -> None:
        """
        Reset internal frame queue so we have no leftover frames and run read_cam in thread.
        :return None:
        """
        with self._lock:
            if not self._finalized:
                self._finalize()
            if not self._running.is_set():
                self._tracker.reset()
                self._internal_frame_q.reset_q()
                self._num_frms = 0
                self._start = time()
                self._running.set()

    def await_err(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._err_event)

    def stop_reading(self) -> None:
        """
        End any looping tasks.
        :return None:
        """
        with self._lock:
            self._running.clear()

    def _read_cam(self) -> None:
        """
        Continuously check camera for new frames and put into queue.
        :return None:
        """
        while not self._end.is_set():
            if self._running.is_set():
                ret, frame, dt = self._get_a_frame()
                if not ret:
                    break
                self._tracker.update_fps()
                metric = (time() - self._start) // self._spf_target
                frm_diff = int(metric - self._num_frms)
                if frm_diff > 0:
                    self._internal_frame_q.add_to_q((frame, dt, frm_diff))
                    self._num_frms += frm_diff
                elif frm_diff > -self._buffer:
                    self._internal_frame_q.add_to_q((frame, dt, 1))
                    self._num_frms += 1
            else:
                tsleep(.1)

    def _get_a_frame(self) -> (bool, ndarray, datetime):
        """
        Helper function for self._read_cam. Raise error event if camera fails.
        :return bool: If frame was read successfully.
        """
        s = time()
        ret, frame = self._stream.read()
        e = time()
        dt = datetime.now()
        time_taken = e - s
        timeout = time_taken > self._timeout_limit
        if not ret or frame is None or timeout:
            self._logger.warning("cam_stream_reader.py _read_cam(): Camera failed. "
                                 + "ret: " + str(ret)
                                 + ". Frame is None: " + str(frame is None)
                                 + ". Time taken: " + str(time_taken))
            self._loop.call_soon_threadsafe(self._err_event.set)
            return False, None, None
        return True, frame, dt

    def get_fps_setting(self) -> float:
        """
        Return the current fps limit for this camera.
        :return int: The current fps limit.
        """
        return self._fps_target

    def get_fps_actual(self) -> int:
        """
        Return the current fps this camera is reading at.
        :return int: The current fps.
        """
        return self._tracker.get_fps()

    def set_fps(self, new_fps: float) -> None:
        """
        Set simulated read speed of this camera. Reader will still read from camera at max rate.
        :param new_fps: The new simulated fps.
        :return None:
        """
        with self._lock:
            self._running.clear()
            tsleep(.05)
            self._fps_target = new_fps
            self._spf_target = 1 / self._fps_target
            self._buffer = new_fps // 6
            self._start = time()
            self._num_frms = 0
            self._running.set()

    def get_next_new_frame(self) -> (bool, (ndarray, datetime, int)):
        """
        Get next frame from queue if it exists and return it, else return None.
        :return (bool, (ndarray, datetime)): (Whether there is a frame, (frame/None, datetime/None))
        """
        self._logger.debug("running")
        ret = self._internal_frame_q.get_from_q()
        if ret is not None:
            self._logger.debug("done with next element")
            return True, ret
        self._logger.debug("done with None")
        return False, None

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
        with self._lock:
            self._internal_frame_q.reset_q()
            self._set_fourcc()
            self._set_resolution(size)

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

    async def calc_max_fps(self, res_to_test: (float, float), num_reads: int = 240) -> int:
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
            await asyncsleep(0)
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
