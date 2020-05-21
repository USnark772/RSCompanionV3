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
from PySide2.QtWidgets import QMdiArea
from PySide2.QtCore import QSize, Qt
from Devices.AbstractDevice.View.abstract_view import AbstractView


class MDIArea(QMdiArea):
    """ The area to show device specific views. """
    def __init__(self, parent=None, size: QSize = QSize(10, 10), log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setMinimumSize(size)
        self._logger.debug("Done")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def add_window(self, window: AbstractView) -> None:
        """
        Add given window to the MDI Area.
        :param window: The window to add.
        :return: None.
        """
        self._logger.debug("running")
        window.setParent(self)
        self.addSubWindow(window)
        window.show()
        self._logger.debug("done")

    def remove_window(self, window: AbstractView) -> None:
        """
        Remove the given window from the MDI Area.
        :param window: The window to remove.
        :return: None.
        """
        self._logger.debug("running")
        self.removeSubWindow(window)
        self._logger.debug("done")

    # TODO: Implement this
    def set_window_order(self):
        # order = QMdiArea.ActivationHistoryOrder
        # order = QMdiArea.StackingOrder
        order = QMdiArea.CreationOrder
        self.setActivationOrder(order)

    # TODO: Implement this
    def sort_windows_cascade(self):
        self.cascadeSubWindows()

    # TODO: Implement this
    def sort_windows_tiled(self):
        self.tileSubWindows()

    # TODO: Implement this
    def sort_windows_horizontal(self):
        window_list = self.subWindowList()
        for i in range(len(window_list)):
            if i == 0:
                window_list[i].move(0, 0)
            else:
                prev = window_list[i-1]
                window_list[i].move(prev.pos().x() + prev.width(), 0)

    # TODO: Implement this
    def sort_windows_vertical(self):
        window_list = self.subWindowList()
        for i in range(len(window_list)):
            if i == 0:
                window_list[i].move(0, 0)
            else:
                prev = window_list[i-1]
                window_list[i].move(0, prev.pos().y() + prev.height())

    # TODO: Implement this
    def set_window_view_mode(self):
        # QMdiArea.SubWindowView
        # QMdiArea.TabbedView
        pass
