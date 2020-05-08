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

""" English version strings for the DRT code. """

from Devices.DRT.Model import drt_defs as defs
from enum import Enum, auto
from Model.app_defs import LangEnum


class StringsEnum(Enum):
    CUSTOM_LABEL = auto()
    ISO_LABEL = auto()
    CONFIG_TAB_LABEL = auto()
    CONFIG_LABEL = auto()
    ISO_BUTTON_LABEL = auto()
    UPLOAD_BUTTON_LABEL = auto()
    DURATION_LABEL = auto()
    INTENSITY_LABEL = auto()
    UPPER_ISI_LABEL = auto()
    LOWER_ISI_LABEL = auto()
    CONFIG_LABEL_TOOLTIP = auto()
    ISO_BUTTON_TOOLTIP = auto()
    UPLOAD_BUTTON_TOOLTIP = auto()
    DURATION_TOOLTIP = auto()
    INTENSITY_TOOLTIP = auto()
    UPPER_ISI_TOOLTIP = auto()
    LOWER_ISI_TOOLTIP = auto()
    SAVE_HDR = auto()
    PLOT_NAME_RT = auto()
    PLOT_NAME_CLICKS = auto()
    GRAPH_TS = auto()


# English strings
iso = "ISO"
lower_isi_eng = "Lower ISI"
upper_isi_eng = "Upper ISI"
english = {StringsEnum.CUSTOM_LABEL: "Custom",
           StringsEnum.ISO_LABEL: iso,
           StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.CONFIG_LABEL: "Current configuration:",
           StringsEnum.ISO_BUTTON_LABEL: iso,
           StringsEnum.UPLOAD_BUTTON_LABEL: "Upload settings",
           StringsEnum.DURATION_LABEL: "Stim Duration",
           StringsEnum.INTENSITY_LABEL: "Stim Intensity",
           StringsEnum.UPPER_ISI_LABEL: upper_isi_eng,
           StringsEnum.LOWER_ISI_LABEL: lower_isi_eng,
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
           StringsEnum.ISO_BUTTON_TOOLTIP: "Set device to ISO standard",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
           StringsEnum.DURATION_TOOLTIP: "Milliseconds. Range: " + str(defs.duration_min) + "-" + str(
               defs.duration_max),
           StringsEnum.INTENSITY_TOOLTIP: "Intensity of the stimulus",
           StringsEnum.UPPER_ISI_TOOLTIP: "Milliseconds. Range: " + lower_isi_eng + "-" + str(defs.ISI_max),
           StringsEnum.LOWER_ISI_TOOLTIP: "Milliseconds. Range: " + str(defs.ISI_min) + "-" + upper_isi_eng,
           StringsEnum.SAVE_HDR: "timestamp, probe #, clicks, milliseconds from experiment start, response time",
           StringsEnum.PLOT_NAME_RT: "Response time",
           StringsEnum.PLOT_NAME_CLICKS: "Clicks",
           }

# TODO: Verify French version
# French strings
lower_isi_fre = "Inférieur ISI"
upper_isi_fre = "Supérieur ISI"
french = {StringsEnum.CUSTOM_LABEL: "Douane",
          StringsEnum.ISO_LABEL: iso,
          StringsEnum.CONFIG_TAB_LABEL: "Configuration",
          StringsEnum.CONFIG_LABEL: "Configuration actuelle:",
          StringsEnum.ISO_BUTTON_LABEL: iso,
          StringsEnum.UPLOAD_BUTTON_LABEL: "Importer les paramètres",
          StringsEnum.DURATION_LABEL: "Durée de stim",
          StringsEnum.INTENSITY_LABEL: "Intensité de stim",
          StringsEnum.UPPER_ISI_LABEL: upper_isi_fre,
          StringsEnum.LOWER_ISI_LABEL: lower_isi_fre,
          StringsEnum.CONFIG_LABEL_TOOLTIP: "Configuration actuelle de l'appareil",
          StringsEnum.ISO_BUTTON_TOOLTIP: "Réglez l'appareil sur la norme ISO",
          StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Télécharger la configuration actuelle sur l'appareil",
          StringsEnum.DURATION_TOOLTIP: "Millisecondes. Intervalle: " + str(defs.duration_min) + "-" +
                                        str(defs.duration_max),
          StringsEnum.INTENSITY_TOOLTIP: "Intensité du stim",
          StringsEnum.UPPER_ISI_TOOLTIP: "Millisecondes. Intervalle: " + lower_isi_fre + "-" + str(defs.ISI_max),
          StringsEnum.LOWER_ISI_TOOLTIP: "Millisecondes. Intervalle: " + str(defs.ISI_min) + "-" + upper_isi_fre,
          StringsEnum.SAVE_HDR: "horodatage, sonde #, clics, millisecondes depuis le début de l'expérience, "
                                "temp de réponse",
          StringsEnum.PLOT_NAME_RT: "Temp de réponse",
          StringsEnum.PLOT_NAME_CLICKS: "Clics",
          }

# TODO: verify Spanish version
# Spanish strings
lower_isi_spa = "Inferior ISI"
upper_isi_spa = "Superior ISI"
spanish = {StringsEnum.CUSTOM_LABEL: "Personalizado",
           StringsEnum.ISO_LABEL: iso,
           StringsEnum.CONFIG_TAB_LABEL: "Configuración",
           StringsEnum.CONFIG_LABEL: "Configuración actual:",
           StringsEnum.ISO_BUTTON_LABEL: iso,
           StringsEnum.UPLOAD_BUTTON_LABEL: "Subir configuraciones",
           StringsEnum.DURATION_LABEL: "Duración de estím",
           StringsEnum.INTENSITY_LABEL: "Intensidad de estím",
           StringsEnum.UPPER_ISI_LABEL: upper_isi_spa,
           StringsEnum.LOWER_ISI_LABEL: lower_isi_spa,
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Configuración actual del dispositivo",
           StringsEnum.ISO_BUTTON_TOOLTIP: "Establecer dispositivo a estándar ISO",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Subir la configuración actual al dispositivo",
           StringsEnum.DURATION_TOOLTIP: "Milisegundos. Alcance: " + str(defs.duration_min) + "-" + str(
               defs.duration_max),
           StringsEnum.INTENSITY_TOOLTIP: "Intensidad del estímulo",
           StringsEnum.UPPER_ISI_TOOLTIP: "Milisegundos. Alcance: " + lower_isi_eng + "-" + str(defs.ISI_max),
           StringsEnum.LOWER_ISI_TOOLTIP: "Milisegundos. Alcance: " + str(defs.ISI_min) + "-" + upper_isi_eng,
           StringsEnum.SAVE_HDR: "marca de tiempo, Investigacion #, clics,"
                                 " milisegundos desde el inicio del experimento, tiempo de respuesta",
           StringsEnum.PLOT_NAME_RT: "Tiempo de respuesta",
           StringsEnum.PLOT_NAME_CLICKS: "Clics",
           }

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.SPA: spanish}
