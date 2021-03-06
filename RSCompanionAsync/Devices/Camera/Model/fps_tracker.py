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

from time import time, mktime
from threading import Lock
from collections import deque
from datetime import datetime


class FPSTracker:
    def __init__(self):
        self._lock = Lock()
        self._fps = 0
        self._times = deque()
        self._num_to_keep = 60
        self._sum_times = 0
        self._prev_time = time()

    def update_fps(self, timestamp: datetime = None, given_time: time = None):
        if timestamp is not None:
            now = mktime(timestamp.timetuple()) + timestamp.microsecond / 1E6
        elif given_time is not None:
            now = given_time
        else:
            now = time()
        self._lock.acquire()
        diff = now - self._prev_time
        self._times.append(diff)
        self._sum_times += diff
        while len(self._times) > self._num_to_keep:
            self._sum_times -= self._times.popleft()
        self._prev_time = now
        if self._sum_times > 0:
            self._fps = round(self._num_to_keep / self._sum_times)
        self._lock.release()

    def get_fps(self) -> int:
        self._lock.acquire()
        ret = self._fps
        self._lock.release()
        return ret

    def reset(self) -> None:
        self._lock.acquire()
        self._times = deque()
        self._prev_time = time()
        self._sum_times = 0
        self._fps = 0
        self._lock.release()
