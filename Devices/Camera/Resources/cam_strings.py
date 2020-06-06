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
from enum import Enum, auto


# Define enum like this.
class StringsEnum(Enum):
    CONFIG_TAB_LABEL = auto()
    INITIALIZATION_BAR_LABEL = auto()
    INITIALIZING = auto()
    IMAGE_DISPLAY_LABEL = auto()
    IMAGE_DISPLAY = auto()
    SHOW_FEED_CHECKBOX_LABEL = auto()
    RESOLUTION_SELECTOR_LABEL = auto()
    FRAME_ROTATION_SETTING_LABEL = auto()
    FPS_SELECTOR_LABEL = auto()
    FPS_DISPLAY_VALUE = auto()
    CONFIG_TAB_TOOLTIP = auto()
    FRAME_SIZE_TOOLTIP = auto()
    SHOW_CAM_TOOLTIP = auto()
    FPS_DISPLAY_TOOLTIP = auto()
    ROTATION_TOOLTIP = auto()
    IMAGE_DISPLAY_TOOLTIP = auto()


# Define languages like this.
english = {StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.INITIALIZATION_BAR_LABEL: "Initialization progress",
           StringsEnum.IMAGE_DISPLAY_LABEL: "Preview",
           StringsEnum.IMAGE_DISPLAY: "No video",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Show Feed",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "Image Resolution",
           StringsEnum.INITIALIZING: "Initializing",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Rotate Image",
           StringsEnum.FPS_SELECTOR_LABEL: "FPS",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Show/Hide configuration tab",
           StringsEnum.FRAME_SIZE_TOOLTIP: "Select resolution for this camera.",
           StringsEnum.SHOW_CAM_TOOLTIP: "Show or hide camera feed preview. (Does not disable camera)",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "The approximate fps this camera is performing at. This value can be"
                                            " affected by the load your computer is currently under.",
           StringsEnum.ROTATION_TOOLTIP: "Set degree of rotation for video feed. -360 < value < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Preview of camera feed.",
           }

# TODO: Verify translations
# Dutch strings
dutch = {StringsEnum.CONFIG_TAB_LABEL: "Configuratie",
         StringsEnum.INITIALIZATION_BAR_LABEL: "Initialisatievoortgang",
         StringsEnum.IMAGE_DISPLAY_LABEL: "Voorbeeld",
         StringsEnum.IMAGE_DISPLAY: "Geen video",
         StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Feed Weergeven",
         StringsEnum.RESOLUTION_SELECTOR_LABEL: "Foto resolutie",
         StringsEnum.INITIALIZING: "Bezig met initialiseren",
         StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Roteer afbeelding",
         StringsEnum.FPS_SELECTOR_LABEL: "FPS",
         StringsEnum.FPS_DISPLAY_VALUE: "0",
         StringsEnum.CONFIG_TAB_TOOLTIP: "Configuratietabblad weergeven/verbergen",
         StringsEnum.FRAME_SIZE_TOOLTIP: "Selecteer resolutie voor deze camera.",
         StringsEnum.SHOW_CAM_TOOLTIP: "Voorbeeldweergave van camerafeed weergeven of verbergen."
                                       " (Schakelt camera niet uit)",
         StringsEnum.FPS_DISPLAY_TOOLTIP: "De geschatte fps waarop deze camera presteert. Deze waarde kan worden"
                                          " beïnvloed door de belasting van uw computer.",
         StringsEnum.ROTATION_TOOLTIP: "Stel de mate van rotatie in voor videofeed. -360 < waarde < 360.",
         StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Voorbeeld van camerafeed.",
         }

