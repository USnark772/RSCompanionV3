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


# Define enum like this.
class StringsEnum(Enum):
    CUSTOM_LABEL = auto()
    NHTSA_LABEL = auto()
    EBLIND_LABEL = auto()
    DCON_LABEL = auto()
    INF_LABEL = auto()
    CONFIG_TAB_LABEL = auto()
    CONFIG_LABEL = auto()
    UPLOAD_BUTTON_LABEL = auto()
    OPEN_DURATION_LABEL = auto()
    CLOSE_DURATION_LABEL = auto()
    DEBOUNCE_LABEL = auto()
    BUTTON_MODE_LABEL = auto()
    CONTROL_MODE_LABEL = auto()
    HOLD_VAL_LABEL = auto()
    CLICK_VAL_LABEL = auto()
    LENS_VAL_LABEL = auto()
    TRIAL_VAL_LABEL = auto()
    MANUAL_OPEN_LABEL = auto()
    MANUAL_CLOSE_LABEL = auto()
    CONFIG_TAB_TOOLTIP = auto()
    CONFIG_LABEL_TOOLTIP = auto()
    UPLOAD_BUTTON_TOOLTIP = auto()
    OPEN_DURATION_TOOLTIP = auto()
    CLOSE_DURATION_TOOLTIP = auto()
    DEBOUNCE_TOOLTIP = auto()
    BUTTON_MODE_TOOLTIP = auto()
    CONTROL_MODE_TOOLTIP = auto()
    HOLD_VAL_TOOLTIP = auto()
    CLICK_VAL_TOOLTIP = auto()
    LENS_VAL_TOOLTIP = auto()
    TRIAL_VAL_TOOLTIP = auto()
    MANUAL_OPEN_TOOLTIP = auto()
    MANUAL_CLOSE_TOOLTIP = auto()
    SAVE_HDR = auto()
    PLOT_NAME_OPEN_CLOSE = auto()
    GRAPH_TS = auto()


# Define languages like this.
english = {StringsEnum.CUSTOM_LABEL: "Custom",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "eBlindfold",
           StringsEnum.DCON_LABEL: "Direct Control",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.CONFIG_LABEL: "Current Configuration:",
           StringsEnum.UPLOAD_BUTTON_LABEL: "Upload Settings",
           StringsEnum.OPEN_DURATION_LABEL: "Open Duration",
           StringsEnum.CLOSE_DURATION_LABEL: "Close Duration",
           StringsEnum.DEBOUNCE_LABEL: "Debounce Time",
           StringsEnum.BUTTON_MODE_LABEL: "Button Mode",
           StringsEnum.CONTROL_MODE_LABEL: "Control Mode",
           StringsEnum.HOLD_VAL_LABEL: "Hold",
           StringsEnum.CLICK_VAL_LABEL: "Click",
           StringsEnum.LENS_VAL_LABEL: "Lens",
           StringsEnum.TRIAL_VAL_LABEL: "Trial",
           StringsEnum.MANUAL_OPEN_LABEL: "Open Lens",
           StringsEnum.MANUAL_CLOSE_LABEL: "Close Lens",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Show/Hide configuration tab",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
           StringsEnum.OPEN_DURATION_TOOLTIP: "Set lens open duration.",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "Set lens close duration.",
           StringsEnum.DEBOUNCE_TOOLTIP: "Set button debounce time.",
           StringsEnum.BUTTON_MODE_TOOLTIP: "Set button mode to Click or Hold.",
           StringsEnum.CONTROL_MODE_TOOLTIP: "Set control mode to Lens or Trial.",
           StringsEnum.HOLD_VAL_TOOLTIP: "Hold button to toggle lens.",
           StringsEnum.CLICK_VAL_TOOLTIP: "Click button to toggle lens.",
           StringsEnum.LENS_VAL_TOOLTIP: "Click button to toggle lens.",
           StringsEnum.TRIAL_VAL_TOOLTIP: "Click button to toggle trial.",
           StringsEnum.MANUAL_OPEN_TOOLTIP: "Manually open lens.",
           StringsEnum.MANUAL_CLOSE_TOOLTIP: "Manually close lens.",
           StringsEnum.SAVE_HDR: "timestamp, trial, open, close, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "Time Open/Close",
           StringsEnum.GRAPH_TS: "Timestamp",
           }

