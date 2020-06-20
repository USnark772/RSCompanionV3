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

from RSCompanionAsync.Model.app_defs import LangEnum
from enum import Enum, auto


class StringsEnum(Enum):
    TITLE = auto()
    START_TIME = auto()
    BLOCK_NO = auto()


english = {StringsEnum.TITLE: "Information",
           StringsEnum.START_TIME: "Experiment start time:",
           StringsEnum.BLOCK_NO: "Block number:"
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: "Informatie",
         StringsEnum.START_TIME: "Starttijd van het experiment:",
         StringsEnum.BLOCK_NO: "Blokkeer nummer:"
         }

# French strings
french = {StringsEnum.TITLE: "Information",
          StringsEnum.START_TIME: "Heure de début de l'expérience:",
          StringsEnum.BLOCK_NO: "Numéro de bloc:"
          }

# German strings
german = {StringsEnum.TITLE: "Information",
          StringsEnum.START_TIME: "Startzeit des Experiments:",
          StringsEnum.BLOCK_NO: "Blocknummer:"
          }

# Russian strings
russian = {StringsEnum.TITLE: "Информация",
           StringsEnum.START_TIME: "Время начала эксперимента:",
           StringsEnum.BLOCK_NO: "Номер блока:"
           }

# Spanish strings
spanish = {StringsEnum.TITLE: "Información",
           StringsEnum.START_TIME: "Hora de inicio del experimento:",
           StringsEnum.BLOCK_NO: "Número de bloque:"
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: "信息",
           StringsEnum.START_TIME: "实验开始时间:",
           StringsEnum.BLOCK_NO: "块号:"
           }

# Japanese strings
japanese = {StringsEnum.TITLE: "情報",
            StringsEnum.START_TIME: "実験開始時間:",
            StringsEnum.BLOCK_NO: "ブロック番号:"
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
