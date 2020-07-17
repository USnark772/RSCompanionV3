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
    SF_TIMES = auto()
    TIMESTAMP = auto()
    TIME_EVENT = auto()
    CREATE = auto()
    END = auto()
    START = auto()
    STOP = auto()


english = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "Close " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "Close app? Any unsaved progress will be lost!",
           StringsEnum.SF_TIMES: "times_",
           StringsEnum.TIMESTAMP: "timestamp",
           StringsEnum.TIME_EVENT: "event",
           StringsEnum.CREATE: "create",
           StringsEnum.END: "end",
           StringsEnum.START: "start",
           StringsEnum.STOP: "stop",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: app_name,
         StringsEnum.CLOSE_TITLE: "Dicht " + company_name,
         StringsEnum.CLOSE_APP_CONFIRM: "App sluiten? Alle niet-opgeslagen voortgang gaat verloren!",
         StringsEnum.SF_TIMES: "keer_",
         StringsEnum.TIMESTAMP: "tijdstempel",
         StringsEnum.TIME_EVENT: "evenement",
         StringsEnum.CREATE: "creëer",
         StringsEnum.END: "einde",
         StringsEnum.START: "begin",
         StringsEnum.STOP: "hou op",
         }

# French strings
french = {StringsEnum.TITLE: app_name,
          StringsEnum.CLOSE_TITLE: "Fermer " + company_name,
          StringsEnum.CLOSE_APP_CONFIRM: "Fermer l'application? Tout progrès non enregistré sera perdu!",
          StringsEnum.SF_TIMES: "fois_",
          StringsEnum.TIMESTAMP: "horodatage",
          StringsEnum.TIME_EVENT: "événement",
          StringsEnum.CREATE: "créer",
          StringsEnum.END: "fin",
          StringsEnum.START: "début",
          StringsEnum.STOP: "arrêtez",
          }

# German strings
german = {StringsEnum.TITLE: app_name,
          StringsEnum.CLOSE_TITLE: "Schließen " + company_name,
          StringsEnum.CLOSE_APP_CONFIRM: "App schließen? Jeder nicht gespeicherte Fortschritt geht verloren!",
          StringsEnum.SF_TIMES: "mal_",
          StringsEnum.TIMESTAMP: "Zeitstempel",
          StringsEnum.TIME_EVENT: "Veranstaltung",
          StringsEnum.CREATE: "erstellen",
          StringsEnum.END: "ende",
          StringsEnum.START: "anfang",
          StringsEnum.STOP: "halt",
          }

# Russian strings
russian = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "закрывать " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "Закрыть приложение? Любой несохраненный прогресс будет потерян!",
           StringsEnum.SF_TIMES: "раз_",
           StringsEnum.TIMESTAMP: "отметка времени",
           StringsEnum.TIME_EVENT: "мероприятие",
           StringsEnum.CREATE: "Создайте",
           StringsEnum.END: "Конец",
           StringsEnum.START: "Начало",
           StringsEnum.STOP: "стоп",
           }

# Spanish strings
spanish = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "Cerrar " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "¿Cerrar app? ¡Cualquier progreso no guardado se perderá!",
           StringsEnum.SF_TIMES: "veces_",
           StringsEnum.TIMESTAMP: "marca de tiempo",
           StringsEnum.TIME_EVENT: "evento",
           StringsEnum.CREATE: "crear",
           StringsEnum.END: "final",
           StringsEnum.START: "comienzo",
           StringsEnum.STOP: "detener",
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: app_name,
           StringsEnum.CLOSE_TITLE: "关闭 " + company_name,
           StringsEnum.CLOSE_APP_CONFIRM: "关闭应用程式？ 任何未保存的进度将丢失！",
           StringsEnum.SF_TIMES: "次_",
           StringsEnum.TIMESTAMP: "时间戳记",
           StringsEnum.TIME_EVENT: "事件",
           StringsEnum.CREATE: "创建",
           StringsEnum.END: "结束",
           StringsEnum.START: "开始",
           StringsEnum.STOP: "停",
           }

# Japanese strings
japanese = {StringsEnum.TITLE: app_name,
            StringsEnum.CLOSE_TITLE: "閉じる " + company_name,
            StringsEnum.CLOSE_APP_CONFIRM: "アプリを閉じますか？ 保存されていない進行状況は失われます！",
            StringsEnum.SF_TIMES: "回_",
            StringsEnum.TIMESTAMP: "タイムスタンプ",
            StringsEnum.TIME_EVENT: "出来事",
            StringsEnum.CREATE: "作成する",
            StringsEnum.END: "終わり",
            StringsEnum.START: "開始",
            StringsEnum.STOP: "やめる",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
