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
from Resources.Strings.app_strings import company_name, app_name
from enum import Enum, auto


class StringsEnum(Enum):
    FILE = auto()
    LAST_DIR = auto()
    HELP = auto()
    ABOUT_APP = auto()
    ABOUT_COMPANY = auto()
    UPDATE_CHECK = auto()
    SHOW_LOG_WINDOW = auto()
    USE_CAMS = auto
    ATTACHED_CAMS = auto()
    SETTINGS = auto()
    DEBUG_MENU = auto()
    DEBUG = auto()
    WARNING = auto()
    LANG = auto()
    ENG = auto()
    FRE = auto()
    SPA = auto()


english = {StringsEnum.FILE: "File",
           StringsEnum.LAST_DIR: "Open last save location",
           StringsEnum.HELP: "Help",
           StringsEnum.ABOUT_APP: "About " + app_name,
           StringsEnum.ABOUT_COMPANY: "About " + company_name,
           StringsEnum.UPDATE_CHECK: "Check For Updates",
           StringsEnum.SHOW_LOG_WINDOW: "Show log window",
           StringsEnum.USE_CAMS: "Use cameras",
           StringsEnum.ATTACHED_CAMS: "Attached Camera",
           StringsEnum.SETTINGS: "Settings",
           StringsEnum.DEBUG_MENU: "Debug level",
           StringsEnum.DEBUG: "Debugging mode",
           StringsEnum.WARNING: "Normal mode",
           StringsEnum.LANG: "Language:",
           StringsEnum.ENG: "English",
           StringsEnum.FRE: "French",
           StringsEnum.SPA: "Spanish",
           }

# TODO: Verify French version
french = {StringsEnum.FILE: "Fichier",
          StringsEnum.LAST_DIR: "Ouvrir le dernier emplacement d'enregistrement",
          StringsEnum.HELP: "Assistance",
          StringsEnum.ABOUT_APP: "À propos de " + app_name,
          StringsEnum.ABOUT_COMPANY: "À propos de " + company_name,
          StringsEnum.UPDATE_CHECK: "Vérifier les mises à jour",
          StringsEnum.SHOW_LOG_WINDOW: "Afficher la fenêtre du journal",
          StringsEnum.USE_CAMS: "Utiliser des caméras",
          StringsEnum.ATTACHED_CAMS: "Caméra attachée",
          StringsEnum.SETTINGS: "Réglages",
          StringsEnum.DEBUG_MENU: "Niveau de débogage",
          StringsEnum.DEBUG: "Mode de débogage",
          StringsEnum.WARNING: "Mode normal",
          StringsEnum.LANG: "Langue:",
          StringsEnum.ENG: "Anglais",
          StringsEnum.FRE: "Français",
          StringsEnum.SPA: "Espagnol",
          }

# TODO: Verify Spanish version
spanish = {StringsEnum.FILE: "Expediente",
           StringsEnum.LAST_DIR: "Abrir la última ubicación de guardado",
           StringsEnum.HELP: "Ayuda",
           StringsEnum.ABOUT_APP: "Acerca de " + app_name,
           StringsEnum.ABOUT_COMPANY: "Acerca de " + company_name,
           StringsEnum.UPDATE_CHECK: "Buscar actualizaciones",
           StringsEnum.SHOW_LOG_WINDOW: "Mostrar ventana de registro",
           StringsEnum.USE_CAMS: "Usar cámaras",
           StringsEnum.ATTACHED_CAMS: "Cámara adjunta",
           StringsEnum.SETTINGS: "Configuraciones",
           StringsEnum.DEBUG_MENU: "Nivel de depuración",
           StringsEnum.DEBUG: "Modo de depuración",
           StringsEnum.WARNING: "Modo normal",
           StringsEnum.LANG: "Idioma:",
           StringsEnum.ENG: "Inglés",
           StringsEnum.FRE: "Francés",
           StringsEnum.SPA: "Español",
           }

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.SPA: spanish}
