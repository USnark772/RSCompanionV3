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
    CREATE = auto()
    END = auto()
    CREATE_TT = auto()
    END_TT = auto()
    START_TT = auto()
    RESUME_TT = auto()
    PAUSE_TT = auto()
    COND_NAME_SHADOW = auto()


english = {StringsEnum.TITLE: "Experiment",
           StringsEnum.CREATE: "Create",
           StringsEnum.END: "End",
           StringsEnum.CREATE_TT: "Create a new experiment",
           StringsEnum.END_TT: "End experiment",
           StringsEnum.START_TT: "Begin experiment",
           StringsEnum.RESUME_TT: "Resume experiment",
           StringsEnum.PAUSE_TT: "Pause experiment",
           StringsEnum.COND_NAME_SHADOW: "Optional condition name",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.TITLE: "Experiment",
         StringsEnum.CREATE: "Creëer",
         StringsEnum.END: "Einde",
         StringsEnum.CREATE_TT: "Maak een nieuw experiment",
         StringsEnum.END_TT: "Einde experiment",
         StringsEnum.START_TT: "Begin met experimenteren",
         StringsEnum.RESUME_TT: "Hervat experiment",
         StringsEnum.PAUSE_TT: "Pauzeer het experiment",
         StringsEnum.COND_NAME_SHADOW: "Optionele conditienaam",
         }

# French strings
french = {StringsEnum.TITLE: "Expérience",
          StringsEnum.CREATE: "Créer",
          StringsEnum.END: "Fin",
          StringsEnum.CREATE_TT: "Créer une nouvelle expérience",
          StringsEnum.END_TT: "Fin de l'expérience",
          StringsEnum.START_TT: "Commencer l'expérience",
          StringsEnum.RESUME_TT: "Reprendre l'expérience",
          StringsEnum.PAUSE_TT: "Suspendre l'expérience",
          StringsEnum.COND_NAME_SHADOW: "Nom de condition facultatif",
          }

# German strings
german = {StringsEnum.TITLE: "Experiment",
          StringsEnum.CREATE: "Erstellen",
          StringsEnum.END: "Ende",
          StringsEnum.CREATE_TT: "Erstellen Sie ein neues Experiment",
          StringsEnum.END_TT: "Experiment beenden",
          StringsEnum.START_TT: "Experiment beginnen",
          StringsEnum.RESUME_TT: "Experiment fortsetzen",
          StringsEnum.PAUSE_TT: "Experiment anhalten",
          StringsEnum.COND_NAME_SHADOW: "Optionaler Bedingungsname",
          }

# Russian strings
russian = {StringsEnum.TITLE: "эксперимент",
           StringsEnum.CREATE: "Создайте",
           StringsEnum.END: "Конец",
           StringsEnum.CREATE_TT: "Создать новый эксперимент",
           StringsEnum.END_TT: "Конец эксперимента",
           StringsEnum.START_TT: "Начать эксперимент",
           StringsEnum.RESUME_TT: "Возобновить эксперимент",
           StringsEnum.PAUSE_TT: "Пауза эксперимента",
           StringsEnum.COND_NAME_SHADOW: "Необязательное имя условия",
           }

# Spanish strings
spanish = {StringsEnum.TITLE: "Experimentar",
           StringsEnum.CREATE: "Crear",
           StringsEnum.END: "Final",
           StringsEnum.CREATE_TT: "Crea un nuevo experimento",
           StringsEnum.END_TT: "Fin del experimento",
           StringsEnum.START_TT: "Comenzar experimento",
           StringsEnum.RESUME_TT: "Reanudar experimento",
           StringsEnum.PAUSE_TT: "Pausa experimento",
           StringsEnum.COND_NAME_SHADOW: "Nombre de condición opcional",
           }

# Chinese (simplified) strings
chinese = {StringsEnum.TITLE: "实验",
           StringsEnum.CREATE: "创建",
           StringsEnum.END: "结束",
           StringsEnum.CREATE_TT: "创建一个新实验",
           StringsEnum.END_TT: "结束实验",
           StringsEnum.START_TT: "开始实验",
           StringsEnum.RESUME_TT: "继续实验",
           StringsEnum.PAUSE_TT: "暂停实验",
           StringsEnum.COND_NAME_SHADOW: "可选条件名称",
           }

# Japanese strings
japanese = {StringsEnum.TITLE: "実験",
            StringsEnum.CREATE: "作成する",
            StringsEnum.END: "終わり",
            StringsEnum.CREATE_TT: "新しい実験を作成する",
            StringsEnum.END_TT: "実験を終了",
            StringsEnum.START_TT: "実験を始める",
            StringsEnum.RESUME_TT: "実験を再開",
            StringsEnum.PAUSE_TT: "実験を一時停止",
            StringsEnum.COND_NAME_SHADOW: "オプションの条件名",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
