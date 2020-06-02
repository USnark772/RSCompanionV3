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
from concurrent.futures import ThreadPoolExecutor
from asyncio import create_task, sleep, Event, futures, get_running_loop
from threading import Event as TEvent
from time import sleep
from multiprocessing import Process, Pipe
from numpy import ndarray
from PySide2.QtGui import QPixmap, QImage
from cv2 import cvtColor, COLOR_BGR2RGB
from Model.app_helpers import await_event
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Devices.Camera.View.cam_view import CamView
from Devices.Camera.Model.cam_model import CamModel
from Devices.Camera.Model import cam_defs as defs
from Devices.Camera.Resources.cam_strings import LangEnum


class Controller(AbstractController):
    def __init__(self, cam_index: int = 0, lang: LangEnum = LangEnum.ENG, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self.cam_index = cam_index
        cam_name = "CAM_" + str(self.cam_index)
        view = CamView(cam_name, log_handlers)
        super().__init__(view)
        # TODO: Get logging in here. See https://docs.python.org/3/howto/logging-cookbook.html find multiprocessing.
        self._model_msg_pipe, msg_pipe = Pipe()  # For messages/commands.
        self._model_image_pipe, img_pipe = Pipe(False)  # For images.
        self._model = Process(target=CamModel, args=(msg_pipe, img_pipe, self.cam_index))
        # self._model = CamModel(cam_name, self.cam_index, log_handlers)
        self._tasks = []
        self._switcher = {defs.ModelEnum.FAILURE: self.err_cleanup,
                          defs.ModelEnum.CUR_FPS: self._update_view_fps,
                          defs.ModelEnum.CLEANUP: self._set_model_cleaned}
        self._stop = TEvent()
        self._loop = get_running_loop()
        self.set_lang(lang)
        self._model_cleaned = Event()
        self._ended = Event()
        executor = ThreadPoolExecutor(2)
        self._tasks.append(self._loop.run_in_executor(executor, self._update_view))
        self._tasks.append(self._loop.run_in_executor(executor, self._handle_pipe))
        self._model.start()
        self.send_msg_to_model((defs.ModelEnum.SET_USE_CAM, True))
        self._logger.debug("Initialized")

    def get_index(self) -> int:
        """
        Get this camera index.
        :return int: The camera index.
        """
        return self.cam_index

    def await_ended(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._ended)

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this device.
        :param lang: The language to use.
        :return None:
        """
        self._logger.debug("running")
        self.view.set_lang(lang)
        self._logger.debug("done")

    def err_cleanup(self) -> None:
        """
        Handle cleanup when camera fails.
        :return None:
        """
        self._logger.debug("running")
        self._logger.warning("Camera error occurred.")
        create_task(self.cleanup(True))
        self._logger.debug("done")

    async def cleanup(self, discard: bool = False) -> None:
        """
        Cleanup this object and prep for app closure.
        :param discard: Quit without saving.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.CLEANUP, discard))
        await self._model_cleaned.wait()
        self._stop.set()
        if self._model.is_alive():
            self._model.join()
        self._ended.set()
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

    def _handle_pipe(self) -> None:
        """
        Handle msgs from model.
        :return None:
        """
        self._logger.debug("running")
        try:
            while not self._stop.isSet():
                if self._model_msg_pipe.poll():
                    msg = self._model_msg_pipe.recv()
                    if msg[1] is not None:
                        self._loop.call_soon_threadsafe(self._switcher[msg[0]], msg[1])
                    else:
                        self._loop.call_soon_threadsafe(self._switcher[msg[0]])
                sleep(1)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

    def _update_view(self) -> None:
        """
        Update view with latest image from camera.
        :return None:
        """
        self._logger.debug("running")
        try:
            while not self._stop.isSet():
                next_image = None
                while self._model_image_pipe.poll():
                    next_image = self._model_image_pipe.recv()
                if next_image is not None:
                    self._loop.call_soon_threadsafe(self.view.update_image, self.convert_frame_to_qt_image(next_image))
                sleep(.008)
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

    def _set_model_cleaned(self) -> None:
        """
        Set flag that model is done with cleanup.
        :return None:
        """
        self._logger.debug("running")
        self._model_cleaned.set()
        self._logger.debug("done")

    def send_msg_to_model(self, msg) -> None:
        """
        A wrapper for pipe.send()
        :param msg:
        :return:
        """
        try:
            self._model_msg_pipe.send(msg)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

    @staticmethod
    def convert_frame_to_qt_image(frame: ndarray) -> QPixmap:
        """
        Convert image to suitable format for display in Qt.
        :param frame: The image to convert.
        :return QPixmap: The converted image.
        """
        rgb_image = cvtColor(frame, COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        res = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        ret = QPixmap.fromImage(res)
        return ret
