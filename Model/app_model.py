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
Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

import os
import glob
import importlib.util
import zipfile
import tempfile
from logging import StreamHandler, getLogger
from datetime import datetime
from asyncio import Event, create_task, futures, get_running_loop
from aioserial import AioSerial
from Model.rs_device_com_scanner import RSDeviceCommScanner
from Model.cam_scanner import CamScanner
from Model.app_defs import LangEnum
from Model.app_helpers import await_event, end_tasks, write_line_to_file, format_current_time
from Model.version_checker import VersionChecker
from Devices.AbstractDevice.View.abstract_view import AbstractView


class AppModel:
    def __init__(self, lang: LangEnum = LangEnum.ENG, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._controllers = self.get_controllers()
        self._rs_dev_scanner = RSDeviceCommScanner(self.get_profiles(), log_handlers)
        self._cam_scanner = CamScanner(log_handlers)
        self._ver_check = VersionChecker(log_handlers)
        self._log_handlers = log_handlers
        self._new_dev_view_flag = Event()
        self._remove_dev_view_flag = Event()
        self._current_lang = lang
        self._temp_folder = None
        self._save_path = str()
        self._devs = dict()
        self._dev_inits = dict()
        self._new_dev_views = []
        self._remove_dev_views = []
        self._gatherable_tasks = []
        self._cancelable_tasks = []
        self._note_filename = "notes.csv"
        self._flag_filename = "flags.csv"
        self.exp_created = False
        self.exp_running = False
        self.saving = False
        self._make_cam_controller(0)
        self._logger.debug("Initialized")

    def await_new_view(self) -> futures:
        """
        Signal when there is a new view event.
        :return futures: If the flag is set.
        """
        return await_event(self._new_dev_view_flag)

    def await_remove_view(self) -> futures:
        """
        Signal when there is a remove view event.
        :return futures: If the flag is set.
        """
        return await_event(self._remove_dev_view_flag)

    def await_dev_con_err(self) -> futures:
        """
        Signal when there is a err connecting to rs device.
        :return futures: If the flag is set.
        """
        return self._rs_dev_scanner.await_err()

    def await_cam_con_err(self) -> futures:
        """
        Signal when there is a err connecting to camera.
        :return futures: If the flag is set.
        """
        return self._cam_scanner.await_err()

    def change_lang(self, lang: LangEnum) -> None:
        """
        Change the language new devices are initialized with.
        :param lang: The enum to use.
        :return None:
        """
        self._current_lang = lang
        self._signal_lang_change()

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set language in each device controller.
        :param lang: The enum for the language.
        :return: None.
        """
        for controller in self._devs.values():
            controller.set_lang(lang)

    def check_version(self) -> int:
        """

        :return bool: 1: update available, 0: up to date, -1: error checking.
        """
        return self._ver_check.check_version()

    def get_next_new_view(self) -> (bool, AbstractView):
        """
        Return the next new view if there is one.
        :return bool, AbstractView: If there is an element to return, The next element to return.
        """
        if len(self._new_dev_views) > 0:
            return True, self._new_dev_views.pop(0)
        return False, None

    def get_next_view_to_remove(self) -> (bool, AbstractView):
        """
        Return the next view to remove if there is one.
        :return bool, AbstractView: If there is an element to return, The next element to return.
        """
        if len(self._remove_dev_views) > 0:
            return True, self._remove_dev_views.pop(0)
        return False, None

    def save_note(self, note: str) -> None:
        """
        Save note to experiment note file if experiment created.
        :param note: The text to save.
        :return None:
        """
        if self.exp_created:
            timestamp = format_current_time(datetime.now(), True, True, True)
            line = timestamp + ", " + note
            create_task(write_line_to_file(self._temp_folder.name + "/" + self._note_filename, line))

    def save_flag(self, flag: str) -> None:
        """
        Save flag to experiment flag file if experiment created.
        :param flag: The flag to save.
        :return None:
        """
        if self.exp_created:
            timestamp = format_current_time(datetime.now(), True, True, True)
            line = timestamp + ", " + flag
            create_task(write_line_to_file(self._temp_folder.name + "/" + self._flag_filename, line))

    def signal_create_exp(self, path: str) -> None:
        """
        Call create_exp on all device controllers.
        :param path: The save dir for this experiment.
        :return bool: If there was an error.
        """
        self._logger.debug("running")
        devices_running = list()
        self._temp_folder = tempfile.TemporaryDirectory()
        self._save_path = path
        try:
            for controller in self._devs.values():
                controller.create_exp(self._temp_folder.name + "/")
                devices_running.append(controller)
            self._logger.debug("done")
            self.exp_created = True
        except Exception as e:
            self._logger.exception("Failed creating exp on a controller.")
            for controller in devices_running:
                controller.end_exp()
            self._temp_folder.cleanup()
            self.exp_created = False

    def signal_end_exp(self, save: bool = True) -> None:
        """
        Call end exp on all device controllers.
        :return bool: If there was an error.
        """
        self._logger.debug("running")
        try:
            for controller in self._devs.values():
                controller.end_exp()
            self._logger.debug("done")
            create_task(self._save_exp(save))
        except Exception as e:
            self._logger.exception("Failed ending exp on a controller.")
        self.exp_created = False

    def signal_start_exp(self) -> None:
        """
        Starts an experiment.
        :return bool: Return false if an experiment failed to start, otherwise return true.
        """
        self._logger.debug("running")
        devices = list()
        try:
            for controller in self._devs.values():
                controller.start_exp()
                devices.append(controller)
                self.exp_running = True
        except Exception as e:
            self._logger.exception("Failed trying to start exp on controller.")
            for controller in devices:
                controller.end_exp()
                self.exp_running = False

    def signal_stop_exp(self) -> None:
        """
        Stops an experiment.
        :return bool: Return false if an experiment failed to stop, otherwise return true.
        """
        self._logger.debug("running")
        try:
            for controller in self._devs.values():
                controller.stop_exp()
        except Exception as e:
            self._logger.exception("Failed trying to stop exp on controller")
        self.exp_running = False

    async def _await_new_devs(self) -> None:
        """
        Wait for and handle new devices.
        :return None:
        """
        while True:
            await self._rs_dev_scanner.await_connect()
            self._setup_new_devices()

    async def _await_remove_devs(self) -> None:
        """
        Wait for and handle devices to remove.
        :return None:
        """
        while True:
            await self._rs_dev_scanner.await_disconnect()
            self._remove_lost_devices()

    async def _await_new_cams(self) -> None:
        """
        Wait for and handle new cameras.
        :return None:
        """
        while True:
            await self._cam_scanner.await_connect()
            self._setup_new_cams()

    async def _await_remove_cams(self) -> None:
        """
        Wait for and handle cameras to remove.
        :return None:
        """
        while True:
            await self._cam_scanner.await_disconnect()
            self._remove_lost_devices()

    async def _save_exp(self, save: bool) -> None:
        """
        Save the latest exp and cleanup temp folder.
        :param save: Should experiment data be saved.
        :return None:
        """
        self.saving = True
        if save:
            await get_running_loop().run_in_executor(None, self._convert_to_rs_file)
        self._temp_folder.cleanup()
        self.saving = False

    def _convert_to_rs_file(self) -> None:
        """
        Transfer latest experiment data to .rs file.
        :return None:
        """
        with zipfile.ZipFile(self._save_path, "w") as zipper:
            for file in os.listdir(self._temp_folder.name):
                zipper.write(self._temp_folder.name + "/" + file, file)

    def _signal_lang_change(self) -> bool:
        """
        Change language each device is using.
        :return None:
        """
        self._logger.debug("running")
        try:
            for controller in self._devs.values():
                controller.set_lang(self._current_lang)
            return True
        except Exception as e:
            self._logger.exception("Failed trying to stop exp on controller")
            return False

    def _setup_new_devices(self) -> None:
        """
        Get new device info from new device queue and make new device.
        :return: None.
        """
        self._logger.debug("running")
        ret, item = self._rs_dev_scanner.get_next_new_com()
        while ret:
            dev_type, connection = item[0], item[1]
            self._make_device(dev_type, connection)
            ret, item = self._rs_dev_scanner.get_next_new_com()
        self._logger.debug("done")

    def _make_device(self, dev_type: str, conn: AioSerial) -> None:
        """
        Make new controller for dev_type.
        :param dev_type: The type of device.
        :param conn: The device connection.
        :return None:
        """
        self._logger.debug("running")
        if dev_type not in self._controllers.keys():
            self._logger.warning("Could not recognize device type")
            return
        ret = self._make_rs_controller(conn, dev_type)
        if not ret:
            self._logger.warning("Failed making controller for type: " + dev_type)
            return
        self._logger.debug("done")

    def _make_rs_controller(self, conn: AioSerial, dev_type) -> bool:
        """
        Create controller of type dev_type
        :param conn: The com connection for this device.
        :param dev_type: The type of device.
        :return bool: Success of controller creation.
        """
        self._logger.debug("running")
        ret = True
        try:
            controller = self._controllers[dev_type](conn, self._current_lang, self._log_handlers)
            self._devs[conn.port] = controller
            self._new_dev_views.append(controller.get_view())
            self._new_dev_view_flag.set()
        except Exception as e:
            self._logger.exception("Problem making controller")
            ret = False
        self._logger.debug("done")
        return ret

    def _setup_new_cams(self) -> None:
        """
        Get new device info from new device queue and make new device.
        :return: None.
        """
        self._logger.debug("running")
        ret, cam_index = self._cam_scanner.get_next_new_cam()
        while ret:
            self._make_cam_controller(cam_index)
            ret, cam_index = self._rs_dev_scanner.get_next_new_com()
        self._logger.debug("done")

    def _make_cam_controller(self, cam_index: int) -> bool:
        """
        Create controller of type camera
        :param cam_index: The camera index to use.
        :return:
        """
        self._logger.debug("running")
        ret = True
        try:
            controller = self._controllers["Camera"](cam_index, self._current_lang, self._log_handlers)
            self._devs[cam_index] = controller
            self._new_dev_views.append(controller.get_view())
            self._new_dev_view_flag.set()
        except Exception as e:
            self._logger.exception("Problem making controller")
            ret = False
        self._logger.debug("done")
        return ret

    def _remove_lost_devices(self) -> None:
        """
        For any lost device, destroy controller and signal view removal to controller.
        :return: None.
        """
        self._logger.debug("running")
        ret, item = self._rs_dev_scanner.get_next_lost_com()
        to_remove = []
        while ret:
            for key in self._devs:
                conn = self._devs[key].get_conn()
                if conn and conn.port == item.device:
                    self._remove_dev_views.append(self._devs[key].get_view())
                    self._devs[key].cleanup()
                    to_remove.append(key)
                    self._remove_dev_view_flag.set()
                    break
            ret, item = self._rs_dev_scanner.get_next_lost_com()
        if len(to_remove) > 0:
            for ele in to_remove:
                del self._devs[ele]
        self._logger.debug("done")

    def _remove_lost_cams(self) -> None:
        """
        For any lost camera, destroy controller and signal view removal to controller.
        :return None:
        """
        pass
        self._logger.debug("running")
        ret, cam_index = self._cam_scanner.get_next_lost_cam()
        to_remove = []
        while ret:
            if cam_index in self._devs.keys():
                self._remove_dev_views.append(self._devs[cam_index].get_view())
                self._devs[cam_index].cleanup()
                to_remove.append(cam_index)
                self._remove_dev_view_flag.set()
            ret, cam_index = self._cam_scanner.get_next_lost_cam()
        if len(to_remove) > 0:
            for ele in to_remove:
                del self._devs[ele]
        self._logger.debug("done")

    def start(self) -> None:
        """
        Create all async tasks this model requires.
        :return None:
        """
        self._logger.debug("running")
        self._gatherable_tasks.append(create_task(self._await_new_devs()))
        self._gatherable_tasks.append(create_task(self._await_remove_devs()))
        self._rs_dev_scanner.start()
        self._logger.debug("done")

    def cleanup(self) -> None:
        """
        End all async tasks that are running and cleanup any other things that might cause shutdown errors.
        :return None:
        """
        self._logger.debug("running")
        self._rs_dev_scanner.cleanup()
        if self.exp_running:
            self.signal_stop_exp()
        if self.exp_created:
            self.signal_end_exp(False)
        while self.saving:
            continue
        for dev in self._devs.values():
            dev.cleanup()
        for task in self._cancelable_tasks:
            task.cancel()
        create_task(end_tasks(self._gatherable_tasks))
        self._logger.debug("done")

    # TODO add debugging
    @staticmethod
    def get_profiles() -> dict:
        """
        Iteratively search for any devices and get the profiles for those devices.
        :return dict: The list of keyval pairs {device name: device profile}
        """
        profs = {}
        # TODO: Handle when not under asyncCompanion directory
        while not os.getcwd().endswith("asyncCompanion"):  # Make sure we are in the right directory.
            os.chdir(os.pardir)
        for device in os.listdir('Devices'):
            if device != "AbstractDevice":
                fpath = glob.glob("Devices/" + device + "/Model/*defs.py")
                if fpath:
                    spec = importlib.util.spec_from_file_location("stuff", fpath[0])
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    try:
                        profs.update(mod.profile)
                    except Exception as e:
                        pass
        return profs

    # TODO add debugging
    @staticmethod
    def get_controllers() -> dict:
        """
        Iteratively search for any devices and get the controller classes for those devices.
        :return dict: The list of keyval pairs {device name: device controller class}
        """
        controllers = {}
        # TODO: Handle when not under asyncCompanion directory
        while not os.getcwd().endswith("asyncCompanion"):  # Make sure we are in the right directory.
            os.chdir(os.pardir)
        for device in os.listdir('Devices'):
            if device != "AbstractDevice":
                fpath = glob.glob("Devices/" + device + "/Controller/*controller.py")
                if fpath:
                    spec = importlib.util.spec_from_file_location(device, fpath[0])
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    controllers.update({device: mod.Controller})
        return controllers
