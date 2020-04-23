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
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setMaximumSize(size)
        self.__flag = QLabel(self)
        font = QFont()
        font.setPointSize(16)
        self.__flag.setFont(font)
        self.layout().addWidget(self.__flag, 0, Qt.AlignHCenter)

        self.__set_texts()
        self.__set_tooltips()
        self.logger.debug("Initialized")

    def set_flag(self, text):
        self.logger.debug("running")
        self.__flag.setText(text)
        self.logger.debug("done")

    def get_flag(self):
        return self.__flag.text()

    def __set_texts(self):
        self.logger.debug("running")
        self.setTitle("Key Flag")
        self.__flag.setText("")
        self.logger.debug("done")

    def __set_tooltips(self):
        self.logger.debug("running")
        self.__flag.setToolTip("The most recent key pressed for reference in save file")
        self.logger.debug("done")
