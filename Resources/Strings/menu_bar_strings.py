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
    LAYOUT = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    TILED = auto()
    CASCADE = auto()
    DEBUG_MENU = auto()
    DEBUG = auto()
    WARNING = auto()
    LANG = auto()
    ENG = auto()
    FRE = auto()
    GER = auto()
    SPA = auto()
    CHI = auto()


lang_eng = "English"
lang_fre = "Français"
lang_ger = "Deutsche"
lang_spa = "Español"
lang_chi = "中文"


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
           StringsEnum.LAYOUT: "Window Layout",
           StringsEnum.HORIZONTAL: "Horizontal",
           StringsEnum.VERTICAL: "Vertical",
           StringsEnum.TILED: "Tiled",
           StringsEnum.CASCADE: "Cascade",
           StringsEnum.DEBUG_MENU: "Debug level",
           StringsEnum.DEBUG: "Debugging mode",
           StringsEnum.WARNING: "Normal mode",
           StringsEnum.LANG: "Language:",
           StringsEnum.ENG: lang_eng,
           StringsEnum.FRE: lang_fre,
           StringsEnum.GER: lang_ger,
           StringsEnum.SPA: lang_spa,
           StringsEnum.CHI: lang_chi,
           }

# TODO: Verify French
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
          StringsEnum.LAYOUT: "Disposition des fenêtres",
          StringsEnum.HORIZONTAL: "Horizontal",
          StringsEnum.VERTICAL: "Vertical",
          StringsEnum.TILED: "Carrelé",
          StringsEnum.CASCADE: "Cascade",
          StringsEnum.DEBUG_MENU: "Niveau de débogage",
          StringsEnum.DEBUG: "Mode de débogage",
          StringsEnum.WARNING: "Mode normal",
          StringsEnum.LANG: "Langue:",
          StringsEnum.ENG: lang_eng,
          StringsEnum.FRE: lang_fre,
          StringsEnum.GER: lang_ger,
          StringsEnum.SPA: lang_spa,
          StringsEnum.CHI: lang_chi,
          }

# TODO: Verify German
german = {StringsEnum.FILE: "Datei",
          StringsEnum.LAST_DIR: "Öffnen Sie den letzten Speicherort",
          StringsEnum.HELP: "Hilfe",
          StringsEnum.ABOUT_APP: "Über " + app_name,
          StringsEnum.ABOUT_COMPANY: "Über " + company_name,
          StringsEnum.UPDATE_CHECK: "Auf Updates prüfen",
          StringsEnum.SHOW_LOG_WINDOW: "Protokollfenster anzeigen",
          StringsEnum.USE_CAMS: "Verwenden Sie Kameras",
          StringsEnum.ATTACHED_CAMS: "Angebrachte Kamera",
          StringsEnum.SETTINGS: "die Einstellungen",
          StringsEnum.LAYOUT: "Fensterlayout",
          StringsEnum.HORIZONTAL: "Horizontal",
          StringsEnum.VERTICAL: "Vertikale",
          StringsEnum.TILED: "Gefliest",
          StringsEnum.CASCADE: "Kaskade",
          StringsEnum.DEBUG_MENU: "Debug-Ebene",
          StringsEnum.DEBUG: "Debugging-Modus",
          StringsEnum.WARNING: "Normaler Modus",
          StringsEnum.LANG: "Sprache:",
          StringsEnum.ENG: lang_eng,
          StringsEnum.FRE: lang_fre,
          StringsEnum.GER: lang_ger,
          StringsEnum.SPA: lang_spa,
          StringsEnum.CHI: lang_chi,
          }

# TODO: Verify Spanish
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
           StringsEnum.LAYOUT: "Diseño de la ventana",
           StringsEnum.HORIZONTAL: "Horizontal",
           StringsEnum.VERTICAL: "Vertical",
           StringsEnum.TILED: "Embaldosado",
           StringsEnum.CASCADE: "Cascada",
           StringsEnum.DEBUG_MENU: "Nivel de depuración",
           StringsEnum.DEBUG: "Modo de depuración",
           StringsEnum.WARNING: "Modo normal",
           StringsEnum.LANG: "Idioma:",
           StringsEnum.ENG: lang_eng,
           StringsEnum.FRE: lang_fre,
           StringsEnum.GER: lang_ger,
           StringsEnum.SPA: lang_spa,
           StringsEnum.CHI: lang_chi,
           }

# TODO: Verify Chinese (simplified)
chinese = {StringsEnum.FILE: "文件",
           StringsEnum.LAST_DIR: "打开上一个保存位置",
           StringsEnum.HELP: "帮帮",
           StringsEnum.ABOUT_APP: "关于 " + app_name,
           StringsEnum.ABOUT_COMPANY: "关于 " + company_name,
           StringsEnum.UPDATE_CHECK: "检查更新",
           StringsEnum.SHOW_LOG_WINDOW: "显示日志窗口",
           StringsEnum.USE_CAMS: "使用相机",
           StringsEnum.ATTACHED_CAMS: "附属相机",
           StringsEnum.SETTINGS: "应用程式设定",
           StringsEnum.LAYOUT: "窗口布局",
           StringsEnum.HORIZONTAL: "卧式",
           StringsEnum.VERTICAL: "垂直",
           StringsEnum.TILED: "平铺",
           StringsEnum.CASCADE: "级联",
           StringsEnum.DEBUG_MENU: "调试级别",
           StringsEnum.DEBUG: "调试模式",
           StringsEnum.WARNING: "正常模式",
           StringsEnum.LANG: "语言:",
           StringsEnum.ENG: lang_eng,
           StringsEnum.FRE: lang_fre,
           StringsEnum.GER: lang_ger,
           StringsEnum.SPA: lang_spa,
           StringsEnum.CHI: lang_chi,
           }

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}
