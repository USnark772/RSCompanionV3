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

from RSCompanionAsync.Model.app_defs import LangEnum
from enum import Enum, auto


# TODO: Check translations.

# Define enum like this.
class StringsEnum(Enum):
    CONFIG_TAB_LABEL = auto()
    INITIALIZATION_BAR_LABEL = auto()
    INITIALIZING = auto()
    IMAGE_DISPLAY_LABEL = auto()
    IMAGE_DISPLAY = auto()
    SHOW_FEED_CHECKBOX_LABEL = auto()
    USE_CAM_CHECKBOX_LABEL = auto()
    RESOLUTION_SELECTOR_LABEL = auto()
    FRAME_ROTATION_SETTING_LABEL = auto()
    FPS_SELECTOR_LABEL = auto()
    FPS_DISPLAY_VALUE = auto()
    BLOCK_KEY_FLAG = auto()
    EXP_STATUS_LABEL = auto()
    EXP_STATUS_PAUSE = auto()
    EXP_STATUS_RUN = auto()
    EXP_STATUS_STOP = auto()
    FPS_SELECTOR_TOOLTIP = auto()
    CONFIG_TAB_TOOLTIP = auto()
    RESOLUTION_SELECTOR_TOOLTIP = auto()
    SHOW_FEED_CHECKBOX_TOOLTIP = auto()
    USE_CAM_CHECKBOX_TOOLTIP = auto()
    FPS_DISPLAY_TOOLTIP = auto()
    ROTATION_TOOLTIP = auto()
    IMAGE_DISPLAY_TOOLTIP = auto()
    OVERLAY_COND_NAME_LABEL = auto()
    OVERLAY_BLOCK_NUM_LABEL = auto()
    OVERLAY_KEYFLAG_LABEL = auto()
    OVERLAY_FPS_LABEL = auto()
    OVERLAY_EXP_STATUS_LABEL = auto()


# Define languages like this.
english = {StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.INITIALIZATION_BAR_LABEL: "Initialization progress",
           StringsEnum.INITIALIZING: "Initializing",
           StringsEnum.IMAGE_DISPLAY_LABEL: "Preview",
           StringsEnum.IMAGE_DISPLAY: "No video",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Show Feed",
           StringsEnum.USE_CAM_CHECKBOX_LABEL: "Use Camera",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "Image Resolution",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Rotate Image",
           StringsEnum.FPS_SELECTOR_LABEL: "FPS Limiter",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.BLOCK_KEY_FLAG: "Block #, Key Flag: ",
           StringsEnum.EXP_STATUS_LABEL: "Exp Status: ",
           StringsEnum.EXP_STATUS_STOP: "Stopped",
           StringsEnum.EXP_STATUS_RUN: "Running",
           StringsEnum.EXP_STATUS_PAUSE: "Paused",
           StringsEnum.FPS_SELECTOR_TOOLTIP: "Limit camera FPS. (If camera is lagging)",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Show/Hide configuration tab",
           StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "Select resolution for this camera. (Higher resolutions may cause"
                                                    " lag)",
           StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "Show or hide camera feed preview. (Does not disable camera)",
           StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "Enable/disable use of this camera.",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "The approximate fps this camera is performing at. This value can be"
                                            " affected by the load your computer is currently under.",
           StringsEnum.ROTATION_TOOLTIP: "Set degree of rotation for video feed. -360 < value < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Preview of camera feed.",
           StringsEnum.OVERLAY_COND_NAME_LABEL: "Cond Name:",
           StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
           StringsEnum.OVERLAY_KEYFLAG_LABEL: "Keyflag:",
           StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Block #:",
           StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Exp Status:",
           }

