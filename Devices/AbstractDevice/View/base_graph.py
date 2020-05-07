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
from logging import getLogger, StreamHandler
from datetime import datetime
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from Devices.AbstractDevice.Resources.abstract_strings import strings, StringsEnum, LangEnum


class AbstractMeta(ABCMeta, type(Canvas)):
    pass


class BaseGraph(Canvas, ABC, metaclass=AbstractMeta):
    """ Generic device data graphing class. """
    def __init__(self, parent, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(Figure(figsize=(5, 5)))
        self.setParent(parent)
        self._new = True
        self._nav_bar = NavBar(self, parent)
        self._nav_bar.update()
        self._leg_plot_links = dict()
        self._plots = list()  # name, coords, active
        self._v_lines = list()
        self._base_strings = dict()
        self.figure.canvas.mpl_connect('pick_event', self._onpick)
        self._logger.debug("Initialized")

    def get_nav_bar(self) -> NavBar:
        """
        Get this graph's nav bar.
        :return NavBar: This graph's nav bar.
        """
        return self._nav_bar

    def refresh_self(self):
        """ Redraw the canvas. """
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
    def plot_device_data(self, axes, name, show_in_legend) -> []:
        """
        How this specific device should plot its data.
        :param axes: The current graph.
        :param name: A given plot_name as passed in at initialization.
        :param show_in_legend: Whether to show this line in the legend.
        :return list: A list of graph lines.
        """
        pass

    def plot(self, new=False):
        """ Reset all subplots to empty then call subclass's plot function for each subplot """
        self._logger.debug("running")
        lines = {}
        self._leg_plot_links = {}
        self.figure.clear()
        self.figure.set_tight_layout(True)
        num_plots = len(self._plots)
        for i in range(num_plots):
            plot = self._plots[i]
            name = plot[0]
            active = plot[2]
            lines[name] = []
            if active:
                coords = plot[1]
                print(coords)
                axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                axes.tick_params(axis='x', labelrotation=30)
                axes.set_ylabel(name)
                if i == 0:
                    show_in_legend = True
                else:
                    show_in_legend = False
                if i == num_plots - 1:
                    axes.set_xlabel(self._base_strings[StringsEnum.GRAPH_TS])
                if not new:
                    lines[name] = self.plot_device_data(axes, name, show_in_legend)
        if not new:
            legend = self.figure.legend(loc='upper left', framealpha=0.4)
            legend.set_draggable(True)
            self._match_legend_plot_lines(legend, lines)
            self.add_vert_lines()
        self.figure.canvas.draw()
        self._logger.debug("done")

    def add_vert_lines(self, timestamp: datetime = None):
        self._logger.debug("running")
        for axes in self.figure.get_axes():
            if timestamp:
                self._vlines.append(timestamp)
                axes.axvline(timestamp)
                self.refresh_self()
            else:
                for line in self._vlines:
                    axes.axvline(line)
        self._logger.debug("done")

    def set_subplots(self, names: [str]):
        self._logger.debug("running")
        if len(names) < 1:
            return
        r = len(names)
        c = 1
        for i in range(0, r):
            self._plots.append((names[i], (r, c, i + 1), True))
        self._logger.debug("done")

    def _match_legend_plot_lines(self, legend, lines):
        """ Attach lines in all subplots to appropriate marker in legend """
        self._logger.debug("running")
        for legend_line in legend.get_lines():
            self._leg_plot_links[legend_line] = []
            legend_line.set_picker(5)
            for plot in lines:
                for line in lines[plot]:
                    if line[0] == legend_line.get_label():
                        self._leg_plot_links[legend_line].append(line[1])
        self._logger.debug("done")

    def _onpick(self, event) -> None:
        """
        Show or hide lines in subplots based on which marker in legend was clicked
        :param event: The click event.
        :return None:
        """
        self._logger.debug("running")
        print(__name__, "type of event is:", type(event))
        legend_line = event.artist
        if legend_line in self._legend_plot_links:
            plot_lines = self._legend_plot_links[legend_line]
        else:
            self._logger.debug("done, no matched lines")
            return
        for line in plot_lines:
            visible = not line.get_visible()
            line.set_visible(visible)
        if visible:
            legend_line.set_alpha(1.0)
        else:
            legend_line.set_alpha(0.2)
        self.figure.canvas.draw()
        self._logger.debug("done")
