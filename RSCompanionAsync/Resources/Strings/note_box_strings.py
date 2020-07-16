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
    POST = auto()
    POST_TT = auto()
    SHADOW = auto()
    NOTE_HDR = auto()
    SF_NOTES = auto()


english = {StringsEnum.TITLE: "Note",
           StringsEnum.POST: "Post",
           StringsEnum.POST_TT: "Post note",
           StringsEnum.SHADOW: "Enter note here",
           StringsEnum.NOTE_HDR: "timestamp, note",
           StringsEnum.SF_NOTES: "notes_",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: "Notitie",
         StringsEnum.POST: "Posten",
         StringsEnum.POST_TT: "Notitie plaatsen",
         StringsEnum.SHADOW: "Notitie hier invoeren",
         StringsEnum.NOTE_HDR: "tijdstempel, notitie",
         StringsEnum.SF_NOTES: "notities_",
         }

# French strings
french = {StringsEnum.TITLE: "Remarque",
          StringsEnum.POST: "Publier",
          StringsEnum.POST_TT: "Poster une note",
          StringsEnum.SHADOW: "Entrez une note ici",
          StringsEnum.NOTE_HDR: "horodatage, remarque",
          StringsEnum.SF_NOTES: "remarques_",
          }

# German strings
german = {StringsEnum.TITLE: "Notiz",
          StringsEnum.POST: "Post",
          StringsEnum.POST_TT: "Notiz posten",
          StringsEnum.SHADOW: "Notiz hier eingeben",
          StringsEnum.NOTE_HDR: "Zeitstempel, Notiz",
          StringsEnum.SF_NOTES: "Aufzeichnungen_",
          }

# Russian strings
russian = {StringsEnum.TITLE: "нота",
           StringsEnum.POST: "Публиковать",
           StringsEnum.POST_TT: "Опубликовать заметку",
           StringsEnum.SHADOW: "Введите примечание здесь",
           StringsEnum.NOTE_HDR: "отметка времени, Запись",
           StringsEnum.SF_NOTES: "ноты_",
           }

# Spanish strings
spanish = {StringsEnum.TITLE: "Nota",
           StringsEnum.POST: "Publicar",
           StringsEnum.POST_TT: "Publicar nota",
           StringsEnum.SHADOW: "Ingrese la nota aquí",
           StringsEnum.NOTE_HDR: "marca de tiempo, nota",
           StringsEnum.SF_NOTES: "notas_",
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: "注意",
           StringsEnum.POST: "发布",
           StringsEnum.POST_TT: "发布笔记",
           StringsEnum.SHADOW: "在此处输入注释",
           StringsEnum.NOTE_HDR: "时间戳记, 注意",
           StringsEnum.SF_NOTES: "注意_",
           }

# Japanese strings
japanese = {StringsEnum.TITLE: "ノート",
            StringsEnum.POST: "ポスト",
            StringsEnum.POST_TT: "ポストノート",
            StringsEnum.SHADOW: "ここにメモを入力",
            StringsEnum.NOTE_HDR: "タイムスタンプ, 注意",
            StringsEnum.SF_NOTES: "ノート_",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
