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

from Model.app_defs import LangEnum
from enum import Enum, auto


class StringsEnum(Enum):
    TITLE = auto()
    STORAGE_ID = auto()
    PERC_FREE = auto()
    PERC_USED = auto()
    GB_FREE = auto()
    GB_USED = auto()
    MB_FREE = auto()
    MB_USED = auto()


english = {StringsEnum.TITLE: "Storage Information",
           StringsEnum.STORAGE_ID: 'Storage ID:',
           StringsEnum.PERC_FREE: "Percent free:",
           StringsEnum.PERC_USED: "Percent used:",
           StringsEnum.GB_FREE: "GB free:",
           StringsEnum.GB_USED: "GB used:",
           StringsEnum.MB_FREE: "MB free:",
           StringsEnum.MB_USED: "MB used:",
           }

# TODO: Verify French
french = {StringsEnum.TITLE: "Informations de Stockage",
          StringsEnum.STORAGE_ID: 'ID de Stockage:',
          StringsEnum.PERC_FREE: "Pourcentage inutilisé:",
          StringsEnum.PERC_USED: "Pourcentage utilisé:",
          StringsEnum.GB_FREE: "GB inutilisé:",
          StringsEnum.GB_USED: "GB utilisé:",
          StringsEnum.MB_FREE: "MB inutilisé:",
          StringsEnum.MB_USED: "MB utilisé:",
          }

# TODO: Verify German
german = {StringsEnum.TITLE: "Speicherinformationen",
          StringsEnum.STORAGE_ID: 'Speicher-ID:',
          StringsEnum.PERC_FREE: "Prozent frei:",
          StringsEnum.PERC_USED: "Prozent verwendet:",
          StringsEnum.GB_FREE: "GB frei:",
          StringsEnum.GB_USED: "GB verwendet:",
          StringsEnum.MB_FREE: "MB frei:",
          StringsEnum.MB_USED: "MB verwendet:",
          }

# TODO: Verify Spanish
spanish = {StringsEnum.TITLE: "Información de almacenamiento",
           StringsEnum.STORAGE_ID: 'ID de almacenamiento:',
           StringsEnum.PERC_FREE: "Porcentaje libre:",
           StringsEnum.PERC_USED: "Porcentaje utilizado:",
           StringsEnum.GB_FREE: "GB libre:",
           StringsEnum.GB_USED: "GB utilizado:",
           StringsEnum.MB_FREE: "MB libre:",
           StringsEnum.MB_USED: "MB utilizado:",
           }

# TODO: Verify Chinese (simplified)
chinese = {StringsEnum.TITLE: "储存资讯",
           StringsEnum.STORAGE_ID: '储存ID:',
           StringsEnum.PERC_FREE: "可用百分比:",
           StringsEnum.PERC_USED: "使用百分比:",
           StringsEnum.GB_FREE: "GB 可用的:",
           StringsEnum.GB_USED: "GB 用过的:",
           StringsEnum.MB_FREE: "MB 可用的:",
           StringsEnum.MB_USED: "MB 用过的:",
           }

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}
