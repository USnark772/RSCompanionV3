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

from abc import ABCMeta, ABC, abstractmethod
from asyncio import create_task, sleep
from logging import getLogger, StreamHandler
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator, OldAutoLocator
from Devices.AbstractDevice.Resources.abstract_strings import strings, StringsEnum, LangEnum
import numpy as np


class AbstractMeta(ABCMeta, type(Canvas)):
    pass


class BaseGraph(Canvas, ABC, metaclass=AbstractMeta):
    """ Generic device data graphing class. """
    def __init__(self, parent=None, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(Figure(figsize=(5, 5)))
        # self.setParent(parent)
        self._new = True
        self._plots = list()  # name, coords, active
        self._v_lines = list()
        self._base_strings = dict()
        self._logger.debug("Initialized")

    def refresh_self(self) -> None:
        """
        Redraw this canvas. Good for when making changes to the graph.
        :return None:
        """
        self._logger.debug("running")
        try:
            self.figure.canvas.draw()
        except Exception as e:
            self._logger.exception("issue with drawing canvas.")
        self._logger.debug("done")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this base graph's language.
        :param lang: The lang enum to use.
        :return None:
        """
        self._logger.debug("running")
        self._base_strings = strings[lang]
        self._logger.debug("done")

    def set_new(self, is_new: bool) -> None:
        """ If graph is new then there is no data to display. """
        self._logger.debug("running")
        self._new = is_new
        self._logger.debug("done")

    def get_new(self):
        return self._new

    @abstractmethod
    async def plot_device_data(self, axes, name) -> []:
        """
        How this specific device should plot its data.
        :param axes: The current graph.
        :param name: A given plot_name as passed in at initialization.
        :return list: A list of graph lines.
        """
        pass

    async def plot(self, new=False) -> None:
        """
        Reset all subplots to empty then call subclass's plot function for each subplot
        :param new: Whether this graph has any data in it or not.
        :return None:
        """
        self._logger.debug("running")
        self.figure.clear()
        self.figure.set_tight_layout(True)
        num_plots = len(self._plots)
        axes = None
        alt_axes = None
        for i in range(num_plots):
            # print(i)
            # print(self._plots)
            plot = self._plots[i]
            name = plot[0]
            active = plot[2]
            if active:
                coords = plot[1]
                if i == 0:
                    # old code that can be deleted if new format is okay
                    # axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                    axes = self.figure.add_subplot(1, 1, 1)
                    axes.tick_params(axis='x', labelrotation=30)
                    axes.set_ylabel(name, color='#1f77b4')
                    # axes.set_yticks(step=50)
                    await sleep(.001)
                    # old code that can be deleted if new format is okay
                    # if i == num_plots - 1:
                    #     await sleep(.001)
                    #     axes.set_xlabel(self._base_strings[StringsEnum.GRAPH_TS])
                    #     await sleep(.001)
                    # axes.set_xlabel(self._base_strings[StringsEnum.GRAPH_TS])
                    if not new:
                        # axes.set_yticks(np.arange(0, 1000, step=25))
                        await create_task(self.plot_device_data(axes, name))
                else:
                    alt_axes = axes.twinx()
                    alt_axes.set_ylabel(name, color='#ff7f0e')
                    alt_axes.tick_params(axis='y', labelcolor='#ff7f0e')
                    alt_axes.set_yticks(np.arange(0, 5, step=1))
                    await sleep(.001)
                    if not new:
                        await create_task(self.plot_device_data(alt_axes, name, axes))

        if not new:
            self.add_vert_lines()
        await sleep(.001)
        self.figure.canvas.draw()
        self._logger.debug("done")

    def add_vert_lines(self, timestamp: datetime = None) -> None:
        """
        Add vertical lines at given timestamp to this graph.
        :param timestamp: The x value to add vertical lines at.
        :return None:
        """
        self._logger.debug("running")
        for axes in self.figure.get_axes():
            if timestamp:
                self._vlines.append(timestamp)
                axes.axvline(timestamp)
                self.refresh_self()
            else:
                for line in self._v_lines:
                    axes.axvline(line)
        self._logger.debug("done")

    def set_subplots(self, names: [str]) -> None:
        """
        Create a subplot per name in names.
        :param names: The names for the subplots. (Generally the same as the names of the y axes)
        :return None:
        """
        # print(names)
        self._plots = list()
        self._logger.debug("running")
        if len(names) < 1:
            return
        r = len(names)
        c = 1
        for i in range(0, r):
            self._plots.append((names[i], (r, c, i + 1), True))
        self._logger.debug("done")

    def resizeEvent(self, event):
        try:
            Canvas.resizeEvent(self, event)
        except ValueError as e:
            pass
