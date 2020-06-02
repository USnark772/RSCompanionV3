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
from Model.logging_queue import setup_logging_queue
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QKeyEvent, QDesktopServices
from PySide2.QtCore import QSettings, QSize, QUrl, QDir
from Model.app_model import AppModel
from Model.app_defs import current_version, log_format, LangEnum
from Model.app_helpers import setup_log_file, get_disk_usage_stats, format_current_time
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
        self.app_lh = logging.StreamHandler(self.log_output)
        self.app_lh.setLevel(log_level)
        self.app_lh.setFormatter(self.formatter)
        self.stderr_lh = logging.StreamHandler()
        self.stderr_lh.setLevel(logging.WARNING)
        self.stderr_lh.setFormatter(self.formatter)
        self._logger.addHandler(self.app_lh)
        self._logger.addHandler(self.stderr_lh)
        self._logger.info(self._strings[StringsEnum.LOG_VER_ID] + str(current_version))
        setup_logging_queue()

        self._logger.debug("Initializing")

        # View
        ui_min_size = QSize(950, 740)
        button_box_size = QSize(205, 120)
        info_box_size = QSize(230, 120)
        flag_box_size = QSize(80, 120)
        note_box_size = QSize(250, 120)
        drive_info_box_size = QSize(200, 120)
        mdi_area_min_size = QSize(500, 300)
        self.main_window = AppMainWindow(ui_min_size, self._lang, [self.app_lh, self.stderr_lh])
        self.menu_bar = AppMenuBar(self.main_window, self._lang, [self.app_lh, self.stderr_lh])
        self.button_box = ButtonBox(self.main_window, button_box_size, self._lang, [self.app_lh, self.stderr_lh])
        self.info_box = InfoBox(self.main_window, info_box_size, self._lang, [self.app_lh, self.stderr_lh])
        self.d_info_box = DriveInfoBox(self.main_window, drive_info_box_size, self._lang, [self.app_lh, self.stderr_lh])
        self.flag_box = FlagBox(self.main_window, flag_box_size, self._lang, [self.app_lh, self.stderr_lh])
        self.note_box = NoteBox(self.main_window, note_box_size, self._lang, [self.app_lh, self.stderr_lh])
        self.mdi_area = MDIArea(self.main_window, mdi_area_min_size, [self.app_lh, self.stderr_lh])
        self._file_dialog = QFileDialog(self.main_window)

        # Model
        self._model = AppModel(self._lang, [self.app_lh, self.stderr_lh])

        self._save_file_name = str()
        self._save_dir = str()
        self._tasks = []
        self._setup_handlers()
        self._initialize_view()
        self._start()
        self._drive_updater_task = None
        self._curr_cond_name = ""
        self._logger.debug("Initialized")

    def window_layout_handler(self, layout: str) -> None:
        """
        Sets the subwindow layout to vertical or horizontal
        :param layout: string value of either "vertical" or "horizontal" to set layout
        :return None:
        """
        self._logger.debug("running")
        if layout == "horizontal":
            self.mdi_area.sort_windows_horizontal()
        elif layout == "vertical":
            self.mdi_area.sort_windows_vertical()
        elif layout == "tiled":
            self.mdi_area.sort_windows_tiled()
        elif layout == "cascade":
            self.mdi_area.sort_windows_cascade()
        self._logger.debug("done")

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
        self._settings.setValue("logging/level", debug_level)
        self.main_window.show_help_window(self._strings[StringsEnum.APP_NAME], self._strings[StringsEnum.RESTART_PROG])

    def create_end_exp_handler(self) -> None:
        """
        Handler for create/end button.
        :return None:
        """
        self._logger.debug("running")
        if not self._model.exp_created:
            self._logger.debug("creating experiment")
            if not self._get_save_file_name():
                self._logger.debug("no save directory selected, done running _create_end_exp_handler()")
                return
            self._create_exp()
            self.main_window.set_close_check(True)
            self._logger.debug("done")
        else:
            self._logger.debug("ending experiment")
            self._end_exp()
            self.main_window.set_close_check(False)
            self._save_file_name = ""
        self._logger.debug("done")

    def start_stop_exp_handler(self) -> None:
        """
        Handler play/pause button.
        :return None:
        """
        self._logger.debug("running")
        if self._model.exp_running:
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

    def post_handler(self) -> None:
        """
        Handler for post button.
        :return:
        """
        self._logger.debug("running")
        note = self.note_box.get_note()
        self.note_box.clear_note()
        self._model.save_note(note)
        self._logger.debug("done")

    def about_rs_handler(self) -> None:
        """
        Handler for about company button.
        :return None:
        """
        self._logger.debug("running")
        self.main_window.show_help_window(self._strings[StringsEnum.APP_NAME],
                                          self._strings[StringsEnum.ABOUT_COMPANY])
        self._logger.debug("done")

    def about_app_handler(self) -> None:
        """
        Handler for about app button.
        :return None:
        """
        self._logger.debug("running")
        self.main_window.show_help_window(self._strings[StringsEnum.APP_NAME],
                                          self._strings[StringsEnum.ABOUT_APP])
        self._logger.debug("done")

    def check_for_updates_handler(self) -> None:
        """
        Handler for update button.
        :return None:
        """
        self._logger.debug("running")
        ret = self._model.check_version()
        if ret == 1:
            self.main_window.show_help_window(self._strings[StringsEnum.UPDATE_HDR],
                                              self._strings[StringsEnum.UPDATE_AVAILABLE])
        elif ret == 0:
            self.main_window.show_help_window(self._strings[StringsEnum.UPDATE_HDR],
                                              self._strings[StringsEnum.NO_UPDATE])
        elif ret == -1:
            self.main_window.show_help_window(self._strings[StringsEnum.UPDATE_HDR_ERR],
                                              self._strings[StringsEnum.ERR_UPDATE_CHECK])
        self._logger.debug("done")

    def log_window_handler(self) -> None:
        """
        Handler for output log button.
        :return None:
        """
        self._logger.debug("running")
        self.log_output.show()
        self._logger.debug("done")

    def last_save_dir_handler(self) -> None:
        """
        Handler for last save dir button.
        :return None:
        """
        self._logger.debug("running")
        if self._save_dir == "":
            QDesktopServices.openUrl(QUrl.fromLocalFile(QDir().homePath()))
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self._save_dir))
        self._logger.debug("done")

    def exit_handler(self) -> None:
        """
        Handler for the exit button in the file menu.
        :return None:
        """
        self._logger.debug("running")
        self.main_window.close()
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

    async def _update_drive_info_box(self) -> None:
        """
        Periodically get info about drive currently being used to save data and display info on view.
        :return None:
        """
        while True:
            info = get_disk_usage_stats(self._drive_path)
            self.d_info_box.set_name_val(str(info[0]))
            self.d_info_box.set_perc_val(str(info[4]))
            self.d_info_box.set_gb_val(str(info[2]))
            self.d_info_box.set_mb_val(str(info[3]))
            await sleep(3)

    def _create_exp(self) -> None:
        """
        Create an experiment. Signal devices and update view.
        :return None:
        """
        self._logger.debug("running")
        self._model.signal_create_exp(self._save_file_name)
        if self._model.exp_created:
            self.button_box.set_start_button_enabled(True)
            self.button_box.set_create_button_state(1)
            self._check_toggle_post_button()
            if self._set_drive_updater():
                self._drive_updater_task = create_task(self._update_drive_info_box())
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
        if self._model.exp_running:
            self._stop_exp()
        self._model.signal_end_exp()
        self._check_toggle_post_button()
        if self._drive_updater_task:
            self._drive_updater_task.cancel()
            self._drive_updater_task = None
        self.info_box.set_block_num(0)
        self.button_box.set_create_button_state(0)
        self.button_box.set_start_button_enabled(False)
        self.button_box.set_start_button_state(0)
        self._logger.debug("done")

    def _start_exp(self) -> None:
        """
        Start an experiment if one has been created. Signal devices and update view.
        :return None:
        """
        self._logger.debug("running")
        self._model.signal_start_exp()
        if not self._model.exp_running:
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
        if self._model.exp_created and len(self.note_box.get_note()) > 0:
            self._logger.debug("button = true")
            self.note_box.set_post_button_enabled(True)
        else:
            self._logger.debug("button = false")
            self.note_box.set_post_button_enabled(False)
        self._logger.debug("done")

    def _get_save_file_name(self) -> bool:
        """
        Gets a new filename from the user for the current experiment to be saved as.
        :return bool: True if the file name is longer than 1 character
        """
        self._logger.debug("running")
        self._save_file_name = self._file_dialog.getSaveFileName(filter="*.rs")[0]
        valid = len(self._save_file_name) > 1
        if valid:
            self._save_dir = self._dir_name_from_file_name(self._save_file_name)
        self._logger.debug("done")
        return valid

    def _dir_name_from_file_name(self, filename: str) -> str:
        """
        Get directory name from filename.
        :param filename: The absolute path filename.
        :return str: The resulting directory name.
        """
        self._logger.debug("running")
        dir_name = filename[:filename.rindex("/")]
        self._logger.debug("done")
        return dir_name

    def _keypress_handler(self, event: QKeyEvent) -> None:
        """
        Handle any keypress event and intercept alphabetical keypresses, then set flag_box to that key.
        :param event: The keypress event.
        :return None:
        """
        self._logger.debug("running")
        if 0x41 <= event.key() <= 0x5a:
            self.flag_box.set_flag(chr(event.key()))
            self._model.save_keyflag(self.flag_box.get_flag())
        event.accept()
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
        self.note_box.add_note_box_changed_handler(self._check_toggle_post_button)
        self.note_box.add_post_handler(self.post_handler)
        self.main_window.keyPressEvent = self._keypress_handler

        # File menu
        self.menu_bar.add_open_last_save_dir_handler(self.last_save_dir_handler)
        # self.menu_bar.add_cam_bool_handler(self.toggle_cam_handler)
        self.menu_bar.add_exit_handler(self.exit_handler)

        # Settings menu
        self.menu_bar.add_lang_select_handler(self.language_change_handler)
        self.menu_bar.add_debug_select_handler(self.debug_change_handler)
        self.menu_bar.add_window_layout_handler(self.window_layout_handler)

        # Help menu
        self.menu_bar.add_about_company_handler(self.about_rs_handler)
        self.menu_bar.add_about_app_handler(self.about_app_handler)
        self.menu_bar.add_update_handler(self.check_for_updates_handler)
        self.menu_bar.add_log_window_handler(self.log_window_handler)

        # Close app button
        self.main_window.add_close_handler(self.cleanup)

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
        self._logger.debug("done")

    def _start(self) -> None:
        """
        Start all recurring functions.
        :return None:
        """
        self._tasks.append(create_task(self.new_device_view_handler()))
        self._tasks.append(create_task(self.device_conn_error_handler()))
        self._tasks.append(create_task(self.remove_device_view_handler()))
        self._model.start()

    def cleanup(self) -> None:
        """
        Handler for view close event.
        :return None:
        """
        self._logger.debug("running")
        create_task(self._cleanup())
        self._logger.debug("done")

    async def _cleanup(self) -> None:
        """
        Cleanup any code that would cause problems for shutdown and prep for app closure.
        :return None:
        """
        self._logger.debug("running")
        for task in self._tasks:
            task.cancel()
        await self._model.cleanup()
        if self._drive_updater_task:
            self._drive_updater_task.cancel()
        self.log_output.close()
        self.main_window.set_close_override(True)
        self._logger.debug("done")
        self.main_window.close()
