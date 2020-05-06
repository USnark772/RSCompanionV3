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
from datetime import datetime, timedelta
from Devices.AbstractDevice.View.base_graph import BaseGraphObj
from Devices.DRT.Resources.drt_strings import strings, StringsEnum, LangEnum


class DRTGraph(BaseGraphObj):
    def __init__(self, parent, dev_name: str, lang: LangEnum, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._strings = strings[lang]
        plot_names = [self._strings[StringsEnum.PLOT_NAME_RT], self._strings[StringsEnum.PLOT_NAME_CLICKS]]
        super().__init__(parent, "DRT", plot_names, log_handlers)
        self._dev_name = dev_name
        self._data = dict()
        for name in plot_names:
            self._data[name] = [[], []]
        self.set_texts()
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The lang enum to use.
        :return None:
        """
        self._strings = strings[lang]
        self.set_texts()

    def plot_device_data(self, axes, name, show_in_legend) -> []:
        self._logger.debug("running")
        data = self._data[name]
        lines = []
        left = datetime.now()
        right = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if show_in_legend:
            the_label = self._dev_name
        else:
            the_label = "_nolegend_"
        line, = axes.plot(data[0], data[1], label=the_label, marker='o')
        lines.append((self._dev_name, line))
        if len(data[0]) > 0:
            if right < data[0][-1]:
                right = data[0][-1]
            if left > data[0][0]:
                left = data[0][0]
        if left < right - timedelta(minutes=2):
            left = right - timedelta(minutes=2)
        axes.set_xlim(left=left - timedelta(seconds=10), right=right + timedelta(seconds=10))
        self._logger.debug("done")
        return lines

    def add_data(self, data):
        """ Ensure data comes in as type, x, y """
        self.logger.debug("running")
        self.set_new(False)
        self.__data[data[0]][0].append(data[1])
        self.__data[data[0]][1].append(data[2])
        # self.__calc_mean(self.__data[port_data[0]])
        self.plot()
        self.logger.debug("done")

    def add_empty_point(self, timestamp):
        if self.get_new():
            return
        for data in self.__data.values():
            data[0].append(timestamp)
            data[1].append(None)
        self.refresh_self()

    # TODO: Implement.
    def set_texts(self):
        pass