# Dutch strings
dutch = {StringsEnum.CONFIG_TAB_LABEL: "Configuratie",
         StringsEnum.INITIALIZATION_BAR_LABEL: "Initialisatievoortgang",
         StringsEnum.INITIALIZING: "Bezig met initialiseren",
         StringsEnum.IMAGE_DISPLAY_LABEL: "Voorbeeld",
         StringsEnum.IMAGE_DISPLAY: "Geen video",
         StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Feed Weergeven",
         StringsEnum.USE_CAM_CHECKBOX_LABEL: "Gebruikerscamera",
         StringsEnum.RESOLUTION_SELECTOR_LABEL: "Foto resolutie",
         StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Roteer afbeelding",
         StringsEnum.FPS_SELECTOR_LABEL: "FPS Limiter",
         StringsEnum.FPS_DISPLAY_VALUE: "0",
         StringsEnum.BLOCK_KEY_FLAG: "Blok #, Sleutel vlag: ",
         StringsEnum.EXP_STATUS_LABEL: "Exp Status: ",
         StringsEnum.EXP_STATUS_STOP: "Gestopt",
         StringsEnum.EXP_STATUS_RUN: "Rennen",
         StringsEnum.EXP_STATUS_PAUSE: "Onderbroken",
         StringsEnum.FPS_SELECTOR_TOOLTIP: "Beperk camera FPS. (Als de camera achterblijft)",
         StringsEnum.CONFIG_TAB_TOOLTIP: "Configuratietabblad weergeven/verbergen",
         StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "Selecteer resolutie voor deze camera.",
         StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "Voorbeeldweergave van camerafeed weergeven of verbergen."
                                       " (Schakelt camera niet uit)",
         StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "Schakel het gebruik van deze camera in / uit.",
         StringsEnum.FPS_DISPLAY_TOOLTIP: "De geschatte fps waarop deze camera presteert. Deze waarde kan worden"
                                          " beïnvloed door de belasting van uw computer.",
         StringsEnum.ROTATION_TOOLTIP: "Stel de mate van rotatie in voor videofeed. -360 < waarde < 360.",
         StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Voorbeeld van camerafeed.",
         StringsEnum.OVERLAY_COND_NAME_LABEL: "Conditienaam:",
         StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
         StringsEnum.OVERLAY_KEYFLAG_LABEL: "Sleutelvlag:",
         StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Blok #:",
         StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Experimentstatus:",
         }

# French strings
french = {StringsEnum.CONFIG_TAB_LABEL: "Configuration",
          StringsEnum.INITIALIZATION_BAR_LABEL: "Progression de l'initialisation",
          StringsEnum.INITIALIZING: "Initialisation",
          StringsEnum.IMAGE_DISPLAY_LABEL: "Aperçu",
          StringsEnum.IMAGE_DISPLAY: "Pas de vidéo",
          StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Afficher le flux",
          StringsEnum.USE_CAM_CHECKBOX_LABEL: "Caméra utilisateur",
          StringsEnum.RESOLUTION_SELECTOR_LABEL: "Résolution de l'image",
          StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Faire pivoter l'image",
          StringsEnum.FPS_SELECTOR_LABEL: "FPS Limiter",
          StringsEnum.FPS_DISPLAY_VALUE: "0",
          StringsEnum.BLOCK_KEY_FLAG: "Bloc #, Drapeau Clé: ",
          StringsEnum.EXP_STATUS_LABEL: "Statut de l'exp: ",
          StringsEnum.EXP_STATUS_STOP: "Arrêté",
          StringsEnum.EXP_STATUS_RUN: "Fonctionnement",
          StringsEnum.EXP_STATUS_PAUSE: "En pause",
          StringsEnum.FPS_SELECTOR_TOOLTIP: "Limiter le FPS de la caméra. (Si la caméra est en retard)",
          StringsEnum.CONFIG_TAB_TOOLTIP: "Afficher/masquer l'onglet de configuration",
          StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "Sélectionnez la résolution de cette caméra.",
          StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "Afficher ou masquer l'aperçu du flux de la caméra."
                                        " (Ne désactive pas la caméra)",
          StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "Activez / désactivez l'utilisation de cette caméra.",
          StringsEnum.FPS_DISPLAY_TOOLTIP: "Les fps approximatifs de cet appareil photo à."
                                           " Cette valeur peut être affectée par la charge de votre ordinateur.",
          StringsEnum.ROTATION_TOOLTIP: "Définissez le degré de rotation du flux vidéo. -360 < valeur < 360.",
          StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Aperçu du flux de la caméra.",
          StringsEnum.OVERLAY_COND_NAME_LABEL: "Nom de la condition:",
          StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
          StringsEnum.OVERLAY_KEYFLAG_LABEL: "Drapeau clé:",
          StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Bloc #:",
          StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Statut de l'expérience:",
          }

