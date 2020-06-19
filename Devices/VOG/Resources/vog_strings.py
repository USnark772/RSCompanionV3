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
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "Milliseconds",
           StringsEnum.GRAPH_TS: "Timestamp",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.CUSTOM_LABEL: "Op maat",
         StringsEnum.NHTSA_LABEL: "NHTSA",
         StringsEnum.EBLIND_LABEL: "eBlinddoek",
         StringsEnum.DCON_LABEL: "Directe controle",
         StringsEnum.INF_LABEL: "INF",
         StringsEnum.CONFIG_TAB_LABEL: "Configuratie",
         StringsEnum.CONFIG_LABEL: "Huidige configuratie:",
         StringsEnum.UPLOAD_BUTTON_LABEL: "Upload instellingen",
         StringsEnum.OPEN_DURATION_LABEL: "Open Duur",
         StringsEnum.CLOSE_DURATION_LABEL: "Sluitingsduur",
         StringsEnum.DEBOUNCE_LABEL: "Debouncetijd",
         StringsEnum.BUTTON_MODE_LABEL: "Knopmodus",
         StringsEnum.CONTROL_MODE_LABEL: "Besturingsmodus",
         StringsEnum.HOLD_VAL_LABEL: "Houden",
         StringsEnum.CLICK_VAL_LABEL: "Klik",
         StringsEnum.LENS_VAL_LABEL: "Lens",
         StringsEnum.TRIAL_VAL_LABEL: "Proef",
         StringsEnum.MANUAL_OPEN_LABEL: "Open Lens",
         StringsEnum.MANUAL_CLOSE_LABEL: "Lens sluiten",
         StringsEnum.CONFIG_TAB_TOOLTIP: "Configuratietabblad weergeven/verbergen",
         StringsEnum.CONFIG_LABEL_TOOLTIP: "Huidige apparaatconfiguratie",
         StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload de huidige configuratie naar het apparaat",
         StringsEnum.OPEN_DURATION_TOOLTIP: "Stel de open duur van de lens in.",
         StringsEnum.CLOSE_DURATION_TOOLTIP: "Stel de sluitingsduur van de lens in.",
         StringsEnum.DEBOUNCE_TOOLTIP: "Stel de debouncetijd van de knop in.",
         StringsEnum.BUTTON_MODE_TOOLTIP: "Stel de knopmodus in om te Klikken of vast te Houden.",
         StringsEnum.CONTROL_MODE_TOOLTIP: "Stel de bedieningsmodus in op Lens of Proef.",
         StringsEnum.HOLD_VAL_TOOLTIP: "Houd de knop ingedrukt om de lens te wisselen.",
         StringsEnum.CLICK_VAL_TOOLTIP: "Klik op de knop om de lens te wisselen.",
         StringsEnum.LENS_VAL_TOOLTIP: "Klik op de knop om de lens te wisselen.",
         StringsEnum.TRIAL_VAL_TOOLTIP: "Klik op de knop om de proefversie te wisselen.",
         StringsEnum.MANUAL_OPEN_TOOLTIP: "Handmatig geopende lens.",
         StringsEnum.MANUAL_CLOSE_TOOLTIP: "Lens handmatig sluiten.",
         StringsEnum.SAVE_HDR: "tijdstempel, proef, open, sluiten, ",
         StringsEnum.PLOT_NAME_OPEN_CLOSE: "Milliseconden",
         StringsEnum.GRAPH_TS: "tijdstempel",
         }

# French strings
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
          StringsEnum.MANUAL_OPEN_LABEL: "Ouvrir",
          StringsEnum.MANUAL_CLOSE_LABEL: "Fermer",
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
          StringsEnum.PLOT_NAME_OPEN_CLOSE: "Millisecondes",
          StringsEnum.GRAPH_TS: "Horodatage",
          }

