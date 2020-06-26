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

from RSCompanionAsync.Model.app_defs import LangEnum, app_name
from enum import Enum, auto


class StringsEnum(Enum):
    TITLE = auto()


english = {StringsEnum.TITLE: app_name}

dutch = {StringsEnum.TITLE: app_name}

french = {StringsEnum.TITLE: app_name}

german = {StringsEnum.TITLE: app_name}

russian = {StringsEnum.TITLE: app_name}

spanish = {StringsEnum.TITLE: app_name}

chinese = {StringsEnum.TITLE: app_name}

japanese = {StringsEnum.TITLE: app_name}

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
