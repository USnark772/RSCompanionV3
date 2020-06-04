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
from asyncio import sleep, Event
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_defs import common_resolutions


class SizeGetter:
    def __init__(self, stream: StreamReader, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._stream = stream
        self._done_flag = Event()
        self._current_status = 0
        self.running = True

    async def get_sizes(self) -> list:
        """
        Get supported resolutions and return as list.
        :return list: The list of supported frame resolutions for the given StreamReader.
        """
        sizes = list()
        initial_size = self._stream.get_current_frame_size()
        sizes.append(initial_size)
        if initial_size not in common_resolutions:
            list_index = 0
        else:
            list_index = common_resolutions.index(initial_size) + 1
        for i in range(list_index, len(common_resolutions)):
            ret, res = self._stream.test_frame_size(common_resolutions[i])
            if ret and res in common_resolutions:
                sizes.append(res)
            self._current_status = i / (len(common_resolutions) - list_index) * 100
            await sleep(.001)
        self._stream.change_frame_size(initial_size)
        sizes.sort()
        return sizes

    @property
    def status(self) -> int:
        return self._current_status