# German strings
german = {StringsEnum.CUSTOM_LABEL: "Benutzerdefiniert",
          StringsEnum.NHTSA_LABEL: "NHTSA",
          StringsEnum.EBLIND_LABEL: "eAugenbinde",
          StringsEnum.DCON_LABEL: "Direkte Kontrolle",
          StringsEnum.INF_LABEL: "INF",
          StringsEnum.CONFIG_TAB_LABEL: "Konfiguration",
          StringsEnum.CONFIG_LABEL: "Aktuelle Konfiguration:",
          StringsEnum.UPLOAD_BUTTON_LABEL: "Einstellungen hochladen",
          StringsEnum.OPEN_DURATION_LABEL: "offene Dauer",
          StringsEnum.CLOSE_DURATION_LABEL: "Dauer schließen",
          StringsEnum.DEBOUNCE_LABEL: "Entprellzeit",
          StringsEnum.BUTTON_MODE_LABEL: "Tastenmodus",
          StringsEnum.CONTROL_MODE_LABEL: "Steuermodus",
          StringsEnum.HOLD_VAL_LABEL: "Halten",
          StringsEnum.CLICK_VAL_LABEL: "Klicken",
          StringsEnum.LENS_VAL_LABEL: "Linse",
          StringsEnum.TRIAL_VAL_LABEL: "Versuch",
          StringsEnum.MANUAL_OPEN_LABEL: "öffnen",
          StringsEnum.MANUAL_CLOSE_LABEL: "schließen",
          StringsEnum.CONFIG_TAB_TOOLTIP: "Registerkarte Konfiguration anzeigen/ausblenden",
          StringsEnum.CONFIG_LABEL_TOOLTIP: "Aktuelle Gerätekonfiguration",
          StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Laden Sie die aktuelle Konfiguration auf das Gerät hoch",
          StringsEnum.OPEN_DURATION_TOOLTIP: "Stellen Sie die offene Dauer des Linse ein.",
          StringsEnum.CLOSE_DURATION_TOOLTIP: "Stellen Sie die Dauer schließen des Linse ein.",
          StringsEnum.DEBOUNCE_TOOLTIP: "Stellen Sie die Entprellzeit der Schaltfläche ein.",
          StringsEnum.BUTTON_MODE_TOOLTIP: "Stellen Sie den Tastenmodus auf Klicken oder Halten ein.",
          StringsEnum.CONTROL_MODE_TOOLTIP: "Stellen Sie den Steuermodus auf Linse oder Test.",
          StringsEnum.HOLD_VAL_TOOLTIP: "Halten Sie die Taste gedrückt, um das Objektiv umzuschalten.",
          StringsEnum.CLICK_VAL_TOOLTIP: "Klicken Sie auf die Schaltfläche, um das Linse umzuschalten.",
          StringsEnum.LENS_VAL_TOOLTIP: "Klicken Sie auf die Schaltfläche, um das Linse umzuschalten.",
          StringsEnum.TRIAL_VAL_TOOLTIP: "Click the button to switch the trial version.",
          StringsEnum.MANUAL_OPEN_TOOLTIP: "Linse manuell öffnen.",
          StringsEnum.MANUAL_CLOSE_TOOLTIP: "Linse manuell schließen.",
          StringsEnum.SAVE_HDR: "Zeitstempel, Versuch, öffnen, schließen, ",
          StringsEnum.PLOT_NAME_OPEN_CLOSE: "Millisekunden",
          StringsEnum.GRAPH_TS: "Zeitstempel",
          }

# Russian strings
russian = {StringsEnum.CUSTOM_LABEL: "изготовленный на заказ",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "повязка на глазах",
           StringsEnum.DCON_LABEL: "Прямой контроль",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "конфигурация",
           StringsEnum.CONFIG_LABEL: "Текущая конфигурация:",
           StringsEnum.UPLOAD_BUTTON_LABEL: "Настройки загрузки",
           StringsEnum.OPEN_DURATION_LABEL: "Открытая продолжительность",
           StringsEnum.CLOSE_DURATION_LABEL: "Длительность закрытия",
           StringsEnum.DEBOUNCE_LABEL: "Время отката",
           StringsEnum.BUTTON_MODE_LABEL: "Режим кнопки",
           StringsEnum.CONTROL_MODE_LABEL: "Режим управления",
           StringsEnum.HOLD_VAL_LABEL: "Держать",
           StringsEnum.CLICK_VAL_LABEL: "щелчок",
           StringsEnum.LENS_VAL_LABEL: "объектив",
           StringsEnum.TRIAL_VAL_LABEL: "пробный",
           StringsEnum.MANUAL_OPEN_LABEL: "Открытая линза",
           StringsEnum.MANUAL_CLOSE_LABEL: "Закрыть объектив",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Показать/Скрыть вкладку конфигурации",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Текущая конфигурация устройства",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Загрузить текущую конфигурацию на устройство",
           StringsEnum.OPEN_DURATION_TOOLTIP: "Установите длительность открытия объектива.",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "Set the length of time the lens closes.",
           StringsEnum.DEBOUNCE_TOOLTIP: "Установите время отскока кнопки.",
           StringsEnum.BUTTON_MODE_TOOLTIP: "Установите режим кнопки, чтобы нажать или удерживать.",
           StringsEnum.CONTROL_MODE_TOOLTIP: "Установите режим управления на объектив или пробную версию.",
           StringsEnum.HOLD_VAL_TOOLTIP: "Удерживайте кнопку для переключения объектива.",
           StringsEnum.CLICK_VAL_TOOLTIP: "Нажмите кнопку, чтобы переключить объектив.",
           StringsEnum.LENS_VAL_TOOLTIP: "Нажмите кнопку, чтобы переключить объектив.",
           StringsEnum.TRIAL_VAL_TOOLTIP: "Нажмите кнопку, чтобы включить пробную версию.",
           StringsEnum.MANUAL_OPEN_TOOLTIP: "Вручную откройте объектив.",
           StringsEnum.MANUAL_CLOSE_TOOLTIP: "Вручную закройте объектив.",
           StringsEnum.SAVE_HDR: "отметка времени, пробный, открытый, закрывать, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "миллисекунды",
           StringsEnum.GRAPH_TS: "отметка времени",
           }

