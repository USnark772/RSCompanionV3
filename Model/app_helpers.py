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

import os
from shutil import disk_usage
from logging import getLogger
from tempfile import gettempdir
from datetime import datetime
from PySide2.QtWidgets import QPushButton, QFrame
from Model.app_defs import button_normal_style, button_pressed_style
from Model.app_strings import program_output_hdr

logger = getLogger(__name__)


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


def get_remaining_disk_size(path: str = ''):
    if path == '':
        path = os.path.abspath(os.sep)
    drive_name = os.path.splitdrive(path)[0]
    info = disk_usage(path)
    mb = round(info[2] / (1024 ** 2))
    gb = round(info[2] / (1024 ** 3))
    percentage = round(info[2] / info[0] * 100)
    return drive_name, percentage, gb, mb


def get_current_time(day=False, time=False, mil=False, save=False, graph=False, device=False, date_time=None):
    """
    Returns a datetime string with day, time, and milliseconds options. Also available, save is formatted for when
    colons are not acceptable and graph is for the graphing utility which requires a datetime object
    """
    logger.debug("running")
    if not date_time:
        date_time = datetime.now()
    if day and time and mil:
        logger.debug("day, time, mil. done")
        return date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    elif day and time and not mil:
        logger.debug("day, time. done")
        return date_time.strftime("%Y-%m-%d %H:%M:%S")
    elif day and not time and not mil:
        logger.debug("day. done")
        return date_time.strftime("%Y-%m-%d")
    elif not day and time and not mil:
        logger.debug("time, done")
        return date_time.strftime("%H:%M:%S")
    elif not day and time and mil:
        logger.debug("time, mil. done")
        return date_time.strftime("%H:%M:%S.%f")
    elif save:
        logger.debug("save. done")
        return date_time.strftime("%Y-%m-%d-%H-%M-%S")
    elif graph or device:
        logger.debug("graph or device. done")
        return date_time


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
