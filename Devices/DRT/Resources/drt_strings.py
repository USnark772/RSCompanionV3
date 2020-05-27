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
    CONFIG_TAB_TOOLTIP = auto()
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
           StringsEnum.CONFIG_TAB_TOOLTIP: "Show/Hide configuration tab",
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
           StringsEnum.GRAPH_TS: "Timestamp",
           }

# TODO: Verify translations
# Dutch strings
lower_isi_dut = "Lagere ISI"
upper_isi_dut = "Bovenste ISI"
dutch = {StringsEnum.CUSTOM_LABEL: "Op maat",
         StringsEnum.ISO_LABEL: iso,
         StringsEnum.CONFIG_TAB_LABEL: "Configuratie",
         StringsEnum.CONFIG_LABEL: "Huidige configuratie:",
         StringsEnum.ISO_BUTTON_LABEL: iso,
         StringsEnum.UPLOAD_BUTTON_LABEL: "Upload instellingen",
         StringsEnum.DURATION_LABEL: "Stim Duur",
         StringsEnum.INTENSITY_LABEL: "Stim-intensiteit",
         StringsEnum.UPPER_ISI_LABEL: upper_isi_dut,
         StringsEnum.LOWER_ISI_LABEL: lower_isi_dut,
         StringsEnum.CONFIG_TAB_TOOLTIP: "Configuratietabblad weergeven/verbergen",
         StringsEnum.CONFIG_LABEL_TOOLTIP: "Huidige apparaatconfiguratie",
         StringsEnum.ISO_BUTTON_TOOLTIP: "Stel het apparaat in op de ISO-standaard",
         StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload de huidige configuratie naar het apparaat",
         StringsEnum.DURATION_TOOLTIP: "Milliseconden. Bereik: " + str(defs.duration_min) + "-" + str(
             defs.duration_max),
         StringsEnum.INTENSITY_TOOLTIP: "Intensity of the stimulus",
         StringsEnum.UPPER_ISI_TOOLTIP: "Milliseconden. Bereik: " + lower_isi_dut + "-" + str(defs.ISI_max),
         StringsEnum.LOWER_ISI_TOOLTIP: "Milliseconden. Bereik: " + str(defs.ISI_min) + "-" + upper_isi_dut,
         StringsEnum.SAVE_HDR: "tijdstempel, onderzoek #, klikken, milliseconden vanaf het begin van het experiment,"
                               " reactietijd",
         StringsEnum.PLOT_NAME_RT: "Reactietijd",
         StringsEnum.PLOT_NAME_CLICKS: "klikken",
         StringsEnum.GRAPH_TS: "tijdstempel",
         }

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
          StringsEnum.CONFIG_TAB_TOOLTIP: "Afficher/masquer l'onglet de configuration",
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
          StringsEnum.GRAPH_TS: "Horodatage",
          }

# German strings
lower_isi_ger = "Niedriger ISI"
upper_isi_ger = "Obere ISI"
german = {StringsEnum.CUSTOM_LABEL: "Benutzerdefiniert",
          StringsEnum.ISO_LABEL: iso,
          StringsEnum.CONFIG_TAB_LABEL: "Konfiguration",
          StringsEnum.CONFIG_LABEL: "Aktuelle Konfiguration:",
          StringsEnum.ISO_BUTTON_LABEL: iso,
          StringsEnum.UPLOAD_BUTTON_LABEL: "Einstellungen hochladen",
          StringsEnum.DURATION_LABEL: "Reizdauer",
          StringsEnum.INTENSITY_LABEL: "Reizintensität",
          StringsEnum.UPPER_ISI_LABEL: upper_isi_ger,
          StringsEnum.LOWER_ISI_LABEL: lower_isi_ger,
          StringsEnum.CONFIG_TAB_TOOLTIP: "Registerkarte Konfiguration anzeigen/ausblenden",
          StringsEnum.CONFIG_LABEL_TOOLTIP: "Aktuelle Gerätekonfiguration",
          StringsEnum.ISO_BUTTON_TOOLTIP: "Gerät auf ISO-Standard einstellen",
          StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Laden Sie die aktuelle Konfiguration auf das Gerät hoch",
          StringsEnum.DURATION_TOOLTIP: "Millisekunden. Angebot: " + str(defs.duration_min) + "-" + str(
              defs.duration_max),
          StringsEnum.INTENSITY_TOOLTIP: "Intensität des Reizes",
          StringsEnum.UPPER_ISI_TOOLTIP: "Millisekunden. Angebot: " + lower_isi_ger + "-" + str(defs.ISI_max),
          StringsEnum.LOWER_ISI_TOOLTIP: "Millisekunden. Angebot: " + str(defs.ISI_min) + "-" + upper_isi_ger,
          StringsEnum.SAVE_HDR: "Zeitstempel, Sonde #, Klicks, Millisekunden nach Beginn des Experiments,"
                                " Reaktionszeit",
          StringsEnum.PLOT_NAME_RT: "Reaktionszeit",
          StringsEnum.PLOT_NAME_CLICKS: "Klicks",
          StringsEnum.GRAPH_TS: "Zeitstempel",
          }