# German strings
german = {StringsEnum.CONFIG_TAB_LABEL: "Konfiguration",
          StringsEnum.INITIALIZATION_BAR_LABEL: "Initialisierungsfortschritt",
          StringsEnum.INITIALIZING: "Initialisieren",
          StringsEnum.IMAGE_DISPLAY_LABEL: "Vorschau",
          StringsEnum.IMAGE_DISPLAY: "Kein Video",
          StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Feed anzeigen",
          StringsEnum.USE_CAM_CHECKBOX_LABEL: "Benutzerkamera",
          StringsEnum.RESOLUTION_SELECTOR_LABEL: "Bildauflösung",
          StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Bild drehen",
          StringsEnum.FPS_SELECTOR_LABEL: "FPS-Begrenzer",
          StringsEnum.FPS_DISPLAY_VALUE: "0",
          StringsEnum.BLOCK_KEY_FLAG: "Block #, Schlüsselflagge: ",
          StringsEnum.EXP_STATUS_LABEL: "Experimentstatus: ",
          StringsEnum.EXP_STATUS_STOP: "Gestoppt",
          StringsEnum.EXP_STATUS_RUN: "Laufen",
          StringsEnum.EXP_STATUS_PAUSE: "Pause",
          StringsEnum.FPS_SELECTOR_TOOLTIP: "Begrenzen Sie die Kamera-FPS. (Wenn die Kamera zurückbleibt)",
          StringsEnum.CONFIG_TAB_TOOLTIP: "Registerkarte Konfiguration anzeigen/ausblenden",
          StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "Wählen Sie die Auflösung für diese Kamera.",
          StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "Vorschau des Kamera-Feeds ein- oder ausblenden."
                                        " (Deaktiviert die Kamera nicht)",
          StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "Aktivieren / Deaktivieren der Verwendung dieser Kamera.",
          StringsEnum.FPS_DISPLAY_TOOLTIP: "Die ungefähren Bilder pro Sekunde, mit denen diese Kamera arbeitet."
                                           " Dieser Wert kann durch die Belastung Ihres Computers beeinflusst werden.",
          StringsEnum.ROTATION_TOOLTIP: "Stellen Sie den Rotationsgrad für den Video-Feed ein. -360 < Wert < 360.",
          StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Vorschau des Kamera-Feeds.",
          StringsEnum.OVERLAY_COND_NAME_LABEL: "Bedingungsname:",
          StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
          StringsEnum.OVERLAY_KEYFLAG_LABEL: "Schlüsselflagge:",
          StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Block #:",
          StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Versuchsstatus:",
          }

