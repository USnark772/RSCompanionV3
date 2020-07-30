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
    BLOCK_NUM = auto()
    CUR_TIME = auto()
    BLK_ST_TIME = auto()


english = {StringsEnum.TITLE: "Information",
           StringsEnum.START_TIME: "Experiment start time:",
           StringsEnum.BLOCK_NUM: "Block number:",
           StringsEnum.CUR_TIME: "Current time:",
           StringsEnum.BLK_ST_TIME: "Block start time:",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: "Informatie",
         StringsEnum.START_TIME: "Starttijd van het experiment:",
         StringsEnum.BLOCK_NUM: "Blokkeer nummer:",
         StringsEnum.CUR_TIME: "Huidige tijd:",
         StringsEnum.BLK_ST_TIME: "Starttijd blokkeren:",
         }

# French strings
french = {StringsEnum.TITLE: "Information",
          StringsEnum.START_TIME: "Heure de début de l'expérience:",
          StringsEnum.BLOCK_NUM: "Numéro de bloc:",
          StringsEnum.CUR_TIME: "Heure actuelle:",
          StringsEnum.BLK_ST_TIME: "Heure de début du bloc:",
          }

# German strings
german = {StringsEnum.TITLE: "Information",
          StringsEnum.START_TIME: "Startzeit des Experiments:",
          StringsEnum.BLOCK_NUM: "Blocknummer:",
          StringsEnum.CUR_TIME: "Aktuelle Uhrzeit:",
          StringsEnum.BLK_ST_TIME: "Startzeit blockieren:",
          }

# Russian strings
russian = {StringsEnum.TITLE: "Информация",
           StringsEnum.START_TIME: "Время начала эксперимента:",
           StringsEnum.BLOCK_NUM: "Номер блока:",
           StringsEnum.CUR_TIME: "Текущее время:",
           StringsEnum.BLK_ST_TIME: "Время начала блока:",
           }

# Spanish strings
spanish = {StringsEnum.TITLE: "Información",
           StringsEnum.START_TIME: "Hora de inicio del experimento:",
           StringsEnum.BLOCK_NUM: "Número de bloque:",
           StringsEnum.CUR_TIME: "Tiempo actual:",
           StringsEnum.BLK_ST_TIME: "Bloquear hora de inicio:",
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: "信息",
           StringsEnum.START_TIME: "实验开始时间:",
           StringsEnum.BLOCK_NUM: "块号:",
           StringsEnum.CUR_TIME: "当前时间:",
           StringsEnum.BLK_ST_TIME: "阻止开始时间:",
           }

# Japanese strings
japanese = {StringsEnum.TITLE: "情報",
            StringsEnum.START_TIME: "実験開始時間:",
            StringsEnum.BLOCK_NUM: "ブロック番号:",
            StringsEnum.CUR_TIME: "現在の時刻:",
            StringsEnum.BLK_ST_TIME: "ブロック開始時間:",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
