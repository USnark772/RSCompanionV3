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

from logging import getLogger, StreamHandler
from asyncio import create_task, Event, futures
from cv2 import COLOR_BGR2RGB, cvtColor
from numpy import ndarray
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt
from Model.app_helpers import await_event
from Devices.Camera.Model import cam_defs as defs
from Devices.Camera.Model.cam_stream_reader import StreamReader


class CamModel:
    def __init__(self, cam_name: str = "", cam_index: int = 0, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._new_image_event = Event()
        self._cam_reader = StreamReader(cam_index)
        self._cam_reader.start()
        self._latest_frame: ndarray
        self._logger.debug("Initialized")

    def await_new_image(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._new_image_event)

    def get_latest_frame(self) -> QPixmap:
        """
        :return QPixmap: The latest frame in QPixmap form.
        """
        return self.convert_frame_to_qt_image(self._latest_frame)

    def cleanup(self) -> None:
        """
        Cleanup this code and prep for app closure.
        :return None:
        """
        self._logger.debug("running")
        self._cam_reader.cleanup()
        self._logger.debug("done")

    async def _handle_new_frame(self) -> None:
        """
        Handle frames from camera
        :return None:
        """
        while True:
            await self._cam_reader.await_new_frame()
            self._latest_frame = self._cam_reader.get_latest_frame()
            self._new_image_event.set()
            # TODO: Do stuff with frame here.

    @staticmethod
    def convert_frame_to_qt_image(frame: ndarray) -> QPixmap:
        """
        Convert image to suitable format for display in Qt.
        :param frame: The image to convert.
        :return QPixmap: The converted image.
        """
        rgb_image = cvtColor(frame, COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(248, 186, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