# Russian strings
russian = {StringsEnum.CONFIG_TAB_LABEL: "конфигурация",
           StringsEnum.INITIALIZATION_BAR_LABEL: "Процесс инициализации",
           StringsEnum.INITIALIZING: "Инициализация",
           StringsEnum.IMAGE_DISPLAY_LABEL: "предварительный просмотр",
           StringsEnum.IMAGE_DISPLAY: "Нет видео",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Показать видео",
           StringsEnum.USE_CAM_CHECKBOX_LABEL: "Пользовательская камера",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "Разрешение изображения",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Повернуть изображение",
           StringsEnum.FPS_SELECTOR_LABEL: "FPS Limiter",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.BLOCK_KEY_FLAG: "Блок №, Ключ: ",
           StringsEnum.EXP_STATUS_LABEL: "Статус эксперимента: ",
           StringsEnum.EXP_STATUS_STOP: "Остановился",
           StringsEnum.EXP_STATUS_RUN: "идущий",
           StringsEnum.EXP_STATUS_PAUSE: "Приостановлено",
           StringsEnum.FPS_SELECTOR_TOOLTIP: "Предельная камера FPS. (Если камера отстает)",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Показать/Скрыть вкладку конфигурации",
           StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "Выберите разрешение для этой камеры.",
           StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "Показать или скрыть предварительный просмотр камеры."
                                                   " (Не отключает камеру)",
           StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "Enable/disable use of this camera.",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "Приблизительный кадр / с, с которым работает эта камера."
                                            " На это значение может повлиять нагрузка на ваш компьютер.",
           StringsEnum.ROTATION_TOOLTIP: "Установите степень поворота видео. -360 < значение < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Предварительный просмотр камеры.",
           StringsEnum.OVERLAY_COND_NAME_LABEL: "Cond Name:",
           StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
           StringsEnum.OVERLAY_KEYFLAG_LABEL: "Keyflag:",
           StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Block #:",
           StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Exp Status:",
           }

# Spanish strings
spanish = {StringsEnum.CONFIG_TAB_LABEL: "Configuración",
           StringsEnum.INITIALIZATION_BAR_LABEL: "Progreso de inicialización",
           StringsEnum.INITIALIZING: "Inicializando",
           StringsEnum.IMAGE_DISPLAY_LABEL: "Preestreno",
           StringsEnum.IMAGE_DISPLAY: "No hay video",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "Mostrar feed",
           StringsEnum.USE_CAM_CHECKBOX_LABEL: "Cámara de usuario",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "Resolución de imagen",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Girar imagen",
           StringsEnum.FPS_SELECTOR_LABEL: "Limitador FPS",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.BLOCK_KEY_FLAG: "Bloque #, clave: ",
           StringsEnum.EXP_STATUS_LABEL: "Estado exp: ",
           StringsEnum.EXP_STATUS_STOP: "Detenido",
           StringsEnum.EXP_STATUS_RUN: "Corriendo",
           StringsEnum.EXP_STATUS_PAUSE: "Pausado",
           StringsEnum.FPS_SELECTOR_TOOLTIP: "Límite de cámara FPS. (Si la cámara está retrasada)",
           StringsEnum.CONFIG_TAB_TOOLTIP: "Mostrar/Ocultar pestaña de configuración",
           StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "Seleccione la resolución para esta cámara.",
           StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "Mostrar u ocultar la vista previa de alimentación de la cámara."
                                         " (No desactiva la cámara)",
           StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "Activar / desactivar el uso de esta cámara.",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "Los fps aproximados que esta cámara está realizando. Este valor puede"
                                            " verse afectado por la carga a la que se encuentra actualmente"
                                            " su computadora.",
           StringsEnum.ROTATION_TOOLTIP: "Establecer el grado de rotación para la alimentación de video."
                                         " -360 < valor < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Vista previa de la alimentación de la cámara.",
           StringsEnum.OVERLAY_COND_NAME_LABEL: "Nombre de condición:",
           StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
           StringsEnum.OVERLAY_KEYFLAG_LABEL: "Bandera clave:",
           StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Bloque #:",
           StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Estado del experimento:",
           }

