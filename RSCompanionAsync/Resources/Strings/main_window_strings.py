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

from RSCompanionAsync.Model.app_defs import LangEnum, app_name, company_name
from enum import Enum, auto


class StringsEnum(Enum):
    TITLE = auto()
    CLOSE_TITLE = auto()
    CLOSE_APP_CONFIRM = auto()


english = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "Close " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "Close app? Any unsaved progress will be lost!",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: app_name,
         StringsEnum.CLOSE_TITLE: "Dicht " + company_name,
         StringsEnum.CLOSE_APP_CONFIRM: "App sluiten? Alle niet-opgeslagen voortgang gaat verloren!",
         }

# French strings
french = {StringsEnum.TITLE: app_name,
          StringsEnum.CLOSE_TITLE: "Fermer " + company_name,
          StringsEnum.CLOSE_APP_CONFIRM: "Fermer l'application? Tout progrès non enregistré sera perdu!",
          }

# German strings
german = {StringsEnum.TITLE: app_name,
          StringsEnum.CLOSE_TITLE: "Schließen " + company_name,
          StringsEnum.CLOSE_APP_CONFIRM: "App schließen? Jeder nicht gespeicherte Fortschritt geht verloren!",
          }

# Russian strings
russian = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "закрывать " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "Закрыть приложение? Любой несохраненный прогресс будет потерян!",
           }

# Spanish strings
spanish = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "Cerrar " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "¿Cerrar app? ¡Cualquier progreso no guardado se perderá!",
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "关闭 " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "关闭应用程式？ 任何未保存的进度将丢失！",
           }

# Japanese strings
japanese = {StringsEnum.TITLE: app_name,
            StringsEnum.CLOSE_TITLE: "閉じる " + company_name,
            StringsEnum.CLOSE_APP_CONFIRM: "アプリを閉じますか？ 保存されていない進行状況は失われます！",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
