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
    INITIALIZATION_BAR_LABEL = auto()
    IMAGE_DISPLAY_LABEL = auto()
    IMAGE_DISPLAY = auto()
    SHOW_CAM_CHECKBOX_LABEL = auto()
    FRAME_SIZE_SELECTOR_LABEL = auto()
    FRAME_ROTATION_SETTING_LABEL = auto()
    FPS_DISPLAY_LABEL = auto()
    FPS_DISPLAY_VALUE = auto()
    FRAME_SIZE_TOOLTIP = auto()
    SHOW_CAM_TOOLTIP = auto()
    FPS_DISPLAY_TOOLTIP = auto()
    ROTATION_TOOLTIP = auto()
    IMAGE_DISPLAY_TOOLTIP = auto()


# Define languages like this.
english = {StringsEnum.INITIALIZATION_BAR_LABEL: "Initialization progress",
           StringsEnum.IMAGE_DISPLAY_LABEL: "Preview",
           StringsEnum.IMAGE_DISPLAY: "Initializing",
           StringsEnum.SHOW_CAM_CHECKBOX_LABEL: "Show Feed",
           StringsEnum.FRAME_SIZE_SELECTOR_LABEL: "Frame Size",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Rotate Image",
           StringsEnum.FPS_DISPLAY_LABEL: "FPS:",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
           StringsEnum.FRAME_SIZE_TOOLTIP: "Select resolution for this camera.",
           StringsEnum.SHOW_CAM_TOOLTIP: "Show or hide camera feed preview. (Does not disable camera)",
           StringsEnum.FPS_DISPLAY_TOOLTIP: "The approximate fps this camera is performing at. This value can be"
                                            " affected by the load your computer is currently under.",
           StringsEnum.ROTATION_TOOLTIP: "Set degree of rotation for video feed. -360 < value < 360.",
           StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Preview of camera feed.",
           }

# TODO: Verify translations
french = {StringsEnum.INITIALIZATION_BAR_LABEL: "Progression de l'initialisation",
          StringsEnum.IMAGE_DISPLAY_LABEL: "Aperçu",
          StringsEnum.IMAGE_DISPLAY: "Initialisation",
          StringsEnum.SHOW_CAM_CHECKBOX_LABEL: "Afficher le flux",
          StringsEnum.FRAME_SIZE_SELECTOR_LABEL: "Taille du cadre",
          StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Faire pivoter l'image",
          StringsEnum.FPS_DISPLAY_LABEL: "FPS:",
          StringsEnum.FPS_DISPLAY_VALUE: "0",
          StringsEnum.FRAME_SIZE_TOOLTIP: "Sélectionnez la résolution de cette caméra.",
          StringsEnum.SHOW_CAM_TOOLTIP: "Afficher ou masquer l'aperçu du flux de la caméra."
                                        " (Ne désactive pas la caméra)",
          StringsEnum.FPS_DISPLAY_TOOLTIP: "Les fps approximatifs de cet appareil photo à."
                                           " Cette valeur peut être affectée par la charge de votre ordinateur.",
          StringsEnum.ROTATION_TOOLTIP: "Définissez le degré de rotation du flux vidéo. -360 < valeur < 360.",
          StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Aperçu du flux de la caméra.",
          }

german = {StringsEnum.INITIALIZATION_BAR_LABEL: "Initialisierungsfortschritt",
          StringsEnum.IMAGE_DISPLAY_LABEL: "Vorschau",
          StringsEnum.IMAGE_DISPLAY: "Initialisieren",
          StringsEnum.SHOW_CAM_CHECKBOX_LABEL: "Feed anzeigen",
          StringsEnum.FRAME_SIZE_SELECTOR_LABEL: "Rahmengröße",
          StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Bild drehen",
          StringsEnum.FPS_DISPLAY_LABEL: "FPS:",
          StringsEnum.FPS_DISPLAY_VALUE: "0",
          StringsEnum.FRAME_SIZE_TOOLTIP: "Wählen Sie die Auflösung für diese Kamera.",
          StringsEnum.SHOW_CAM_TOOLTIP: "Vorschau des Kamera-Feeds ein- oder ausblenden."
                                        " (Deaktiviert die Kamera nicht)",
          StringsEnum.FPS_DISPLAY_TOOLTIP: "Die ungefähren Bilder pro Sekunde, mit denen diese Kamera arbeitet."
                                           " Dieser Wert kann durch die Belastung Ihres Computers beeinflusst werden.",
          StringsEnum.ROTATION_TOOLTIP: "Stellen Sie den Rotationsgrad für den Video-Feed ein. -360 < Wert < 360.",
          StringsEnum.IMAGE_DISPLAY_TOOLTIP: "Vorschau des Kamera-Feeds.",
          }

spanish = {StringsEnum.INITIALIZATION_BAR_LABEL: "Progreso de inicialización",
           StringsEnum.IMAGE_DISPLAY_LABEL: "Preestreno",
           StringsEnum.IMAGE_DISPLAY: "Inicializando",
           StringsEnum.SHOW_CAM_CHECKBOX_LABEL: "Mostrar feed",
           StringsEnum.FRAME_SIZE_SELECTOR_LABEL: "Tamaño del marco",
           StringsEnum.FRAME_ROTATION_SETTING_LABEL: "Girar imagen",
           StringsEnum.FPS_DISPLAY_LABEL: "FPS:",
           StringsEnum.FPS_DISPLAY_VALUE: "0",
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

chinese = english

# Add defined languages to strings dictionary.
strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}