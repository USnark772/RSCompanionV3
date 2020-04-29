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
from tempfile import gettempdir
from PySide2.QtWidgets import QPushButton, QFrame
from Model.app_defs import button_normal_style, button_pressed_style
from Model.app_strings import program_output_hdr


def setup_log_file(file_name: str) -> str:
    """
    Create program output file to save log.
    :param file_name: Name of the save log
    :return str: full directory to the save log, including the save log name
    """

    fname = gettempdir() + "\\" + file_name
    with open(fname, "w") as temp:
        temp.write(program_output_hdr)
    return fname


class ClickAnimationButton(QPushButton):
    def __init__(self, parent=None):
        self.logger = getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.pressed.connect(self.pressed_color)
        self.released.connect(self.released_state)
        self.setStyleSheet(button_normal_style)
        self.logger.debug("Initialized")

    def pressed_color(self):
        self.setStyleSheet(button_pressed_style)

    def released_state(self):
        self.setStyleSheet(button_normal_style)


class EasyFrame(QFrame):
    """ Creates a frame for display purposes depending on bools. """
    def __init__(self, line=False, vert=False):
        self.logger = getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__()
        if line:
            if vert:
                self.setFrameShape(QFrame.VLine)
            else:
                self.setFrameShape(QFrame.HLine)
            self.setFrameShadow(QFrame.Sunken)
        else:
            self.setFrameShape(QFrame.StyledPanel)
            self.setFrameShadow(QFrame.Raised)
        self.logger.debug("Initialized")
