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

Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from enum import Enum, auto
from RSCompanionAsync.Model.app_defs import LangEnum


class StringsEnum(Enum):
    SIGNAL_LOCKED = auto()
    NO_SIGNAL = auto()
    NA = auto()
    TIME = auto()
    SPEED = auto()
    HEADING = auto()
    ELEVATION = auto()
    LAT = auto()
    LON = auto()
    SAVE_HDR = auto()


# English strings
english = {StringsEnum.SIGNAL_LOCKED: "GPS signal locked",
           StringsEnum.NO_SIGNAL: "No GPS signal",
           StringsEnum.NA: "N/A",
           StringsEnum.TIME: "Date Time:",
           StringsEnum.SPEED: "Speed:",
           StringsEnum.HEADING: "Heading:",
           StringsEnum.ELEVATION: "Elevation:",
           StringsEnum.LAT: "Latitude:",
           StringsEnum.LON: "Longitude:",
           StringsEnum.SAVE_HDR: "raw NMEA sentence"
           }

dutch = {}

french = {}

german = {}

russian = {}

spanish = {}

chinese = {}

japanese = {}

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
