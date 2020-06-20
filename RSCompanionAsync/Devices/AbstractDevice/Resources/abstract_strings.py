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

# ***********************************************************
# A template for how to setup the strings.py for your device.
# ***********************************************************

from RSCompanionAsync.Model.app_defs import LangEnum
from enum import Enum, auto


# Define enum like this.
class StringsEnum(Enum):
    EXAMPLE_ENTRY = auto()
    GRAPH_TS = auto()


# Define languages like this.
english = {StringsEnum.EXAMPLE_ENTRY: "Implement this language.",
           StringsEnum.GRAPH_TS: "Timestamp",
           }

dutch = {StringsEnum.EXAMPLE_ENTRY: "Implementeer deze taal.",
         StringsEnum.GRAPH_TS: "Tijdstempel",
         }

french = {StringsEnum.EXAMPLE_ENTRY: "Implémentez ce langage.",
          StringsEnum.GRAPH_TS: "Horodatage",
          }

german = {StringsEnum.EXAMPLE_ENTRY: "Implementieren Sie diese Sprache.",
          StringsEnum.GRAPH_TS: "Zeitstempel",
          }

russian = {StringsEnum.EXAMPLE_ENTRY: "Реализуйте этот язык.",
           StringsEnum.GRAPH_TS: "Отметка",
           }

spanish = {StringsEnum.EXAMPLE_ENTRY: "Implementa este lenguaje.",
           StringsEnum.GRAPH_TS: "marca de tiempo",
           }

chinese = {StringsEnum.EXAMPLE_ENTRY: "实施这种语言。",
           StringsEnum.GRAPH_TS: "时间戳记",
           }

japanese = {StringsEnum.EXAMPLE_ENTRY: "この言語を実装します。",
            StringsEnum.GRAPH_TS: "タイムスタンプ",
            }

# Add defined languages to strings dictionary.
strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
