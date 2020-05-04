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

import logging
from logging import DEBUG
from datetime import datetime
from asyncio import create_task, sleep
from aioserial import AioSerial
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QKeyEvent
from PySide2.QtCore import QSettings, QSize
from Model.app_model import AppModel
from Model.app_defs import current_version, log_format, LangEnum
from Model.app_helpers import setup_log_file, get_remaining_disk_size, format_current_time, end_tasks
from Resources.Strings.app_strings import strings, StringsEnum, company_name, app_name
from View.HelpWidgets.output_window import OutputWindow
from View.MainWindow.main_window import AppMainWindow
from View.ControlWidgets.menu_bar import AppMenuBar
from View.ControlWidgets.button_box import ButtonBox
from View.InfoWidgets.info_box import InfoBox
from View.InfoWidgets.drive_info_box import DriveInfoBox
from View.InfoWidgets.flag_box import FlagBox
from View.ControlWidgets.note_box import NoteBox
from View.DeviceDisplayWidgets.mdi_area import MDIArea


# TODO: Figure out logging for asyncio
class AppController:
    """ The main controller for this app. """
    def __init__(self):
        # App settings and logging.
        self._settings = QSettings(company_name, app_name)

        if not self._settings.contains("language"):
            self._settings.setValue("language", LangEnum.ENG)
        self._lang = self._settings.value("language")
        self._strings = strings[self._lang]

        self._settings.beginGroup("logging")
        if not self._settings.contains("level"):
            self._settings.setValue("level", DEBUG)
        log_level = self._settings.value('level')
        self._settings.endGroup()

        log_file = setup_log_file(self._strings[StringsEnum.LOG_OUT_NAME], self._strings[StringsEnum.PROG_OUT_HDR])
        logging.basicConfig(filename=log_file, filemode='w', level=log_level, format=log_format)
        self._logger = logging.getLogger(__name__)
        self.log_output = OutputWindow(self._lang)
        self.formatter = logging.Formatter(log_format)
        self.ch = logging.StreamHandler(self.log_output)
        self.ch.setLevel(log_level)
        self.ch.setFormatter(self.formatter)
        self._logger.addHandler(self.ch)
        self._logger.info(self._strings[StringsEnum.LOG_VER_ID] + str(current_version))

        self._logger.debug("Initializing")

        # View
        ui_min_size = QSize(950, 740)
        button_box_size = QSize(205, 120)
        info_box_size = QSize(230, 120)
        flag_box_size = QSize(80, 120)
        note_box_size = QSize(250, 120)
        drive_info_box_size = QSize(200, 120)
        self.main_window = AppMainWindow(ui_min_size, self.ch, self._lang)
        self.menu_bar = AppMenuBar(self.main_window, self.ch, self._lang)
        self.button_box = ButtonBox(self.main_window, button_box_size, self.ch, self._lang)
        self.info_box = InfoBox(self.main_window, info_box_size, self.ch, self._lang)
        self.d_info_box = DriveInfoBox(self.main_window, drive_info_box_size, self.ch, self._lang)
        self.flag_box = FlagBox(self.main_window, flag_box_size, self.ch, self._lang)
        self.note_box = NoteBox(self.main_window, note_box_size, self.ch, self._lang)
        self.mdi_area = MDIArea(self.main_window, self.ch)
        self._file_dialog = QFileDialog(self.main_window)

        # Model
        self._model = AppModel(self.ch, self._lang)

        # from PySide2.QtWidgets import QMdiSubWindow
        # for i in range(6):
        #     window = QMdiSubWindow()
        #     window.setFixedSize(300, 200)
        #     self.mdi_area.add_window(window)

        self._save_file_name = str()
        self._save_dir = str()
        self._tasks = []
        self._setup_handlers()
        self._initialize_view()
        self._start()
        self._logger.debug("Initialized")
        self._exp_created = False
        self._exp_running = False
        self._updater_task = None
        self._curr_cond_name = ""

    def language_change_handler(self, lang: LangEnum) -> None:
        """
        Sets the app language to the user selection.
        :return None:
        """
        self._logger.debug("running")
        self._settings.setValue("language", lang)
        self._strings = strings[lang]
        self.main_window.set_lang(lang)
        self.menu_bar.set_lang(lang)
        self.button_box.set_lang(lang)
        self.info_box.set_lang(lang)
        self.d_info_box.set_lang(lang)
        self.flag_box.set_lang(lang)
        self.note_box.set_lang(lang)
        self._model.change_lang(lang)
        self._logger.debug("done")

    def debug_change_handler(self, debug_level: str) -> None:
        """
        Sets the app debug level.
        :param debug_level: The debug level
        :return None:
        """
        print(__name__, "debug level changed")
        self._settings.setValue("logging/level", debug_level)
        self.main_window.show_help_window(self._strings[StringsEnum.APP_NAME], self._strings[StringsEnum.RESTART_PROG])

    def create_end_exp_handler(self) -> None:
        """
        Handler for create/end button.
        :return None:
        """
        self._logger.debug("running")
        if not self._exp_created:
            self._logger.debug("creating experiment")
            if not self._get_save_file_name():
                self._logger.debug("no save directory selected, done running _create_end_exp_handler()")
                return
            self._create_exp()
            self._logger.debug("done")
        else:
            self._logger.debug("ending experiment")
            self._end_exp()
            self._save_file_name = ""
        self._logger.debug("done")

    def start_stop_exp_handler(self) -> None:
        """
        Handler play/pause button.
        :return None:
        """
        self._logger.debug("running")
        if self._exp_running:
            self._logger.debug("stopping experiment")
            self._stop_exp()
        else:
            self._logger.debug("starting experiment")
            self._start_exp()
        self._logger.debug("done")

    async def new_device_view_handler(self) -> None:
        """
        Check for and handle any new device view objects from model.
        :return None:
        """
        self._logger.debug("running")
        dev_type: str
        dev_port: AioSerial
        while True:
            await self._model.await_new_view()
            ret, view = self._model.get_next_new_view()
            while ret:
                self.mdi_area.add_window(view)
                ret, view = self._model.get_next_new_view()

    async def remove_device_view_handler(self) -> None:
        """
        Check for and handle any device views to remove from model.
        :return None:
        """
        while True:
            await self._model.await_remove_view()
            ret, view = self._model.get_next_view_to_remove()
            while ret:
                self.mdi_area.remove_window(view)
                ret, view = self._model.get_next_view_to_remove()

    async def device_conn_error_handler(self) -> None:
        """
        Alert user to device connection error.
        :return None:
        """
        while True:
            await self._model.await_dev_con_err()
            self.main_window.show_help_window("Error", self._strings[StringsEnum.DEV_CON_ERR])

    # TODO: Implement
    def post_handler(self) -> None:
        """
        Handler for post button.
        :return:
        """
        self._logger.debug("running")
        print("Implement handling for this button.")
        self._logger.debug("done")

    # TODO: Implement
    def about_rs_handler(self) -> None:
        """
        Handler for about company button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    # TODO: Implement
    def about_app_handler(self) -> None:
        """
        Handler for about app button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    # TODO: Implement
    def check_for_updates_handler(self) -> None:
        """
        Handler for update button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def log_window_handler(self) -> None:
        """
        Handler for output log button.
        :return None:
        """
        self._logger.debug("running")
        self.log_output.show()
        self._logger.debug("done")

    # TODO: Implement
    def last_save_dir_handler(self) -> None:
        """
        Handler for last save dir button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    # TODO: Implement
    def toggle_cam_handler(self) -> None:
        """
        Handler for use cam button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    async def _update_drive_info_box(self):
        while True:
            info = get_remaining_disk_size(self._drive_path)
            self.d_info_box.set_name_val(str(info[0]))
            self.d_info_box.set_perc_val(str(info[1]))
            self.d_info_box.set_gb_val(str(info[2]))
            self.d_info_box.set_mb_val(str(info[3]))
            await sleep(2)

    def _create_exp(self) -> None:
        """
        Create an experiment. Signal devices and update view.
        :return None:
        """
        self._logger.debug("running")
        self._exp_created = self._model.signal_create_exp()
        if self._exp_created:
            self.button_box.set_start_button_enabled(True)
            self.button_box.set_create_button_state(1)
            self._check_toggle_post_button()
            if self._set_drive_updater():
                self._updater_task = create_task(self._update_drive_info_box())
            self.info_box.set_start_time(format_current_time(datetime.now(), time=True))
        else:
            self.button_box.set_create_button_state(0)
        self._logger.debug("done")

    def _end_exp(self) -> None:
        """
        End an experiment. Stop experiment if running then signal devices and update view.
        :return None:
        """
        self._logger.debug("running")
        self._exp_created = False
        if self._exp_running:
            self._stop_exp()
        self._model.signal_end_exp()
        self._check_toggle_post_button()
        if self._updater_task:
            self._updater_task.cancel()
            self._updater_task = None
        self.info_box.set_block_num(0)
        self.button_box.set_create_button_state(0)
        self.button_box.set_start_button_enabled(False)
        self.button_box.set_start_button_state(0)
        self._logger.debug("done")

    # TODO implement _add_break_in_graph_lines()?
    def _start_exp(self) -> None:
        """
        Start an experiment if one has been created. Signal devices and update view.
        :return None:
        """
        self._logger.debug("running")
        self._exp_running = self._model.signal_start_exp()
        if not self._exp_running:
            return
        self.info_box.set_block_num(str(int(self.info_box.get_block_num()) + 1))
        self.button_box.set_start_button_state(1)
        self.button_box.set_condition_name_box_enabled(False)
        self._curr_cond_name = self.button_box.get_condition_name()
        self._logger.debug("done")

    def _stop_exp(self) -> None:
        """
        Stop an experiment. Signal devices and update view.
        :return None:
        """
        self._logger.debug("running")
        self._exp_running = False
        self._model.signal_stop_exp()
        self.button_box.set_start_button_state(2)
        self.button_box.set_condition_name_box_enabled(True)
        self._logger.debug("done")

    def _set_drive_updater(self, filename: str = None) -> bool:
        """
        Update drive info display with drive information.
        :param filename: The drive to look at.
        :return None:
        """
        ret = True
        if not filename and not self._save_dir == "":
            self._drive_path = self._save_dir
        elif len(filename) > 0:
            self._drive_path = filename
        else:
            ret = False
        return ret

    def _check_toggle_post_button(self) -> None:
        """
        If an experiment is created and running and there is a note then allow user access to post button.
        :return None:
        """
        self._logger.debug("running")
        if self._exp_created and len(self.note_box.get_note()) > 0:
            self._logger.debug("button = true")
            self.note_box.set_post_button_enabled(True)
        else:
            self._logger.debug("button = false")
            self.note_box.set_post_button_enabled(False)
        self._logger.debug("done")

    def _get_save_file_name(self) -> bool:
        """
        Saves a save directory from a given file
        :return bool: True if the file name is longer than 1 character
        """
        self._logger.debug("running")
        self._save_file_name = self._file_dialog.getSaveFileName(filter="*.txt")[0]
        valid = len(self._save_file_name) > 1
        if valid:
            self._save_dir = self._get_save_dir_from_file_name(self._save_file_name)
        self._logger.debug("done")
        return valid

    def _get_save_dir_from_file_name(self, filename: str) -> str:
        """
        Return the path part only of the given absolute path filename.
        :param filename: The absolute path filename.
        :return str: The path only part of the filename.
        """
        self._logger.debug("running")
        end_index = filename.rfind('/')
        dir_name = filename[:end_index + 1]
        self._logger.debug("done")
        return dir_name

    def _keypress_handler(self, event: QKeyEvent) -> None:
        """
        Handle any keypress event and accept only alphabetical keypresses, then set flag_box to that key.
        :param event: The event to analyze and use.
        :return None:
        """
        self._logger.debug("running")
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.flag_box.set_flag(chr(event.key()))
            event.accept()
        else:
            event.ignore()
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        """
        Attach events to handlers
        :return None:
        """
        self._logger.debug("running")
        # Experiment controls
        self.button_box.add_create_button_handler(self.create_end_exp_handler)
        self.button_box.add_start_button_handler(self.start_stop_exp_handler)
        self.note_box.add_post_handler(self.post_handler)
        self.main_window.keyPressEvent = self._keypress_handler

        # File menu
        self.menu_bar.add_open_last_save_dir_handler(self.last_save_dir_handler)
        # self.menu_bar.add_cam_bool_handler(self.toggle_cam_handler)

        # Settings menu
        self.menu_bar.add_lang_select_handler(self.language_change_handler)
        self.menu_bar.add_debug_select_handler(self.debug_change_handler)

        # Help menu
        self.menu_bar.add_about_company_handler(self.about_rs_handler)
        self.menu_bar.add_about_app_handler(self.about_app_handler)
        self.menu_bar.add_update_handler(self.check_for_updates_handler)
        self.menu_bar.add_log_window_handler(self.log_window_handler)

        # Close app button
        self.main_window.add_close_handler(self._cleanup)

        self._logger.debug("done")

    def _initialize_view(self) -> None:
        """
        Put the different components of the view together and then show the view.
        :return None:
        """
        self._logger.debug("running")
        self.menu_bar.set_debug_action(self._settings.value("logging/level"))
        self.main_window.add_menu_bar(self.menu_bar)
        self.main_window.add_control_bar_widget(self.button_box)
        self.main_window.add_control_bar_widget(self.flag_box)
        self.main_window.add_control_bar_widget(self.note_box)
        self.main_window.add_spacer_item(1)
        self.main_window.add_control_bar_widget(self.info_box)
        self.main_window.add_control_bar_widget(self.d_info_box)
        self.main_window.add_mdi_area(self.mdi_area)
        self.main_window.show()

    def _start(self) -> None:
        """
        Start all recurring functions.
        :return None:
        """
        self._tasks.append(create_task(self.new_device_view_handler()))
        self._tasks.append(create_task(self.device_conn_error_handler()))
        self._tasks.append(create_task(self.remove_device_view_handler()))
        self._model.start()

    def _cleanup(self) -> None:
        """
        Cleanup any code that would cause problems for shutdown and prep for app closure.
        :return None:
        """
        create_task(end_tasks(self._tasks))
        self._model.cleanup()
        self.log_output.close()
