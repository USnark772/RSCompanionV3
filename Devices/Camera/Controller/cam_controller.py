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
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Devices.Camera.View.cam_view import CamView
from Devices.Camera.Resources.cam_strings import strings, StringsEnum, LangEnum


class Controller(AbstractController):
    def __init__(self, cam_index: int, lang: LangEnum, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        cam_name = "CAM_" + str(cam_index)
        view = CamView(cam_name, log_handlers)
        super().__init__(view)
        # TODO: Do stuff here.
        self.set_lang(lang)
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this device's MVC.
        :param lang: The language to use.
        :return None:
        """
        self._logger.debug("running")
        self.view.set_lang(lang)
        self._logger.debug("done")

    def cleanup(self) -> None:
        pass
