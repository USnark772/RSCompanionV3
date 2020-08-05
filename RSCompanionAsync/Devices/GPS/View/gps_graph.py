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

Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

import numpy as np
from logging import getLogger, StreamHandler
from asyncio import create_task, sleep
from datetime import datetime, timedelta
from RSCompanionAsync.Devices.AbstractDevice.View.base_graph import BaseGraph
from RSCompanionAsync.Devices.GPS.Resources.gps_strings import strings, StringsEnum, LangEnum


class GPSGraph(BaseGraph):
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
        pass

    def clear_graph(self) -> None:
        """
        Clear this graph of any device data.
        :return None:
        """
        pass

    async def plot_device_data(self, axes, name) -> []:
        self._logger.debug("running")
        print("implement gps_graph.py plot_device_data")
        self._logger.debug("done")

    def add_data(self, data: []) -> None:
        self._logger.debug("running")
        print("implement gps_graph.py add_data()")
        self._logger.debug("done")

    def add_empty_point(self):
        if self.get_new():
            return
        print("implement gps_graph.py add_empty_point")

    def _change_plot_names(self, names) -> None:
        print("implement gps_graph.py ")