# French strings
french = {StringsEnum.CONFIG_TAB_LABEL: "Configuration",
          StringsEnum.INITIALIZATION_BAR_LABEL: "Progression de l'initialisation",
          StringsEnum.IMAGE_DISPLAY_LABEL: "Aperçu",
          StringsEnum.IMAGE_DISPLAY: "Pas de vidéo",
          StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Afficher le flux",
          StringsEnum.RESOLUTION_SELECTOR_LABEL: "Résolution de l'image",
          StringsEnum.INITIALIZING: "Initialisation",
          StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Faire pivoter l'image",
          StringsEnum.FPS_SELECTOR_LABEL: "FPS",
          StringsEnum.FPS_DISPLAY_VALUE: "0",
          StringsEnum.CONFIG_TAB_TOOLTIP: "Afficher/masquer l'onglet de configuration",
          StringsEnum.FRAME_SIZE_TOOLTIP: "Sélectionnez la résolution de cette caméra.",
          StringsEnum.SHOW_CAM_TOOLTIP: "Afficher ou masquer l'aperçu du flux de la caméra."
                                        " (Ne désactive pas la caméra)",
          StringsEnum.FPS_DISPLAY_TOOLTIP: "Les fps approximatifs de cet appareil photo à."
                                           " Cette valeur peut être affectée par la charge de votre ordinateur.",
          StringsEnum.ROTATION_TOOLTIP: "Définissez le degré de rotation du flux vidéo. -360 < valeur < 360.",
          StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Aperçu du flux de la caméra.",
          }

# German strings
german = {StringsEnum.CONFIG_TAB_LABEL: "Konfiguration",
          StringsEnum.INITIALIZATION_BAR_LABEL: "Initialisierungsfortschritt",
          StringsEnum.IMAGE_DISPLAY_LABEL: "Vorschau",
          StringsEnum.IMAGE_DISPLAY: "Kein Video",
          StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Feed anzeigen",
          StringsEnum.RESOLUTION_SELECTOR_LABEL: "Bildauflösung",
          StringsEnum.INITIALIZING: "Initialisieren",
          StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Bild drehen",
          StringsEnum.FPS_SELECTOR_LABEL: "FPS",
          StringsEnum.FPS_DISPLAY_VALUE: "0",
          StringsEnum.CONFIG_TAB_TOOLTIP: "Registerkarte Konfiguration anzeigen/ausblenden",
          StringsEnum.FRAME_SIZE_TOOLTIP: "Wählen Sie die Auflösung für diese Kamera.",
          StringsEnum.SHOW_CAM_TOOLTIP: "Vorschau des Kamera-Feeds ein- oder ausblenden."
                                        " (Deaktiviert die Kamera nicht)",
          StringsEnum.FPS_DISPLAY_TOOLTIP: "Die ungefähren Bilder pro Sekunde, mit denen diese Kamera arbeitet."
                                           " Dieser Wert kann durch die Belastung Ihres Computers beeinflusst werden.",
          StringsEnum.ROTATION_TOOLTIP: "Stellen Sie den Rotationsgrad für den Video-Feed ein. -360 < Wert < 360.",
          StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Vorschau des Kamera-Feeds.",
          }

# Russian strings
russian = {StringsEnum.CONFIG_TAB_LABEL: "конфигурация",
           StringsEnum.INITIALIZATION_BAR_LABEL: "Процесс инициализации",
           StringsEnum.IMAGE_DISPLAY_LABEL: "предварительный просмотр",
           StringsEnum.IMAGE_DISPLAY: "Нет видео",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Показать видео",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "Разрешение изображения",
           StringsEnum.INITIALIZING: "Инициализация",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Повернуть изображение",
           StringsEnum.FPS_SELECTOR_LABEL: "FPS",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Показать/Скрыть вкладку конфигурации",
           StringsEnum.FRAME_SIZE_TOOLTIP: "Выберите разрешение для этой камеры.",
           StringsEnum.SHOW_CAM_TOOLTIP: "Показать или скрыть предварительный просмотр камеры. (Не отключает камеру)",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "Приблизительный кадр / с, с которым работает эта камера."
                                            " На это значение может повлиять нагрузка на ваш компьютер.",
           StringsEnum.ROTATION_TOOLTIP: "Установите степень поворота видео. -360 < значение < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Предварительный просмотр камеры.",
           }

