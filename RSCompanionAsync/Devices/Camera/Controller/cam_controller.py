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
from RSCompanionAsync.Model.app_helpers import await_event
from RSCompanionAsync.Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from RSCompanionAsync.Devices.Camera.View.cam_view import CamView
from RSCompanionAsync.Devices.Camera.Model.cam_model import CamModel
from RSCompanionAsync.Devices.Camera.Model import cam_defs as defs
from RSCompanionAsync.Devices.Camera.Resources.cam_strings import LangEnum


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
        self.send_msg_to_model((defs.ModelEnum.INITIALIZE, None))
        self.set_lang(lang)
        self._res_list = list()
        self._setup_handlers()
        self._exp_info_for_later = [str(), str(), 0]  # path, cond_name, block_num
        self._create_exp_later_task = None
        self._start_exp_later_task = None
        self._cleaning = False
        self._initialized = Event()
        self._running = False
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
        self._cleaning = True
        self.send_msg_to_model((defs.ModelEnum.CLEANUP, discard))
        await self._model_cleaned.wait()
        self._stop.set()
        if self._model.is_alive():
            self._model.join()
        self._ended.set()
        self.view.save_window_state()
        self._cleaning = False
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
        self._exp_info_for_later[0] = path
        self._exp_info_for_later[1] = cond_name
        if self._initialized.is_set():
            self.send_msg_to_model((defs.ModelEnum.COND_NAME, cond_name))
            self.view.set_config_active(False)
            self.send_msg_to_model((defs.ModelEnum.START, path))
            self._running = True
            self.saved.clear()
        else:
            if self._create_exp_later_task is not None:
                self._create_exp_later_task.cancel()
            self._create_exp_later_task = create_task(self._create_exp_later())
        self._logger.debug("done")

    async def _create_exp_later(self) -> None:
        """
        Wait until camera is initialized, then use create exp
        :param path:
        :param cond_name:
        :return:
        """
        await self._initialized.wait()
        self.create_exp(self._exp_info_for_later[0], self._exp_info_for_later[1])

    def end_exp(self) -> None:
        """
        Handle experiment ended for this device.
        :return None:
        """
        self._logger.debug("running")
        if self._running:
            self.send_msg_to_model((defs.ModelEnum.STOP, None))
            self.view.set_config_active(True)
            self.send_msg_to_model((defs.ModelEnum.BLOCK_NUM, 0))
            self._running = False
            if self._create_exp_later_task is not None:
                self._create_exp_later_task.cancel()
                self._create_exp_later_task = None
        self._logger.debug("done")

    def start_exp(self, block_num: int, cond_name: str) -> None:
        """
        Handle start exp signal for this camera.
        :param block_num: The current block number.
        :param cond_name: The name for this part of the experiment.
        :return None:
        """
        self._logger.debug("running")
        self._exp_info_for_later[1] = cond_name
        self._exp_info_for_later[2] = block_num
        if self._initialized.is_set():
            self.send_msg_to_model((defs.ModelEnum.BLOCK_NUM, block_num))
            self.send_msg_to_model((defs.ModelEnum.COND_NAME, cond_name))
            self.send_msg_to_model((defs.ModelEnum.EXP_STATUS, True))
        else:
            if self._start_exp_later_task is not None:
                self._start_exp_later_task.cancel()
            self._exp_info_for_later[1] = cond_name
            self._exp_info_for_later[2] = block_num
            self._start_exp_later_task = create_task(self._start_exp_later())
        self._logger.debug("done")

    async def _start_exp_later(self) -> None:
        """
        Wait until camera is initialized, then use start exp
        :param block_num:
        :param cond_name:
        :return:
        """
        await self._initialized.wait()
        self.start_exp(self._exp_info_for_later[2], self._exp_info_for_later[1])

    def stop_exp(self) -> None:
        """
        Alert this camera when experiment stops.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.EXP_STATUS, False))
        if self._create_exp_later_task is not None:
            self._create_exp_later_task.cancel()
            self._create_exp_later_task = None
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

    def update_cond_name(self, name: str) -> None:
        """
        Update condition name for this device.
        :param name: The new condition name.
        :return None:
        """
        self._logger.debug("running")
        self.send_msg_to_model((defs.ModelEnum.COND_NAME, name))
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

    def update_use_overlay(self) -> None:
        """
        Toggle whether overlay is being used on this camera.
        :return None:
        """
        self.send_msg_to_model((defs.ModelEnum.OVERLAY, self.view.use_overlay))

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
        if not self._cleaning:
            create_task(self.cleanup(True))
        self._logger.debug("done")

    def _set_saved(self) -> None:
        """
        Set saved signal.
        :return None:
        """
        self._loop.call_soon_threadsafe(self.saved.set)

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
        fps = init_results[0]
        fps_list = [str(x) for x in range(1, fps + 1)]
        res_list = init_results[1]
        self._res_list = [((str(x[0]) + ", " + str(x[1])), x) for x in res_list]
        self.view.resolution_list = [x[0] for x in self._res_list]
        self.view.fps_list = fps_list
        self.send_msg_to_model((defs.ModelEnum.SET_FPS, fps))
        self.send_msg_to_model((defs.ModelEnum.GET_FPS, None))
        self.send_msg_to_model((defs.ModelEnum.GET_RES, None))
        self.view.set_config_active(True)
        self.view.show_images()
        self._initialized.set()
        self._logger.debug("done")

    def _update_view_fps(self, new_fps: int) -> None:
        """
        Update view object fps display with new value.
        :param new_fps: The new value.
        :return None:
        """
        self._logger.debug("running")
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
        self.view.set_use_overlay_button_handler(self.update_use_overlay)
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
