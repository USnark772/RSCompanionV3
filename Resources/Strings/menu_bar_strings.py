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

from Model.app_defs import LangEnum
from enum import Enum, auto


class StringsEnum(Enum):
    FILE = auto()
    LAST_DIR = auto()
    HELP = auto()
    ABOUT_APP = auto()
    ABOUT_COMPANY = auto()
    UPDATE_CHECK = auto()
    SHOW_LOG_WINDOW = auto()
    USE_CAMS = auto
    ATTACHED_CAMS = auto()


english = {StringsEnum.FILE: "File",
           StringsEnum.LAST_DIR: "Open last save location",
           StringsEnum.HELP: "Help",
           StringsEnum.ABOUT_APP: "About RS Companion",
           StringsEnum.ABOUT_COMPANY: "About Red Scientific",
           StringsEnum.UPDATE_CHECK: "Check For Updates",
           StringsEnum.SHOW_LOG_WINDOW: "Show log window",
           StringsEnum.USE_CAMS: "Use cameras",
           StringsEnum.ATTACHED_CAMS: "Attached Camera"
           }

french = english

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french}