# Spanish strings
spanish = {StringsEnum.CUSTOM_LABEL: "Personalizado",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "eVenda",
           StringsEnum.DCON_LABEL: "Control directo",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "Configuración",
           StringsEnum.CONFIG_LABEL: "Configuración actual:",
           StringsEnum.UPLOAD_BUTTON_LABEL: "Configuración de carga",
           StringsEnum.OPEN_DURATION_LABEL: "Duración abierta",
           StringsEnum.CLOSE_DURATION_LABEL: "Duración de cierre",
           StringsEnum.DEBOUNCE_LABEL: "Tiempo de rebote",
           StringsEnum.BUTTON_MODE_LABEL: "Modo de botón",
           StringsEnum.CONTROL_MODE_LABEL: "Modo de control",
           StringsEnum.HOLD_VAL_LABEL: "Sostener",
           StringsEnum.CLICK_VAL_LABEL: "Hacer clic",
           StringsEnum.LENS_VAL_LABEL: "Lente",
           StringsEnum.TRIAL_VAL_LABEL: "Juicio",
           StringsEnum.MANUAL_OPEN_LABEL: "abierta",
           StringsEnum.MANUAL_CLOSE_LABEL: "cerrada",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Mostrar/Ocultar pestaña de configuración",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Configuración actual del dispositivo",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Subir la configuración actual al dispositivo",
           StringsEnum.OPEN_DURATION_TOOLTIP: "Establecer la duración de la lente abierta.",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "Establezca la duración del cierre de la lente.",
           StringsEnum.DEBOUNCE_TOOLTIP: "Ajuste el tiempo de rebote del botón.",
           StringsEnum.BUTTON_MODE_TOOLTIP: "Establezca el modo de botón en Hacer clic o Mantener.",
           StringsEnum.CONTROL_MODE_TOOLTIP: "Establezca el modo de control en Lente o Prueba.",
           StringsEnum.HOLD_VAL_TOOLTIP: "Mantenga presionado el botón para alternar la lente.",
           StringsEnum.CLICK_VAL_TOOLTIP: "Haga clic en el botón para alternar la lente.",
           StringsEnum.LENS_VAL_TOOLTIP: "Haga clic en el botón para alternar la lente.",
           StringsEnum.TRIAL_VAL_TOOLTIP: "Haga clic en el botón para alternar de prueba.",
           StringsEnum.MANUAL_OPEN_TOOLTIP: "Lente abierta manualmente.",
           StringsEnum.MANUAL_CLOSE_TOOLTIP: "Lente manualmente cerrado.",
           StringsEnum.SAVE_HDR: "marca de tiempo, juicio, abierto, cerca, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "Milisegundos",
           StringsEnum.GRAPH_TS: "marca de tiempo",
           }

# Chinese strings
chinese = {StringsEnum.CUSTOM_LABEL: "自订",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "眼罩",
           StringsEnum.DCON_LABEL: "直接控制",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "组态",
           StringsEnum.CONFIG_LABEL: "当前配置:",
           StringsEnum.UPLOAD_BUTTON_LABEL: "上载设定",
           StringsEnum.OPEN_DURATION_LABEL: "开放时间",
           StringsEnum.CLOSE_DURATION_LABEL: "关闭时间",
           StringsEnum.DEBOUNCE_LABEL: "去抖时间",
           StringsEnum.BUTTON_MODE_LABEL: "按钮模式",
           StringsEnum.CONTROL_MODE_LABEL: "控制方式",
           StringsEnum.HOLD_VAL_LABEL: "保持",
           StringsEnum.CLICK_VAL_LABEL: "请点击",
           StringsEnum.LENS_VAL_LABEL: "镜片",
           StringsEnum.TRIAL_VAL_LABEL: "试用版",
           StringsEnum.MANUAL_OPEN_LABEL: "开镜头",
           StringsEnum.MANUAL_CLOSE_LABEL: "近摄镜",
           StringsEnum.CONFIG_TAB_TOOLTIP: "显示/隐藏配置选项卡",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "当前设备配置",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "将当前配置上传到设备",
           StringsEnum.OPEN_DURATION_TOOLTIP: "设置镜头开启时间。",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "设置镜头关闭时间。",
           StringsEnum.DEBOUNCE_TOOLTIP: "设置按钮的反跳时间。",
           StringsEnum.BUTTON_MODE_TOOLTIP: "将按钮模式设置为单击或按住。",
           StringsEnum.CONTROL_MODE_TOOLTIP: "将控制模式设置为镜头或试镜。",
           StringsEnum.HOLD_VAL_TOOLTIP: "按住按钮可切换镜头。",
           StringsEnum.CLICK_VAL_TOOLTIP: "单击按钮切换镜头。",
           StringsEnum.LENS_VAL_TOOLTIP: "单击按钮切换镜头。",
           StringsEnum.TRIAL_VAL_TOOLTIP: "单击按钮切换试用。",
           StringsEnum.MANUAL_OPEN_TOOLTIP: "手动打开镜头。",
           StringsEnum.MANUAL_CLOSE_TOOLTIP: "手动关闭镜头。",
           StringsEnum.SAVE_HDR: "时间戳记, 试用版, 打开, 关, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "毫秒",
           StringsEnum.GRAPH_TS: "时间戳记",
           }

