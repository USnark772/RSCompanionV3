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
from asyncio import create_task
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Model.app_helpers import end_tasks
from Devices.Camera.View.cam_view import CamView
from Devices.Camera.Model.cam_model import CamModel
from Devices.Camera.Resources.cam_strings import strings, StringsEnum, LangEnum


class Controller(AbstractController):
    def __init__(self, cam_index: int = 0, lang: LangEnum = LangEnum.ENG, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        cam_name = "CAM_" + str(cam_index)
        view = CamView(cam_name, log_handlers)
        super().__init__(view)
        self._model = CamModel(cam_name, cam_index, log_handlers)
        self.set_lang(lang)
        self._awaitable_tasks = []
        self._cancellable_tasks = []
        self._awaitable_tasks.append(create_task(self._update_view()))
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
        self._model.cleanup()
        for task in self._cancellable_tasks:
            task.cancel()
        create_task(end_tasks(self._awaitable_tasks))

    async def _update_view(self) -> None:
        """
        Update view with latest image from camera.
        :return None:
        """
        while True:
            await self._model.await_new_image()
            self.view.update_image(self._model.get_latest_frame())

    def _setup_handlers(self) -> None:
        """
        Connect handlers to view object.
        :return None:
        """
        pass
