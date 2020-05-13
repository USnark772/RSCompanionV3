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
from PySide2.QtWidgets import QTabWidget, QWidget


class CollapsingTab(QTabWidget):
    def __init__(self, parent, contents: QWidget, log_handlers: [StreamHandler], max_width: int = 350,
                 max_height: int = 380):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self._vis = True
        self.setTabPosition(QTabWidget.East)
        self.contents = contents
        self.tab_index = self.addTab(self.contents, "")
        self.tab_extended_width = max_width
        self.tab_collapsed_width = 20
        self.setFixedHeight(max_height)
        self.tabBarClicked.connect(self._toggle_collapse)
        self._logger.debug("Initialized")

    def set_tab_height(self, height: int = None) -> None:
        """
        Set the height of this object.
        :param height: The new height for this object.
        :return None:
        """
        self._logger.debug("running")
        if height is not None:
            self.setFixedHeight(height)
        self._logger.debug("done")

    def set_tab_text(self, text: str) -> None:
        """
        Change the text of this tab.
        :param text: The new text to use.
        :return None:
        """
        self._logger.debug("running")
        self.setTabText(self.tab_index, text)
        self._logger.debug("done")

    def _toggle_collapse(self) -> None:
        """
        Toggle whether this tab is collapsed or not.
        :return None:
        """
        self._logger.debug("running")
        if self._vis:
            self.contents.hide()
            self.setMaximumWidth(self.tab_collapsed_width)
        else:
            self.contents.show()
            self.setMaximumWidth(self.tab_extended_width)
        self._vis = not self._vis
        self._logger.debug("done")


