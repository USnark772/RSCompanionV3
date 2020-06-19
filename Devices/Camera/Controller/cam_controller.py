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
        self.view.show_initialization()
        self.view.set_config_active(False)
        # TODO: Get logging in here. See https://docs.python.org/3/howto/logging-cookbook.html find multiprocessing.
        self._model_msg_pipe, msg_pipe = Pipe()  # For messages/commands.
        self._model_image_pipe, img_pipe = Pipe(False)  # For images.
        self._model = Process(target=CamModel, args=(msg_pipe, img_pipe, self.cam_index))
        # TODO: Multiprocessing could cause issues when packaging app.
        self._switcher = {defs.ModelEnum.FAILURE: self.err_cleanup,
                          defs.ModelEnum.CUR_FPS: self._update_view_fps,
                          defs.ModelEnum.CUR_RES: self._update_view_resolution,
                          defs.ModelEnum.CLEANUP: self._set_model_cleaned,
                          defs.ModelEnum.STOP: self._set_saved,
                          defs.ModelEnum.STAT_UPD: self._show_init_progress,
                          defs.ModelEnum.START: self._finalize}
        self._stop = TEvent()
        self._loop = get_running_loop()
        self._model_cleaned = Event()
        self._ended = Event()
        self._executor = ThreadPoolExecutor(2)
        self._loop.run_in_executor(self._executor, self._handle_pipe)
        self._update_feed_flag = TEvent()
        self._update_feed_flag.set()
        self._handle_pipe_flag = TEvent()
        self._handle_pipe_flag.set()
        self._model.start()
        self._fps_inf = float("inf")
        self._fps_inf_str = "\u221e"
        self._max_fps = 30
        self.set_lang(lang)
        self._res_list = list()
        self.send_msg_to_model((defs.ModelEnum.INITIALIZE, None))
        self._setup_handlers()
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this device.
        :param lang: The language to use.
        :return None:
        """
        self._logger.debug("running")
        self.view.language = lang
        self.send_msg_to_model((defs.ModelEnum.LANGUAGE, lang))
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
        self.view.save_window_state()
        self._logger.debug("done")

    def await_saved(self) -> futures:
        """
        Signal main app that this device data has been saved.
        :return futures: Event to signal saving done.
        """
        return await_event(self.saved)

    def create_exp(self, path: str, cond_name: str) -> None:
        """
        Handle experiment created for this device.
        :param path: The path to use to save data.
        :param cond_name: The optional condition name for this experiment.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.COND_NAME, cond_name))
        self.view.set_config_active(False)
        self.send_msg_to_model((defs.ModelEnum.START, path))
        self._logger.debug("done")

    def end_exp(self) -> None:
        """
        Handle experiment ended for this device.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.STOP, None))
        self.view.set_config_active(True)
        self._logger.debug("done")

    def start_exp(self, block_num: int) -> None:
        """
        Handle start exp signal for this camera.
        :param block_num: The current block number.
        :return None:
        """
        self._logger.debug("running")
        print("")
        self.send_msg_to_model((defs.ModelEnum.BLOCK_NUM, block_num))
        self.send_msg_to_model((defs.ModelEnum.EXP_STATUS, True))
        self._logger.debug("done")

    def stop_exp(self) -> None:
        """
        Alert this camera when experiment stops.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.EXP_STATUS, False))
        self._logger.debug("done")

    def update_keyflag(self, flag: str) -> None:
        """
        Handle keflag changes for this camera.
        :param flag: The new flag.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.KEYFLAG, flag))
        self._logger.debug("done")

    def update_resolution(self) -> None:
        """
        Get resolution selection from View and pass to model.
        :return None:
        """
        self._logger.debug("running")
        cur_res = self.view.resolution
        for res in self._res_list:
            if res[0] == cur_res:
                self.send_msg_to_model((defs.ModelEnum.SET_RES, res[1]))
                break
        self._logger.debug("done")

    def update_fps(self) -> None:
        """
        Get fps selection from View and pass to model.
        :return None:
        """
        self._logger.debug("running")
        if self.view.fps == self._fps_inf_str:
            new_fps = self._fps_inf
        else:
            new_fps = float(self.view.fps)
        self.send_msg_to_model((defs.ModelEnum.SET_FPS, new_fps))
        self._logger.debug("done")

    def update_show_feed(self) -> None:
        """
        Get show feed bool from view and pass to model.
        :return None:
        """
        self._logger.debug("running")
        if not self.view.use_feed or not self.view.use_cam:
            self._update_feed_flag.clear()
            self.view.update_image(msg="No Feed")
        elif self.view.use_feed and self.view.use_cam:
            self._update_feed_flag.set()
        self.send_msg_to_model((defs.ModelEnum.SET_USE_FEED, self.view.use_feed and self.view.use_cam))
        self._logger.debug("done")

    def update_use_cam(self) -> None:
        """
        Set this camera active or inactive.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.SET_USE_CAM, self.view.use_cam))
        self.update_show_feed()
        self._logger.debug("done")

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

    def err_cleanup(self) -> None:
        """
        Handle cleanup when camera fails.
        :return None:
        """
        self._logger.debug("running")
        self._logger.warning("Camera error occurred.")
        create_task(self.cleanup(True))
        self._logger.debug("done")

    def _set_saved(self) -> None:
        """
        Set saved signal.
        :return None:
        """
        self._loop.call_soon_threadsafe(self.saved.set())

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
                    if msg[0] in self._switcher.keys():
                        if msg[1] is not None:
                            self._loop.call_soon_threadsafe(self._switcher[msg[0]], msg[1])
                        else:
                            self._loop.call_soon_threadsafe(self._switcher[msg[0]])
                sleep(1)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass
        except Exception as e:
            raise e

    def _update_feed(self) -> None:
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
                if next_image is not None and self._update_feed_flag.isSet():
                    converted_image = self.convert_image_to_qt_format(next_image)
                    self._loop.call_soon_threadsafe(self.view.update_image, converted_image)
                sleep(.008)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass

    def _show_init_progress(self, progress: int) -> None:
        """
        Update user on camera initialization progress.
        :param progress: The latest progress update.
        :return None:
        """
        self.view.update_init_bar(progress)

    def _finalize(self, init_results: list) -> None:
        """
        Tell model to start. Tell view to show images.
        :param init_results: List of resolutions supported by the camera.
        :return None:
        """
        self._logger.debug("running")
        self._loop.run_in_executor(self._executor, self._update_feed)
        self.send_msg_to_model((defs.ModelEnum.SET_USE_CAM, True))
        self.send_msg_to_model((defs.ModelEnum.SET_USE_FEED, True))
        self._max_fps = init_results[0]
        fps_list = [str(x) for x in range(1, self._max_fps + 1)]
        fps_list.append(self._fps_inf_str)
        res_list = init_results[1]
        # res_list = init_results
        self._res_list = [((str(x[0]) + ", " + str(x[1])), x) for x in res_list]
        self.view.resolution_list = [x[0] for x in self._res_list]
        self.view.fps_list = fps_list
        self.send_msg_to_model((defs.ModelEnum.SET_FPS, self._fps_inf))
        self.send_msg_to_model((defs.ModelEnum.GET_FPS, None))
        self.send_msg_to_model((defs.ModelEnum.GET_RES, None))
        self.view.set_config_active(True)
        self.view.show_images()
        self._logger.debug("done")

    def _update_view_fps(self, new_fps: int) -> None:
        """
        Update view object fps display with new value.
        :param new_fps: The new value.
        :return None:
        """
        self._logger.debug("running")
        if new_fps > self._max_fps:
            new_fps = self._fps_inf_str
        else:
            new_fps = str(new_fps)
        self.view.fps = new_fps
        self._logger.debug("done")

    def _update_view_resolution(self, new_resolution: tuple) -> None:
        """
        Update view object resolution display with new value.
        :param new_resolution: The new value.
        :return None:
        """
        self._logger.debug("running")
        for res in self._res_list:
            if res[1] == new_resolution:
                self.view.resolution = res[0]
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        """
        Connect handlers to view object.
        :return None:
        """
        self._logger.debug("running")
        self.view.set_fps_selector_handler(self.update_fps)
        self.view.set_resolution_selector_handler(self.update_resolution)
        self.view.set_show_feed_button_handler(self.update_show_feed)
        self.view.set_use_cam_button_handler(self.update_use_cam)
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
        except Exception as e:
            raise e

    @staticmethod
    def convert_image_to_qt_format(image: ndarray) -> QPixmap:
        """
        Convert image to suitable format for display in Qt.
        :param image: The image to convert.
        :return QPixmap: The converted image.
        """
        rgb_image = cvtColor(image, COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        res = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        ret = QPixmap.fromImage(res)
        return ret
