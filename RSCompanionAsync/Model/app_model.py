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
import importlib.util
from shutil import move
from pathlib import Path
import tempfile
from logging import StreamHandler, getLogger
from datetime import datetime
from asyncio import Event, create_task, futures, get_running_loop
from aioserial import AioSerial
from RSCompanionAsync.Model.rs_device_com_scanner import RSDeviceCommScanner
from RSCompanionAsync.Model.cam_scanner import CamScanner
import RSCompanionAsync.Model.app_defs as defs
from RSCompanionAsync.Resources.Strings.note_box_strings import strings as note_strings, StringsEnum as NoteEnum
from RSCompanionAsync.Resources.Strings.flag_box_strings import strings as flag_strings, StringsEnum as FlagEnum
from RSCompanionAsync.Resources.Strings.main_window_strings import strings, StringsEnum
from RSCompanionAsync.Model.app_helpers import await_event, write_line_to_file, format_current_time
from RSCompanionAsync.Model.version_checker import VersionChecker
from RSCompanionAsync.Model.rs_file_saver import RSSaver
from RSCompanionAsync.Devices.AbstractDevice.View.abstract_view import AbstractView


class AppModel:
    def __init__(self, lang: defs.LangEnum = defs.LangEnum.ENG, log_handlers: [StreamHandler] = None):
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
        self._done_saving_flag = Event()
        self._saving_flag = Event()
        self._current_lang = lang
        self._saver = RSSaver(lang, log_handlers)
        self._save_path = str()
        self._devs = dict()
        self._dev_inits = dict()
        self._new_dev_views = []
        self._remove_dev_views = []
        self._tasks = []
        self._saving = False
        self._running = True
        self._block_num = 0
        self._cond_name = str()
        self.exp_created = False
        self.exp_running = False
        self._flag_filename = "flags.csv"
        self._note_filename = "notes.csv"
        self._events_filename = "events.csv"
        self._first_note = True
        self._first_flag = True
        self._main_strings = strings[lang]
        self._note_strings = note_strings[lang]
        self._flag_strings = flag_strings[lang]
        self._loop = get_running_loop()
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

    def change_lang(self, lang: defs.LangEnum) -> None:
        """
        Change the language new devices are initialized with.
        :param lang: The enum to use.
        :return None:
        """
        self._current_lang = lang
        self._main_strings = strings[lang]
        self._flag_strings = flag_strings[lang]
        self._note_strings = note_strings[lang]
        self._signal_lang_change()

    def set_lang(self, lang: defs.LangEnum) -> None:
        """
        Set language in each device controller.
        :param lang: The enum for the language.
        :return: None.
        """
        self._flag_strings = flag_strings[lang]
        self._note_strings = note_strings[lang]
        self._saver.set_lang(lang)
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
            if self._first_note:
                self._first_note = False
                create_task(write_line_to_file(self._save_path + self._note_filename,
                                               self._note_strings[NoteEnum.NOTE_HDR]))
            timestamp = datetime.now().timestamp()
            line = ", ".join([str(timestamp), note])
            create_task(write_line_to_file(self._save_path + self._note_filename, line))

    def send_keyflag_to_devs(self, flag: str) -> None:
        """
        Pass the new flag to devices.
        :param flag: The new flag.
        :return None:
        """
        self._logger.debug("running")
        for controller in self._devs.values():
            controller.update_keyflag(flag)
        self._logger.debug("done")

    def save_keyflag(self, flag: str) -> None:
        """
        Save flag to experiment flag file if experiment created.
        :param flag: The flag to save.
        :return None:
        """
        self._logger.debug("running")
        if self.exp_created:
            if self._first_flag:
                self._first_flag = False
                create_task(write_line_to_file(self._save_path + self._flag_filename,
                                               self._flag_strings[FlagEnum.FLAG_HDR]))
            line = ", ".join([str(datetime.now().timestamp()), flag])
            create_task(write_line_to_file(self._save_path + self._flag_filename, line))
        self._logger.debug("done")

    def save_exp_times(self, time: datetime, time_type: str, hdr: bool = False) -> None:
        """
        Save experiment create/end times, and experiment start/stop times.
        :param time: formatted experiment start time used for the save file
        :param time_type: ["create", "end", "start", "stop"]
        :param time: datetime to be recorded
        :param hdr: Whether this file needs a header before writing any other line.
        :return None:
        """
        self._logger.debug("running")
        if hdr:
            line = self._main_strings[StringsEnum.HDR]
            create_task(write_line_to_file(self._save_path + self._events_filename, line))
        line = ", ".join([str(time.timestamp()), time_type, self._cond_name, str(self._block_num)])
        create_task(write_line_to_file(self._save_path + self._events_filename, line))
        self._logger.debug("done")

    def signal_create_exp(self, path: str, cond_name: str, keyflag: str) -> None:
        """
        Call create_exp on all device controllers.
        :param path: The save dir for this experiment.
        :param cond_name: The optional condition name for this experiment.
        :param keyflag: The latest keyflag in effect.
        :return bool: If there was an error.
        """
        self._logger.debug("running")
        self._cond_name = cond_name
        self._first_flag = True
        self._first_note = True
        devices_running = list()
        now = datetime.now()
        exp_start_time = format_current_time(now, save=True)
        self._save_path = self._saver.start(path + "/experiment_" + exp_start_time)
        # self._flag_filename = "flags_" + exp_start_time + ".csv"
        # self._note_filename = "notes_" + exp_start_time + ".csv"
        # self._events_filename = "events_" + exp_start_time + ".csv"
        self.save_exp_times(now, self._main_strings[StringsEnum.CREATE], True)
        try:
            for controller in self._devs.values():
                controller.create_exp(self._save_path, self._cond_name)
                devices_running.append(controller)
            self._logger.debug("done")
            self.exp_created = True
            self._done_saving_flag.clear()
            self.send_keyflag_to_devs(keyflag)
            self.save_keyflag(keyflag)
        except Exception as e:
            self._logger.exception("Failed creating exp on a controller.")
            for controller in devices_running:
                controller.end_exp()
            self.exp_created = False

    def signal_end_exp(self) -> None:
        """
        Call end exp on all device controllers.
        :return bool: If there was an error.
        """
        self._logger.debug("running")
        self.save_exp_times(datetime.now(), self._main_strings[StringsEnum.END])
        try:
            for controller in self._devs.values():
                controller.end_exp()
            self._block_num = 0
            self._saving_flag.set()
            create_task(self._save_exp())
            self._logger.debug("done")
        except Exception as e:
            self._logger.exception("Failed ending exp on a controller.")
        self.exp_created = False

    def signal_start_exp(self, cond_name: str) -> None:
        """
        Starts an experiment.
        :param cond_name: The optional name for this block.
        :return bool: Return false if an experiment failed to start, otherwise return true.
        """
        self._logger.debug("running")
        devices = list()
        next_block_num = self._block_num + 1
        self._cond_name = cond_name
        try:
            for controller in self._devs.values():
                controller.start_exp(next_block_num, self._cond_name)
                devices.append(controller)
            self.exp_running = True
            self._block_num = next_block_num
            self.save_exp_times(datetime.now(), self._main_strings[StringsEnum.START])
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
        self.save_exp_times(datetime.now(), self._main_strings[StringsEnum.STOP])
        try:
            for controller in self._devs.values():
                controller.stop_exp()
        except Exception as e:
            self._logger.exception("Failed trying to stop exp on controller")
        self.exp_running = False

    def get_block_num(self) -> int:
        """
        :return int: The latest block number.
        """
        return self._block_num

    async def _await_new_devs(self) -> None:
        """
        Wait for and handle new devices.
        :return None:
        """
        while self._running:
            await self._rs_dev_scanner.await_connect()
            self._setup_new_devices()

    async def _await_remove_devs(self) -> None:
        """
        Wait for and handle devices to remove.
        :return None:
        """
        while self._running:
            await self._rs_dev_scanner.await_disconnect()
            await self._remove_lost_devices()

    async def _await_new_cams(self) -> None:
        """
        Wait for and handle new cameras.
        :return None:
        """
        while self._running:
            await self._cam_scanner.await_connect()
            await self._setup_new_cams()

    async def _await_remove_cam(self, cam_controller, cam_index: int) -> None:
        """
        Wait for and handle camera removal.
        :return None:
        """
        await cam_controller.await_ended()
        await self._remove_lost_cam(cam_index)
        self._cam_scanner.remove_cam_index(cam_index)

    async def _save_exp(self) -> None:
        """
        Save the latest exp and cleanup temp folder.
        :return None:
        """
        for device in self._devs.values():
            # print("app_model.py _save_exp() awaiting device: " + str(device) + ".await_saved()")
            await device.await_saved()
        x = await get_running_loop().run_in_executor(None, self._saver.stop)
        print("Got x:", x)
        self._saving_flag.clear()
        self._done_saving_flag.set()

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
            if self.exp_created:
                controller.create_exp(self._save_path, self._cond_name)
            if self.exp_running:
                controller.start_exp(self._block_num, self._cond_name)
        except Exception as e:
            self._logger.exception("Problem making controller")
            ret = False
        self._logger.debug("done")
        return ret

    async def _setup_new_cams(self) -> None:
        """
        Get new device info from new device queue and make new device.
        :return: None.
        """
        self._logger.debug("running")
        ret, cam_index = self._cam_scanner.get_next_new_cam()
        while ret:
            await self._make_cam_controller(cam_index)
            ret, cam_index = self._cam_scanner.get_next_new_cam()
        self._logger.debug("done")

    async def _make_cam_controller(self, cam_index: int) -> None:
        """
        Create controller of type camera
        :param cam_index: The camera index to use.
        :return None:
        """
        self._logger.debug("running")
        try:
            controller = self._controllers["Camera"](cam_index, self._current_lang, self._log_handlers)
            self._devs[cam_index] = controller
            self._tasks.append(create_task(self._await_remove_cam(controller, cam_index)))
            self._new_dev_views.append(controller.get_view())
            self._new_dev_view_flag.set()
            if self.exp_created:
                controller.create_exp(self._save_path, self._cond_name)
            if self.exp_running:
                controller.start_exp(self._block_num, self._cond_name)
        except Exception as e:
            self._logger.exception("Problem making controller")
        self._logger.debug("done")

    async def _remove_lost_devices(self) -> None:
        """
        For any lost device, destroy controller and signal view removal to controller.
        :return None:
        """
        self._logger.debug("running")
        ret, item = self._rs_dev_scanner.get_next_lost_com()
        to_remove = []
        while ret:
            for key in self._devs:
                conn = self._devs[key].get_conn()
                if conn and conn.port == item.device:
                    self._remove_dev_views.append(self._devs[key].get_view())
                    await self._devs[key].cleanup(True)
                    to_remove.append(key)
                    self._remove_dev_view_flag.set()
                    break
            ret, item = self._rs_dev_scanner.get_next_lost_com()
        if len(to_remove) > 0:
            for ele in to_remove:
                del self._devs[ele]
        self._logger.debug("done")

    async def _remove_lost_cam(self, cam_index: int) -> None:
        """
        Signal view removal to app controller and remove device controller.
        :return None:
        """
        self._logger.debug("running")
        self._remove_dev_views.append(self._devs[cam_index].get_view())
        self._remove_dev_view_flag.set()
        del self._devs[cam_index]
        self._logger.debug("done")

    def set_cams_active(self, is_active: bool) -> None:
        """
        Set whether this app looks for and uses cameras or not.
        :param is_active: Whether to look for and use cameras.
        :return None:
        """
        if is_active:
            self._activate_use_cams()
        else:
            self._deactivate_use_cams()

    def _deactivate_use_cams(self) -> None:
        """
        Disconnect any cameras currently connected to app and stop cam_scanner.
        :return None:
        """
        self._logger.debug("running")
        for o in self._devs.values():
            if 'Camera' in str(type(o)):
                create_task(o.cleanup())
        self._cam_scanner.deactivate()
        self._logger.debug("done")

    def _activate_use_cams(self) -> None:
        """
        Tell cam_scanner to activate.
        :return None:
        """
        self._logger.debug("running")
        self._cam_scanner.activate()
        self._logger.debug("done")

    def start(self) -> None:
        """
        Create all async tasks this model requires.
        :return None:
        """
        self._logger.debug("running")
        self._tasks.append(create_task(self._await_new_devs()))
        self._tasks.append(create_task(self._await_remove_devs()))
        self._tasks.append(create_task(self._await_new_cams()))
        self._rs_dev_scanner.start()
        self._cam_scanner.activate()
        self._logger.debug("done")

    async def cleanup(self) -> None:
        """
        End all async tasks that are running and cleanup any other things that might cause shutdown errors.
        :return None:
        """
        self._logger.debug("running")
        for task in self._tasks:
            task.cancel()
        await self._rs_dev_scanner.cleanup()
        await self._cam_scanner.cleanup()
        awaitables = list()
        for dev in self._devs.values():
            awaitables.append(create_task(dev.cleanup(True)))
        for awaitable in awaitables:
            await awaitable
        if self._saving_flag.is_set():
            await self._done_saving_flag.wait()
        self._logger.debug("done")

    # TODO add debugging
    @staticmethod
    def get_profiles() -> dict:
        """
        Iteratively search for any devices and get the profiles for those devices.
        :return dict: The list of keyval pairs {device name: device profile}
        """
        profiles = {}
        for listing in os.listdir(defs.dev_path):
            listing_path = defs.dev_path + listing
            if "Abstract" not in listing and os.path.isdir(listing_path):
                model_dir = listing_path + "/Model/"
                if os.path.isdir(model_dir):
                    for name in os.listdir(model_dir):
                        if "defs.py" in name:
                            fpath = model_dir + name
                            spec = importlib.util.spec_from_file_location(listing, fpath)
                            mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(mod)
                            try:
                                profiles.update(mod.profile)
                            except Exception as e:
                                pass
        return profiles

    # TODO add debugging
    @staticmethod
    def get_controllers() -> dict:
        """
        Iteratively search for any devices and get the controller classes for those devices.
        :return dict: The list of keyval pairs {device name: device controller class}
        """
        controllers = {}
        for listing in os.listdir(defs.dev_path):
            listing_path = defs.dev_path + listing
            if "Abstract" not in listing and os.path.isdir(listing_path):
                controller_dir = listing_path + "/Controller/"
                if os.path.isdir(controller_dir):
                    for name in os.listdir(controller_dir):
                        if "controller.py" in name:
                            fpath = controller_dir + name
                            spec = importlib.util.spec_from_file_location(listing, fpath)
                            mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(mod)
                            try:
                                controllers.update({listing: mod.Controller})
                            except Exception as e:
                                pass
        return controllers
