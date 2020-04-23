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
from PySide2.QtWidgets import QWidget, QVBoxLayout, QFrame


class CentralWidget(QWidget):
    """ This code is the overall frame inside the app main window. All other parts will go inside this. """
    def __init__(self, parent):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))
        self.logger.debug("Initialized")
