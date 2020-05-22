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
import time
from asyncio import create_task, sleep
from multiprocessing import Process, Pipe
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Model.app_helpers import end_tasks
from Devices.Camera.View.cam_view import CamView
from Devices.Camera.Model.cam_model import CamModel
from Devices.Camera.Model import cam_defs as defs
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
        # TODO: Get logging in here. See https://docs.python.org/3/howto/logging-cookbook.html find multiprocessing.
        self._model_msg_pipe, msg_pipe = Pipe()  # For messages/commands.
        self._model_image_pipe, img_pipe = Pipe(False)  # For images.
        self._model = Process(target=CamModel, args=(msg_pipe, img_pipe, cam_index))
        self._model.start()
        # self._model = CamModel(cam_name, cam_index, log_handlers)
        self.set_lang(lang)
        self._awaitable_tasks = []
        self._cancellable_tasks = []
        self._awaitable_tasks.append(create_task(self._update_view()))
        self._switcher = {defs.ModelEnum.FAILURE: self.cleanup,
                          defs.ModelEnum.CUR_FPS: self._update_view_fps}
        self.send_msg_to_model((defs.ModelEnum.SET_USE_CAM, True))
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this device.
        :param lang: The language to use.
        :return None:
        """
        self._logger.debug("running")
        self.view.set_lang(lang)
        self._logger.debug("done")

    def cleanup(self) -> None:
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.CLEANUP, None))
        # TODO: Await model done cleanup msg for video saving? Only if end exp has been called.
        for task in self._cancellable_tasks:
            task.cancel()
        create_task(end_tasks(self._awaitable_tasks))
        self._logger.debug("done")

    def create_exp(self, path: str) -> None:
        """
        Handle experiment created for this device.
        :param path: The path to use to save data.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.START, path))
        self._logger.debug("done")

    def end_exp(self) -> None:
        """
        Handle experiment ended for this device.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.STOP, None))
        self._logger.debug("done")

    async def _handle_pipe(self) -> None:
        """
        Handle msgs from model.
        :return None:
        """
        self._logger.debug("running")
        try:
            while True:
                if self._model_msg_pipe.poll():
                    msg = self._model_msg_pipe.recv()
                    if msg[1] is not None:
                        self._switcher[msg[0]](msg[1])
                    else:
                        self._switcher[msg[0]]()
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

    async def _update_view(self) -> None:
        """
        Update view with latest image from camera.
        :return None:
        """
        self._logger.debug("running")
        try:
            while True:
                if self._model_image_pipe.poll():
                    next_image = self._model_image_pipe.recv()
                    self.view.update_image(next_image)
                else:
                    await sleep(0)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

    def _update_view_fps(self, new_fps) -> None:
        """
        Update view object fps display with new value.
        :param new_fps: The new value.
        :return None:
        """
        self._logger.debug("running")
        self.view.set_fps_val(new_fps)
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        """
        Connect handlers to view object.
        :return None:
        """
        self._logger.debug("running")
        self._logger.debug("done")

    def send_msg_to_model(self, msg) -> None:
        """
        A wrapper for pipe.send()
        :param msg:
        :return:
        """
        try:
            print("Sending msg:", msg, "to model")
            self._model_msg_pipe.send(msg)
        except BrokenPipeError as bpe:
            # print(__name__, "bpe", bpe)
            pass
        except OSError as ose:
            # print(__name__, "ose", ose)
            pass