# TODO: Verify French
french = {StringsEnum.CUSTOM_LABEL: "Douane",
          StringsEnum.NHTSA_LABEL: "NHTSA",
          StringsEnum.EBLIND_LABEL: "ébandeau",
          StringsEnum.DCON_LABEL: "Contrôle direct",
          StringsEnum.INF_LABEL: "INF",
          StringsEnum.CONFIG_TAB_LABEL: "Configuration",
          StringsEnum.CONFIG_LABEL: "Configuration actuelle",
          StringsEnum.UPLOAD_BUTTON_LABEL: "Paramètres de téléchargement",
          StringsEnum.OPEN_DURATION_LABEL: "Durée d'ouverture",
          StringsEnum.CLOSE_DURATION_LABEL: "Durée de fermeture",
          StringsEnum.DEBOUNCE_LABEL: "Temps de rebond",
          StringsEnum.BUTTON_MODE_LABEL: "Mode bouton",
          StringsEnum.CONTROL_MODE_LABEL: "Mode de contrôle",
          StringsEnum.HOLD_VAL_LABEL: "Tenir",
          StringsEnum.CLICK_VAL_LABEL: "cliquer",
          StringsEnum.LENS_VAL_LABEL: "Objectif",
          StringsEnum.TRIAL_VAL_LABEL: "Procès",
          StringsEnum.MANUAL_OPEN_LABEL: "Ouvrir l'objectif",
          StringsEnum.MANUAL_CLOSE_LABEL: "Fermer l'objectif",
          StringsEnum.CONFIG_TAB_TOOLTIP: "Afficher/Masquer l'onglet de configuration",
          StringsEnum.CONFIG_LABEL_TOOLTIP: "Configuration actuelle de l'appareil",
          StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Télécharger la configuration actuelle sur l'appareil",
          StringsEnum.OPEN_DURATION_TOOLTIP: "Définir la durée d'ouverture de l'objectif.",
          StringsEnum.CLOSE_DURATION_TOOLTIP: "Réglez la durée de fermeture de l'objectif.",
          StringsEnum.DEBOUNCE_TOOLTIP: "Définir le temps de rebond du bouton.",
          StringsEnum.BUTTON_MODE_TOOLTIP: "Définissez le mode du bouton sur Cliquer ou Maintenir.",
          StringsEnum.CONTROL_MODE_TOOLTIP: "Réglez le mode de contrôle sur Objectif ou Essai.",
          StringsEnum.HOLD_VAL_TOOLTIP: "Maintenez le bouton pour basculer l'objectif.",
          StringsEnum.CLICK_VAL_TOOLTIP: "Cliquez sur le bouton pour basculer l'objectif.",
          StringsEnum.LENS_VAL_TOOLTIP: "Cliquez sur le bouton pour basculer l'objectif.",
          StringsEnum.TRIAL_VAL_TOOLTIP: "Cliquez sur le bouton pour basculer vers l'essai.",
          StringsEnum.MANUAL_OPEN_TOOLTIP: "Ouverture manuelle de l'objectif.",
          StringsEnum.MANUAL_CLOSE_TOOLTIP: "Fermeture manuelle de l'objectif.",
          StringsEnum.SAVE_HDR: "horodatage, procès, ouvert, Fermer, ",
          StringsEnum.PLOT_NAME_OPEN_CLOSE: "Heure d'ouverture/fermeture",
          StringsEnum.GRAPH_TS: "Horodatage",
          }

# TODO: translate languages
german = english

spanish = english

chinese = english

# Add defined languages to strings dictionary.
strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}
