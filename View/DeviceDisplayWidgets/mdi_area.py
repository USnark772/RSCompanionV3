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

from logging import getLogger
from PySide2.QtWidgets import QMdiArea, QMdiSubWindow


class MDIArea(QMdiArea):
    """ The area to show device specific views. """
    def __init__(self, parent, ch):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setMinimumSize(500, 300)
        self._logger.debug("Done")

    def add_window(self, window: QMdiSubWindow) -> None:
        """
        Add given window to the MDI Area.
        :param window: The window to add.
        :return: None.
        """
        self._logger.debug("running")
        self.addSubWindow(window)
        window.show()
        self._logger.debug("done")

    def remove_window(self, window: QMdiSubWindow) -> None:
        """
        Remove the given window from the MDI Area.
        :param window: The window to remove.
        :return: None.
        """
        self._logger.debug("running")
        self.removeSubWindow(window)
        self._logger.debug("done")

    # TODO: Implement these
    def set_window_order(self):
        # order = QMdiArea.ActivationHistoryOrder
        # order = QMdiArea.StackingOrder
        order = QMdiArea.CreationOrder
        self.setActivationOrder(order)

    def sort_windows_cascade(self):
        self.cascadeSubWindows()

    def sort_windows_tiled(self):
        self.tileSubWindows()

    def sort_windows_horizontal(self):
        pass

    def sort_windows_vertical(self):
        pass

    def set_window_view_mode(self):
        # QMdiArea.SubWindowView
        # QMdiArea.TabbedView
        pass
