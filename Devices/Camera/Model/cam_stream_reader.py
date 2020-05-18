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

from cv2 import VideoCapture, CAP_PROP_FOURCC, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from threading import Thread
from time import time
from Devices.Camera.Model import cam_defs as defs


# TODO: Update this to use async
class StreamReader:
    def __init__(self, index: int):
        self.running = False
        self.stream = VideoCapture(index, defs.cap_backend)
        ret, self.frame = self.stream.read()
        self.new_frame = True
        self.t: Thread = Thread()
        self.failure = False

    def cleanup(self):
        self.stop()
        self.stream.release()

    def start(self):
        self.running = True
        self.t = Thread(target=self._update, args=())
        self.t.start()

    def _update(self):
        while self.running:
            start = time()
            ret, self.frame = self.stream.read()
            end = time()
            time_taken = end - start
            if not ret or self.frame is None or time_taken > 0.2:
                self.running = False
                self.failure = True
                break
            self.new_frame = True

    def stop(self):
        self.running = False
        if self.t.is_alive():
            self.t.join()

    def get_latest_frame(self):
        ret = self.new_frame
        self.new_frame = False
        return ret, self.frame

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
