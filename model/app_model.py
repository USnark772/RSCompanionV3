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

from asyncio import get_event_loop, all_tasks, current_task, gather
from aioserial import AioSerial


class AppModel:
    def __init__(self):
        self._devices = {}

    def add_device(self, device: (str, AioSerial)):
        self._devices[device[0]] = device[1]

    @staticmethod
    async def cleanup():
        tasks = [t for t in all_tasks() if t is not current_task()]
        [task.cancel() for task in tasks]
        await gather(*tasks)
        get_event_loop().stop()
