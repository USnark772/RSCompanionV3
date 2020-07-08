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

from cv2 import CAP_DSHOW, VideoWriter_fourcc
from enum import Enum, auto

cap_backend = CAP_DSHOW
cap_temp_codec = VideoWriter_fourcc(*'mjpg')
cap_codec = VideoWriter_fourcc(*'MJPG')

common_resolutions = [(640.0, 480.0),
                      (640.0, 640.0),
                      (800.0, 600.0),
                      (960.0, 720.0),
                      (1024.0, 768.0),
                      (1248.0, 1536.0),
                      (1280.0, 720.0),
                      (1280.0, 960.0),
                      (1440.0, 1080.0),
                      (1600.0, 900.0),
                      (1600.0, 1200.0),
                      (1920.0, 1080.0),
                      ]


class ModelEnum(Enum):
    CLEANUP = auto()
    START = auto()
    STOP = auto()
    SET_RES = auto()
    GET_RES = auto()
    CUR_RES = auto()
    SET_FPS = auto()
    GET_FPS = auto()
    CUR_FPS = auto()
    SET_USE_CAM = auto()
    SET_USE_FEED = auto()
    FAILURE = auto()
    STAT_UPD = auto()
    INITIALIZE = auto()
    OVERLAY = auto()
    COND_NAME = auto()
    BLOCK_NUM = auto()
    KEYFLAG = auto()
    EXP_STATUS = auto()
    LANGUAGE = auto()
