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
Date: 2019
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""


import logging
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt


class FlagBox(QGroupBox):
    """ This code is for showing and storing the keyflag which in this case is the last letter key the user pressed. """
    def __init__(self, parent, size, ch):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setMaximumSize(size)
        self._flag = QLabel(self)
        font = QFont()
        font.setPointSize(16)
        self._flag.setFont(font)
        self.layout().addWidget(self._flag, 0, Qt.AlignHCenter)

        self._set_texts()
        self._set_tooltips()
        self._logger.debug("Initialized")

    def set_flag(self, text):
        self._logger.debug("running")
        self._flag.setText(text)
        self._logger.debug("done")

    def get_flag(self):
        return self._flag.text()

    def _set_texts(self):
        self._logger.debug("running")
        self.setTitle("Key Flag")
        self._flag.setText("")
        self._logger.debug("done")

    def _set_tooltips(self):
        self._logger.debug("running")
        self._flag.setToolTip("The most recent key pressed for reference in save file")
        self._logger.debug("done")