# Spanish strings
spanish = {StringsEnum.CONFIG_TAB_LABEL: "Configuración",
           StringsEnum.INITIALIZATION_BAR_LABEL: "Progreso de inicialización",
           StringsEnum.IMAGE_DISPLAY_LABEL: "Preestreno",
           StringsEnum.IMAGE_DISPLAY: "No hay video",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Mostrar feed",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "Resolución de imagen",
           StringsEnum.INITIALIZING: "Inicializando",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Girar imagen",
           StringsEnum.FPS_SELECTOR_LABEL: "FPS",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Mostrar/Ocultar pestaña de configuración",
           StringsEnum.FRAME_SIZE_TOOLTIP: "Seleccione la resolución para esta cámara.",
           StringsEnum.SHOW_CAM_TOOLTIP: "Mostrar u ocultar la vista previa de alimentación de la cámara."
                                         " (No desactiva la cámara)",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "Los fps aproximados que esta cámara está realizando. Este valor puede"
                                            " verse afectado por la carga a la que se encuentra actualmente"
                                            " su computadora.",
           StringsEnum.ROTATION_TOOLTIP: "Establecer el grado de rotación para la alimentación de video."
                                         " -360 < valor < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Vista previa de la alimentación de la cámara.",
           }

# Chinese simplified strings
# TODO: Verify simplified.
chinese = {StringsEnum.CONFIG_TAB_LABEL: "组态",
           StringsEnum.INITIALIZATION_BAR_LABEL: "初始化进度",
           StringsEnum.IMAGE_DISPLAY_LABEL: "预习",
           StringsEnum.IMAGE_DISPLAY: "沒有視頻",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "显示提要",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "影像解析度",
           StringsEnum.INITIALIZING: "初始化中",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "旋转影像",
           StringsEnum.FPS_SELECTOR_LABEL: "帧数",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.CONFIG_TAB_TOOLTIP: "显示/隐藏配置选项卡",
           StringsEnum.FRAME_SIZE_TOOLTIP: "选择此相机的分辨率。",
           StringsEnum.SHOW_CAM_TOOLTIP: "显示或隐藏相机供稿预览。 （不禁用相机）",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "相机执行的大概fps。 该值可能会受到计算机当前负载的影响。",
           StringsEnum.ROTATION_TOOLTIP: "设置视频馈送的旋转度。 -360 <值<360。",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "相机供稿预览。",
           }

# Japanese strings
japanese = {StringsEnum.CONFIG_TAB_LABEL: "構成",
            StringsEnum.INITIALIZATION_BAR_LABEL: "初期化の進行状況",
            StringsEnum.IMAGE_DISPLAY_LABEL: "プレビュー",
            StringsEnum.IMAGE_DISPLAY: "ビデオなし",
            StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "フィードを表示",
            StringsEnum.RESOLUTION_SELECTOR_LABEL: "画像解像度",
            StringsEnum.INITIALIZING: "初期化中",
            StringsEnum.FRAME_ROTATION_SETTING_LABEL: "画像を回転",
            StringsEnum.FPS_SELECTOR_LABEL: "FPS",
            StringsEnum.FPS_DISPLAY_VALUE: "0",
            StringsEnum.CONFIG_TAB_TOOLTIP: "構成タブの表示/非表示",
            StringsEnum.FRAME_SIZE_TOOLTIP: "このカメラの解像度を選択します。",
            StringsEnum.SHOW_CAM_TOOLTIP: "カメラフィードのプレビューを表示または非表示にします。"
                                          " （カメラを無効にしません）",
            StringsEnum.FPS_DISPLAY_TOOLTIP: "このカメラが実行しているおおよそのfps。 この値は、コンピューターに現在か"
                                             "かっている負荷の影響を受ける可能性があります。",
            StringsEnum.ROTATION_TOOLTIP: "ビデオフィードの回転角度を設定します。 -360 <値<360。",
            StringsEnum.IMAGE_DISPLAY_TOOLTIP: "カメラフィードのプレビュー。",
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
