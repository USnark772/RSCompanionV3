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
from RSCompanionAsync.Devices.AbstractDevice.View.abstract_view import AbstractView


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

        # Dummy subwindows for testing.
        # from Devices.DRT.View.drt_view import DRTView as subwindow
        # from Devices.VOG.View.vog_view import VOGView as subwindow
        # for i in range(6):
        #     window = subwindow()
        #     self.add_window(window)

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
        window.restore_window()
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

    def set_window_order(self, order: int = 0) -> None:
        """
        Set the order of the subwindows when put into a list
        :param order: int 0-2; 0 = Creation order, 1 = Stacking order, 2 = Activation order

        """
        if order == 0:
            setval = QMdiArea.CreationOrder
        if order == 1:
            setval = QMdiArea.StackingOrder
        if order == 2:
            setval = QMdiArea.ActivationHistoryOrder

        self.setActivationOrder(setval)

    def sort_windows_cascade(self) -> None:
        """
        Sort subwindows in a cascade format
        :return None:
        """
        self._logger.debug("running")
        self.setActivationOrder(QMdiArea.StackingOrder)
        sizes = dict()
        window_list = self.subWindowList()
        for win in window_list:
            sizes[win] = (win.width(), win.height())
        self.cascadeSubWindows()
        for win in window_list:
            size = sizes[win]
            win.resize(size[0], size[1])
        self.setActivationOrder(QMdiArea.CreationOrder)
        self._logger.debug("done")

    def sort_windows_tiled(self) -> None:
        """
        Tile subwindows
        :return None:
        """
        self._logger.debug("running")
        self.tileSubWindows()
        self._logger.debug("done")

    def sort_windows_horizontal(self) -> None:
        """
        Sort subwindows horizontally
        :return None:
        """
        self._logger.debug("running")
        window_list = self.subWindowList()
        for i in range(len(window_list)):
            if i == 0:
                window_list[i].move(0, 0)
            else:
                prev = window_list[i-1]
                window_list[i].move(prev.pos().x() + prev.width(), 0)
        self._logger.debug("done")

    def sort_windows_vertical(self) -> None:
        """
        Sort subwindows vertically
        :return None:
        """
        self._logger.debug("running")
        window_list = self.subWindowList()
        for i in range(len(window_list)):
            if i == 0:
                window_list[i].move(0, 0)
            else:
                prev = window_list[i-1]
                window_list[i].move(0, prev.pos().y() + prev.height())
        self._logger.debug("done")

    # TODO: Implement this
    def set_window_view_mode(self):
        # QMdiArea.SubWindowView
        # QMdiArea.TabbedView
        pass