# Russian strings
lower_isi_rus = "ниже ISI"
upper_isi_rus = "верхний ISI"
russian = {StringsEnum.CUSTOM_LABEL: "изготовленный на заказ",
           StringsEnum.ISO_LABEL: iso,
           StringsEnum.CONFIG_TAB_LABEL: "конфигурация",
           StringsEnum.CONFIG_LABEL: "Текущая конфигурация:",
           StringsEnum.ISO_BUTTON_LABEL: iso,
           StringsEnum.UPLOAD_BUTTON_LABEL: "Загрузить настройки",
           StringsEnum.DURATION_LABEL: "Стимул Продолжительность",
           StringsEnum.INTENSITY_LABEL: "Интенсивность стимула",
           StringsEnum.UPPER_ISI_LABEL: upper_isi_rus,
           StringsEnum.LOWER_ISI_LABEL: lower_isi_rus,
           StringsEnum.CONFIG_TAB_TOOLTIP: "Показать/Скрыть вкладку конфигурации",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Текущая конфигурация устройства",
           StringsEnum.ISO_BUTTON_TOOLTIP: "Установить устройство на стандарт ISO",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Загрузить текущую конфигурацию на устройство",
           StringsEnum.DURATION_TOOLTIP: "миллисекунды. Спектр: " + str(defs.duration_min) + "-" + str(
               defs.duration_max),
           StringsEnum.INTENSITY_TOOLTIP: "Intensity of the stimulus",
           StringsEnum.UPPER_ISI_TOOLTIP: "миллисекунды. Спектр: " + lower_isi_rus + "-" + str(defs.ISI_max),
           StringsEnum.LOWER_ISI_TOOLTIP: "миллисекунды. Спектр: " + str(defs.ISI_min) + "-" + upper_isi_rus,
           StringsEnum.SAVE_HDR: "отметка времени, проба #, щелчки, миллисекунды с начала эксперимента, время отклика",
           StringsEnum.PLOT_NAME_RT: "время отклика",
           StringsEnum.PLOT_NAME_CLICKS: "щелчки",
           StringsEnum.GRAPH_TS: "отметка времени",
           }

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
           StringsEnum.CONFIG_TAB_TOOLTIP: "Mostrar/Ocultar pestaña de configuración",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Configuración actual del dispositivo",
           StringsEnum.ISO_BUTTON_TOOLTIP: "Establecer dispositivo a estándar ISO",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Subir la configuración actual al dispositivo",
           StringsEnum.DURATION_TOOLTIP: "Milisegundos. Alcance: " + str(defs.duration_min) + "-" + str(
               defs.duration_max),
           StringsEnum.INTENSITY_TOOLTIP: "Intensidad del estímulo",
           StringsEnum.UPPER_ISI_TOOLTIP: "Milisegundos. Alcance: " + lower_isi_spa + "-" + str(defs.ISI_max),
           StringsEnum.LOWER_ISI_TOOLTIP: "Milisegundos. Alcance: " + str(defs.ISI_min) + "-" + upper_isi_spa,
           StringsEnum.SAVE_HDR: "marca de tiempo, Investigacion #, clics,"
                                 " milisegundos desde el inicio del experimento, tiempo de respuesta",
           StringsEnum.PLOT_NAME_RT: "Tiempo de respuesta",
           StringsEnum.PLOT_NAME_CLICKS: "Clics",
           StringsEnum.GRAPH_TS: "marca de tiempo",
           }