# Japanese strings
japanese = {StringsEnum.CUSTOM_LABEL: "カスタム",
            StringsEnum.NHTSA_LABEL: "NHTSA",
            StringsEnum.EBLIND_LABEL: "e目隠し",
            StringsEnum.DCON_LABEL: "直接制御",
            StringsEnum.INF_LABEL: "INF",
            StringsEnum.CONFIG_TAB_LABEL: "構成",
            StringsEnum.CONFIG_LABEL: "現在の構成:",
            StringsEnum.UPLOAD_BUTTON_LABEL: "アップロード設定",
            StringsEnum.OPEN_DURATION_LABEL: "オープン期間",
            StringsEnum.CLOSE_DURATION_LABEL: "クローズ期間",
            StringsEnum.DEBOUNCE_LABEL: "デバウンス時間",
            StringsEnum.BUTTON_MODE_LABEL: "ボタンモード",
            StringsEnum.CONTROL_MODE_LABEL: "制御モード",
            StringsEnum.HOLD_VAL_LABEL: "ホールド",
            StringsEnum.CLICK_VAL_LABEL: "クリック",
            StringsEnum.LENS_VAL_LABEL: "レンズ",
            StringsEnum.TRIAL_VAL_LABEL: "トライアル",
            StringsEnum.MANUAL_OPEN_LABEL: "オープンレンズ",
            StringsEnum.MANUAL_CLOSE_LABEL: "レンズを閉じる",
            StringsEnum.CONFIG_TAB_TOOLTIP: "構成タブの表示/非表示",
            StringsEnum.CONFIG_LABEL_TOOLTIP: "現在のデバイス構成",
            StringsEnum.UPLOAD_BUTTON_TOOLTIP: "現在の構成をデバイスにアップロード",
            StringsEnum.OPEN_DURATION_TOOLTIP: "レンズの開放時間を設定します。",
            StringsEnum.CLOSE_DURATION_TOOLTIP: "レンズのクローズ期間を設定します。",
            StringsEnum.DEBOUNCE_TOOLTIP: "ボタンのデバウンス時間を設定します。",
            StringsEnum.BUTTON_MODE_TOOLTIP: "ボタンモードをクリックまたはホールドに設定します。",
            StringsEnum.CONTROL_MODE_TOOLTIP: "制御モードをレンズまたはトライアルに設定します。",
            StringsEnum.HOLD_VAL_TOOLTIP: "ボタンを押し続けると、レンズが切り替わります。",
            StringsEnum.CLICK_VAL_TOOLTIP: "ボタンをクリックしてレンズを切り替えます。",
            StringsEnum.LENS_VAL_TOOLTIP: "ボタンをクリックしてレンズを切り替えます。",
            StringsEnum.TRIAL_VAL_TOOLTIP: "ボタンをクリックしてトライアルを切り替えます。",
            StringsEnum.MANUAL_OPEN_TOOLTIP: "レンズを手動で開きます。",
            StringsEnum.MANUAL_CLOSE_TOOLTIP: "レンズを手動で閉じます。",
            StringsEnum.SAVE_HDR: "タイムスタンプ, トライアル, 開いた, 閉じる, ",
            StringsEnum.PLOT_NAME_OPEN_CLOSE: "ミリ秒",
            StringsEnum.GRAPH_TS: "タイムスタンプ",
            }

# Add defined languages to strings dictionary.
strings = {LangEnum.ENG: english,
           LangEnum.DUT: dutch,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.RUS: russian,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese,
           LangEnum.JPN: japanese}
