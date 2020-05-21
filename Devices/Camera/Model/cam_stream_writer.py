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
from Devices.Camera.Model import cam_defs as defs
from Model.app_helpers import await_event, end_tasks


class StreamWriter:
    def __init__(self, frame_queue: SimpleQueue):
        self._writer: VideoWriter = VideoWriter()
        self._frame_queue = frame_queue
        self._running = False
        self._stopping = False
        self._done_writing = False
        self._done_writing_event = Event()
        self._awaitable_tasks = []
        self._loop = get_event_loop()

    def cleanup(self) -> None:
        """
        Cleanup this object and prep for app closure.
        :return None:
        """
        self.stop()

    def await_done_writing(self) -> futures:
        """
        Signal when there is a done writing frames event.
        :return futures: If the flag is set.
        """
        return await_event(self._done_writing_event)

    def start(self, filename: str, fps: int, size: (int, int)) -> None:
        """
        Start this writer with given parameters.
        :param filename: The filename to write to.
        :param fps: The fps to save images with.
        :param size: The size to save images as.
        :return None:
        """
        self._running = True
        self._writer = VideoWriter(filename, defs.cap_codec, fps, size)
        self._awaitable_tasks.append(self._loop.run_in_executor(None, self._update))

    def stop(self) -> None:
        """
        Stop this writer.
        :return None:
        """
        if self._running:
            create_task(self._stop_writer())
        self._running = False

    async def _stop_writer(self) -> None:
        """
        Signal stop and wait for writer to finish writing any frames not yet written.
        :return None:
        """
        self._stopping = True
        await self.await_done_writing()
        self._stopping = False
        await create_task(end_tasks(self._awaitable_tasks))

    async def _update(self) -> None:
        """
        Continuously check for frames to save and save them. Finish saving before exiting if stopping before all
        frames are saved.
        :return None:
        """
        while True:
            if not self._frame_queue.empty():
                self._writer.write(self._frame_queue.get())
            if self._stopping:
                while not self._frame_queue.empty():
                    self._writer.write(self._frame_queue.get())
                self._loop.call_soon_threadsafe(self._done_writing_event.set)
                break
            else:
                await sleep(.001)
