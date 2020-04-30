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
Date: 2019 - 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from cv2 import VideoWriter_fourcc, CAP_DSHOW
from enum import Enum, auto


""" General definitions for the app """

#################################################################################################################
# Model
#################################################################################################################

version_url = "https://raw.githubusercontent.com/redscientific/CompanionApp/master/Version.txt"
log_format = '%(levelname)s - %(name)s - %(funcName)s: %(message)s'
# TODO: Switch image_file_path for build
image_file_path = '../asyncCompanion/View/Images/'
# image_file_path = 'Images/'
# TODO: Increment version number for build
current_version = 2.0

#################################################################################################################
# View
#################################################################################################################

button_box_start_image_filepath = image_file_path + "green_arrow.png"
button_box_pause_image_filepath = image_file_path + "red_vertical_bars.png"

_compliant_text_color = "rgb(0, 0, 0)"
_error_text_color = "rgb(255, 0, 0)"
_selection_color = "rgb(0, 150, 255)"
_font_size = "12px"
tab_line_edit_compliant_style = "QLineEdit { color: " \
                                + _compliant_text_color \
                                + "; selection-background-color: " \
                                + _selection_color \
                                + "; font: " \
                                + _font_size + "; }"
tab_line_edit_error_style = "QLineEdit { color: " \
                            + _error_text_color \
                            + "; selection-background-color: " \
                            + _selection_color \
                            + "; font: " \
                            + _font_size + "; }"

# "QPushButton:pressed { background-color: rgb(150, 180, 200);
button_pressed_style = "QPushButton:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, " \
                       "stop: 0 #dadbde, stop: 1 #f6f7fa); font: " + _font_size + "; }"

# "background-color: rgb(230, 230, 230); " \
button_normal_style = "QPushButton { border: 1px solid #8f8f91; background-color: qlineargradient(x1: 0, y1: 0, " \
                      "x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde); min-height: 22px; font: " + _font_size + "; }"


class LangEnum(Enum):
    ENG = auto()
    FRE = auto()


#################################################################################################################
# Controller
#################################################################################################################
