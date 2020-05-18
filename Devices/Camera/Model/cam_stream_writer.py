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

from cv2 import VideoWriter
from threading import Thread
from queue import Queue
from Devices.Camera.Model import cam_defs as defs


# TODO: Update this to use async
class StreamWriter:
    def __init__(self, frame_queue: Queue):
        self.writer: VideoWriter = VideoWriter()
        self.frame_queue = frame_queue
        self.running = True
        self.stopping = False
        self.t = Thread()

    def cleanup(self):
        self.stop()

    def start(self, filename: str, fps: int, size: (int, int)):
        self.writer = VideoWriter(filename, defs.cap_codec, fps, size)
        self.t = Thread(target=self.__update, args=())
        self.t.start()

    def stop(self):
        self.stopping = True
        if self.t.is_alive():
            self.t.join()
        self.stopping = False

    def __update(self):
        while self.running:
            if not self.frame_queue.empty():
                self.writer.write(self.frame_queue.get())
            if self.stopping:
                self.running = False
                while not self.frame_queue.empty():
                    self.writer.write(self.frame_queue.get())