# Chinese simplified strings
chinese = {StringsEnum.CONFIG_TAB_LABEL: "组态",
           StringsEnum.INITIALIZATION_BAR_LABEL: "初始化进度",
           StringsEnum.INITIALIZING: "初始化中",
           StringsEnum.IMAGE_DISPLAY_LABEL: "预习",
           StringsEnum.IMAGE_DISPLAY: "沒有視頻",
           StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "显示提要",
           StringsEnum.USE_CAM_CHECKBOX_LABEL: "用户相机",
           StringsEnum.RESOLUTION_SELECTOR_LABEL: "影像解析度",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "旋转影像",
           StringsEnum.FPS_SELECTOR_LABEL: "FPS 限制器",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.BLOCK_KEY_FLAG: "块号，钥匙标: ",
           StringsEnum.EXP_STATUS_LABEL: "实验状态: ",
           StringsEnum.EXP_STATUS_STOP: "已停止",
           StringsEnum.EXP_STATUS_RUN: "跑步",
           StringsEnum.EXP_STATUS_PAUSE: "已暂停",
           StringsEnum.FPS_SELECTOR_TOOLTIP: "限制相机的FPS。 (如果相机落后)",
           StringsEnum.CONFIG_TAB_TOOLTIP: "显示/隐藏配置选项卡",
           StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "选择此相机的分辨率。",
           StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "显示或隐藏相机供稿预览。 （不禁用相机）",
           StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "启用/禁用此相机。",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "相机执行的大概fps。 该值可能会受到计算机当前负载的影响。",
           StringsEnum.ROTATION_TOOLTIP: "设置视频馈送的旋转度。 -360 <值<360。",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "相机供稿预览。",
           StringsEnum.OVERLAY_COND_NAME_LABEL: "Cond Name:",
           StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
           StringsEnum.OVERLAY_KEYFLAG_LABEL: "Keyflag:",
           StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Block #:",
           StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Exp Status:",
           }

# Japanese strings
japanese = {StringsEnum.CONFIG_TAB_LABEL: "構成",
            StringsEnum.INITIALIZATION_BAR_LABEL: "初期化の進行状況",
            StringsEnum.INITIALIZING: "初期化中",
            StringsEnum.IMAGE_DISPLAY_LABEL: "プレビュー",
            StringsEnum.IMAGE_DISPLAY: "ビデオなし",
            StringsEnum.SHOW_FEED_CHECKBOX_LABEL: "フィードを表示",
            StringsEnum.USE_CAM_CHECKBOX_LABEL: "ユーザーカメラ",
            StringsEnum.RESOLUTION_SELECTOR_LABEL: "画像解像度",
            StringsEnum.FRAME_ROTATION_SETTING_LABEL: "画像を回転",
            StringsEnum.FPS_SELECTOR_LABEL: "FPSリミッター",
            StringsEnum.FPS_DISPLAY_VALUE: "0",
            StringsEnum.BLOCK_KEY_FLAG: "ブロック番号、キーフラグ: ",
            StringsEnum.EXP_STATUS_LABEL: "実験状況: ",
            StringsEnum.EXP_STATUS_STOP: "停止",
            StringsEnum.EXP_STATUS_RUN: "ランニング",
            StringsEnum.EXP_STATUS_PAUSE: "一時停止",
            StringsEnum.FPS_SELECTOR_TOOLTIP: "カメラのFPSを制限します。 (カメラが遅れている場合)",
            StringsEnum.CONFIG_TAB_TOOLTIP: "構成タブの表示/非表示",
            StringsEnum.RESOLUTION_SELECTOR_TOOLTIP: "このカメラの解像度を選択します。",
            StringsEnum.SHOW_FEED_CHECKBOX_TOOLTIP: "カメラフィードのプレビューを表示または非表示にします。"
                                          " （カメラを無効にしません）",
            StringsEnum.USE_CAM_CHECKBOX_TOOLTIP: "このカメラの使用を有効/無効にします。",
            StringsEnum.FPS_DISPLAY_TOOLTIP: "このカメラが実行しているおおよそのfps。 この値は、コンピューターに現在か"
                                             "かっている負荷の影響を受ける可能性があります。",
            StringsEnum.ROTATION_TOOLTIP: "ビデオフィードの回転角度を設定します。 -360 <値<360。",
            StringsEnum.IMAGE_DISPLAY_TOOLTIP: "カメラフィードのプレビュー。",
            StringsEnum.OVERLAY_COND_NAME_LABEL: "Cond Name:",
            StringsEnum.OVERLAY_FPS_LABEL: "FPS:",
            StringsEnum.OVERLAY_KEYFLAG_LABEL: "Keyflag:",
            StringsEnum.OVERLAY_BLOCK_NUM_LABEL: "Block #:",
            StringsEnum.OVERLAY_EXP_STATUS_LABEL: "Exp Status:",
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