# Chinese (simplified) strings
lower_isi_chi = "较低的ISI"
upper_isi_chi = "上ISI"
chinese = {StringsEnum.CUSTOM_LABEL: "自订",
           StringsEnum.ISO_LABEL: iso,
           StringsEnum.CONFIG_TAB_LABEL: "组态",
           StringsEnum.CONFIG_LABEL: "当前配置:",
           StringsEnum.ISO_BUTTON_LABEL: iso,
           StringsEnum.UPLOAD_BUTTON_LABEL: "上载设定",
           StringsEnum.DURATION_LABEL: "刺激持续时间",
           StringsEnum.INTENSITY_LABEL: "刺激强度",
           StringsEnum.UPPER_ISI_LABEL: upper_isi_chi,
           StringsEnum.LOWER_ISI_LABEL: lower_isi_chi,
           StringsEnum.CONFIG_TAB_TOOLTIP: "显示/隐藏配置选项卡",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "当前设备配置",
           StringsEnum.ISO_BUTTON_TOOLTIP: "将设备设置为ISO标准",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "将当前配置上传到设备",
           StringsEnum.DURATION_TOOLTIP: "毫秒。 范围: " + str(defs.duration_min) + "-" + str(
               defs.duration_max),
           StringsEnum.INTENSITY_TOOLTIP: "刺激强度",
           StringsEnum.UPPER_ISI_TOOLTIP: "毫秒。 范围: " + lower_isi_chi + "-" + str(defs.ISI_max),
           StringsEnum.LOWER_ISI_TOOLTIP: "毫秒。 范围: " + str(defs.ISI_min) + "-" + upper_isi_chi,
           StringsEnum.SAVE_HDR: "时间戳记, 探测 #, 点击次数, 从实验开始算起的毫秒数, 响应时间",
           StringsEnum.PLOT_NAME_RT: "响应时间",
           StringsEnum.PLOT_NAME_CLICKS: "点击次数",
           StringsEnum.GRAPH_TS: "时间戳记",
           }

# Japanese strings
lower_isi_jpn = "下 ISI"
upper_isi_jpn = "上 ISI"
japanese = {StringsEnum.CUSTOM_LABEL: "カスタム",
            StringsEnum.ISO_LABEL: iso,
            StringsEnum.CONFIG_TAB_LABEL: "構成",
            StringsEnum.CONFIG_LABEL: "現在の構成:",
            StringsEnum.ISO_BUTTON_LABEL: iso,
            StringsEnum.UPLOAD_BUTTON_LABEL: "アップロード設定",
            StringsEnum.DURATION_LABEL: "刺激持続時間",
            StringsEnum.INTENSITY_LABEL: "刺激強度",
            StringsEnum.UPPER_ISI_LABEL: upper_isi_jpn,
            StringsEnum.LOWER_ISI_LABEL: lower_isi_jpn,
            StringsEnum.CONFIG_TAB_TOOLTIP: "構成タブの表示/非表示",
            StringsEnum.CONFIG_LABEL_TOOLTIP: "現在のデバイス構成",
            StringsEnum.ISO_BUTTON_TOOLTIP: "デバイスをISO標準に設定",
            StringsEnum.UPLOAD_BUTTON_TOOLTIP: "現在の構成をデバイスにアップロード",
            StringsEnum.DURATION_TOOLTIP: "ミリ秒。 範囲: " + str(defs.duration_min) + "-" + str(
                defs.duration_max),
            StringsEnum.INTENSITY_TOOLTIP: "刺激の強さ",
            StringsEnum.UPPER_ISI_TOOLTIP: "ミリ秒。 範囲: " + lower_isi_jpn + "-" + str(defs.ISI_max),
            StringsEnum.LOWER_ISI_TOOLTIP: "ミリ秒。 範囲: " + str(defs.ISI_min) + "-" + upper_isi_jpn,
            StringsEnum.SAVE_HDR: "タイムスタンプ, 調査 #, クリック, 実験開始からミリ秒, 反応時間",
            StringsEnum.PLOT_NAME_RT: "反応時間",
            StringsEnum.PLOT_NAME_CLICKS: "クリック",
            StringsEnum.GRAPH_TS: "タイムスタンプ",
            }

strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
