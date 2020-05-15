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


# Define enum like this.
class StringsEnum(Enum):
    EXAMPLE_ENTRY = auto()


# Define languages like this.
english = {StringsEnum.EXAMPLE_ENTRY: "Implement this language.",
           }

french = {StringsEnum.EXAMPLE_ENTRY: "Implémentez ce langage.",
          }

german = {StringsEnum.EXAMPLE_ENTRY: "Implementieren Sie diese Sprache.",
          }

spanish = {StringsEnum.EXAMPLE_ENTRY: "Implementa este lenguaje.",
           }

chinese = {StringsEnum.EXAMPLE_ENTRY: "实施这种语言。",
           }

# Add defined languages to strings dictionary.
strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}