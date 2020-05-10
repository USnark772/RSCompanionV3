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
    POST = auto()
    POST_TT = auto()
    SHADOW = auto()


english = {StringsEnum.TITLE: "Note",
           StringsEnum.POST: "Post",
           StringsEnum.POST_TT: "Post note",
           StringsEnum.SHADOW: "Enter note here",
           }

# TODO: Verify French
french = {StringsEnum.TITLE: "Remarque",
          StringsEnum.POST: "Publier",
          StringsEnum.POST_TT: "Poster une note",
          StringsEnum.SHADOW: "Entrez une note ici",
          }

# TODO: Verify German
german = {StringsEnum.TITLE: "Notiz",
          StringsEnum.POST: "Post",
          StringsEnum.POST_TT: "Notiz posten",
          StringsEnum.SHADOW: "Notiz hier eingeben",
          }

# TODO: Verify Spanish
spanish = {StringsEnum.TITLE: "Nota",
           StringsEnum.POST: "Publicar",
           StringsEnum.POST_TT: "Publicar nota",
           StringsEnum.SHADOW: "Ingrese la nota aquí",
           }

# TODO: Verify Chinese (simplified)
chinese = {StringsEnum.TITLE: "注意",
           StringsEnum.POST: "发布",
           StringsEnum.POST_TT: "发布笔记",
           StringsEnum.SHADOW: "在此处输入注释",
           }

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}
