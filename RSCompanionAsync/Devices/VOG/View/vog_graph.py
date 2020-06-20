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
Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from logging import getLogger, StreamHandler
from asyncio import create_task, sleep
from datetime import datetime, timedelta
from RSCompanionAsync.Devices.AbstractDevice.View.base_graph import BaseGraph
from RSCompanionAsync.Devices.VOG.Resources.vog_strings import strings, StringsEnum, LangEnum


class VOGGraph(BaseGraph):
    def __init__(self, parent=None, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent, log_handlers)
        self._data = list()
        self._strings = dict()
        self._logger.debug("Initialized")

    async def show(self) -> None:
        self.set_subplots([self._data[0]])
        await create_task(self.plot(self.get_new()))

    def clear_graph(self) -> None:
        """
        Clear this graph of any device data.
        :return None:
        """
        self._data = [self._data[0], [], [], []]
        self.set_new(True)
        create_task(self.show())

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this device graph's language.
        :param lang: The lang enum to use.
        :return None:
        """
        self._logger.debug("running")
        super(VOGGraph, self).set_lang(lang)
        self._strings = strings[lang]
        self._change_plot_name(self._strings[StringsEnum.PLOT_NAME_OPEN_CLOSE])
        create_task(self.show())
        self._logger.debug("done")

    async def plot_device_data(self, axes, name) -> []:
        self._logger.debug("running")
        left = datetime.now()
        right = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        await sleep(.001)
        axes.plot(self._data[1], self._data[2], marker='o', linestyle='None')
        axes.plot(self._data[1], self._data[3], marker='s', linestyle='None')
        await sleep(.001)
        if len(self._data[1]) > 0:
            if right < self._data[1][-1]:
                right = self._data[1][-1]
            if left > self._data[1][0]:
                left = self._data[1][0]
        temp_left = right - timedelta(minutes=2)
        if left < temp_left:
            left = temp_left
        await sleep(.001)
        axes.set_xlim(left=left - timedelta(seconds=10), right=right + timedelta(seconds=10))
        await sleep(.001)
        self._logger.debug("done")

    def add_data(self, data: []) -> None:
        """
        Ensure data comes in as type: x, y, y
        :return None:
        """
        self._logger.debug("running")
        self.set_new(False)
        self._data[1].append(data[0])
        self._data[2].append(data[1])
        self._data[3].append(data[2])
        create_task(self.plot())
        self._logger.debug("done")

    def _change_plot_name(self, name: str) -> None:
        """
        Change the name of the plot.
        :param name: The new plot name.
        :return None:
        """
        if len(self._data) == 0:
            self._data = [name, [], [], []]
        else:
            self._data[0] = name
