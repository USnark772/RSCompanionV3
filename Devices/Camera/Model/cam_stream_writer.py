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
from queue import SimpleQueue
from asyncio import sleep, get_event_loop, create_task, Event, futures
from threading import Event as TEvent
from time import sleep
from Devices.Camera.Model import cam_defs as defs
from Model.app_helpers import await_event


class StreamWriter:
    def __init__(self):
        self._writer: VideoWriter = VideoWriter()
        self._frame_queue = SimpleQueue()
        self._stopping_flag = TEvent()
        self._done_writing_flag = Event()
        self._writer_released = Event()
        self._tasks = list()
        self._stop_flag = TEvent()
        self._stop_flag.set()
        self._loop = get_event_loop()

    def cleanup(self, discard: bool = False) -> None:
        """
        Cleanup this object and prep for app closure.
        :param discard: Quit without saving.
        :return None:
        """
        self.stop(discard)

    def await_done_writing(self) -> futures:
        """
        Signal when there is a done writing frames event.
        :return futures: If the flag is set.
        """
        return await_event(self._writer_released, True)

    def start(self, filename: str, fps: int, size: (int, int), q: SimpleQueue) -> None:
        """
        Start this writer with given parameters.
        :param filename: The filename to write to.
        :param fps: The fps to save images with.
        :param size: The size to save images as.
        :param q: The queue to write from.
        :return None:
        """
        self._stop_flag.clear()
        self._frame_queue = q
        self._writer = VideoWriter(filename, defs.cap_codec, fps, size)
        self._tasks.append(self._loop.run_in_executor(None, self._update))

    def stop(self, discard: bool) -> None:
        """
        Stop this writer.
        :return None:
        """
        if not self._stop_flag.isSet():
            create_task(self._stop_writer(discard))

    async def _stop_writer(self, discard: bool) -> None:
        """
        Signal stop and wait for writer to finish writing any frames not yet written.
        :return None:
        """
        if not discard:
            self._stopping_flag.set()
            await self._done_writing_flag.wait()
            self._stopping_flag.clear()
        self._stop_flag.set()
        self._writer.release()
        self._writer_released.set()  # TODO: Figure out why this is not noticed by await_done_writing()
        await self._tasks[0]

    def _update(self) -> None:
        """
        Continuously check for frames to save and save them. Finish saving before exiting if stopping before all
        frames are saved.
        :return None:
        """
        while not self._stop_flag.isSet():
            if not self._frame_queue.empty():
                self._writer.write(self._frame_queue.get())
            if self._stopping_flag.isSet():
                while not self._frame_queue.empty():
                    self._writer.write(self._frame_queue.get())
                self._loop.call_soon_threadsafe(self._done_writing_flag.set)
                break
            else:
                sleep(.001)
