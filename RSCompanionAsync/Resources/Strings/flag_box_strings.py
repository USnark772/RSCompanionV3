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
    FLAG_TT = auto()
    FLAG_HDR = auto()
    SF_FLAGS = auto()


english = {StringsEnum.TITLE: "Key Flag",
           StringsEnum.FLAG_TT: "The most recent key pressed for reference in save file",
           StringsEnum.FLAG_HDR: "timestamp, key flag",
           StringsEnum.SF_FLAGS: "flags_",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: "Sleutel vlag",
         StringsEnum.FLAG_TT: "De meest recente toets die ter referentie is ingedrukt in het opslagbestand",
         StringsEnum.FLAG_HDR: "tijdstempel, sleutel vlag",
         StringsEnum.SF_FLAGS: "vlaggen_",
         }

# French strings
french = {StringsEnum.TITLE: "Drapeau clé",
          StringsEnum.FLAG_TT: "La touche la plus récente appuyée pour référence dans le fichier de sauvegarde",
          StringsEnum.FLAG_HDR: "horodatage, drapeau clé",
          StringsEnum.SF_FLAGS: "drapeaux_",
          }

# German strings
german = {StringsEnum.TITLE: "Schlüsselflagge",
          StringsEnum.FLAG_TT: "Die zuletzt als Referenz in der Sicherungsdatei gedrückte Taste",
          StringsEnum.FLAG_HDR: "zeitstempel, schlüsselflagge",
          StringsEnum.SF_FLAGS: "Flaggen_",
          }

# Russian strings
russian = {StringsEnum.TITLE: "Ключ Флаг",
           StringsEnum.FLAG_TT: "Самая последняя клавиша нажата для ссылки в файле сохранения",
           StringsEnum.FLAG_HDR: "отметка времени, Ключ Флаг",
           StringsEnum.SF_FLAGS: "флаги_",
           }

# Spanish strings
spanish = {StringsEnum.TITLE: "Bandera clave",
           StringsEnum.FLAG_TT: "La tecla más reciente presionada para referencia en guardar archivo",
           StringsEnum.FLAG_HDR: "marca de tiempo, bandera clave",
           StringsEnum.SF_FLAGS: "banderas_",
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: "钥匙旗",
           StringsEnum.FLAG_TT: "在保存文件中按下以供参考的最新键",
           StringsEnum.FLAG_HDR: "时间戳记, 钥匙旗",
           StringsEnum.SF_FLAGS: "标志_",
           }

# Japanese strings
japanese = {StringsEnum.TITLE: "キーフラグ",
            StringsEnum.FLAG_TT: "保存ファイルで参照するために押された最新のキー",
            StringsEnum.FLAG_HDR: "タイムスタンプ, キーフラグ",
            StringsEnum.SF_FLAGS: "旗_",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
