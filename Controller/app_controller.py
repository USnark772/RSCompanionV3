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
from asyncio import Event, create_task, gather
from aioserial import AioSerial
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QKeyEvent
from PySide2.QtCore import QSettings, QSize
from Model.app_model import AppModel
from Model.app_defs import current_version, log_format, LangEnum
from Model.app_helpers import setup_log_file, get_remaining_disk_size, get_current_time
from Model.app_strings import log_out_filename, company_name, app_name, log_version_id, device_connection_error
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
        self._settings.beginGroup("logging")
        # TODO: Give user control over logging level
        if not self._settings.contains("level"):
            self._settings.setValue("level", "DEBUG")
        log_level = eval('logging.' + self._settings.value('level'))
        self._settings.endGroup()
        logging.basicConfig(filename=setup_log_file(log_out_filename), filemode='w', level=log_level, format=log_format)
        self._logger = logging.getLogger(__name__)
        self.log_output = OutputWindow()
        self.formatter = logging.Formatter(log_format)
        self.ch = logging.StreamHandler(self.log_output)
        self.ch.setLevel(log_level)
        self.ch.setFormatter(self.formatter)
        self._logger.addHandler(self.ch)
        self._logger.info(log_version_id + str(current_version))

        self._logger.debug("Initializing")

        # View
        ui_min_size = QSize(950, 740)
        button_box_size = QSize(205, 120)
        info_box_size = QSize(230, 120)
        flag_box_size = QSize(80, 120)
        note_box_size = QSize(250, 120)
        drive_info_box_size = QSize(200, 120)
        self.main_window = AppMainWindow(ui_min_size, self.ch)
        self.menu_bar = AppMenuBar(self.main_window, self.ch)
        self.button_box = ButtonBox(self.main_window, button_box_size, self.ch)
        self.info_box = InfoBox(self.main_window, info_box_size, self.ch)
        self.d_info_box = DriveInfoBox(self.main_window, drive_info_box_size, self.ch)
        self.flag_box = FlagBox(self.main_window, flag_box_size, self.ch)
        self.note_box = NoteBox(self.main_window, note_box_size, self.ch)
        self.mdi_area = MDIArea(self.main_window, self.ch)
        self._file_dialog = QFileDialog(self.main_window)

        # Flags
        self._new_dev_view_flag = Event()
        self._dev_conn_err_flag = Event()
        self._remove_dev_view_flag = Event()

        # Model
        self._model = AppModel(self._new_dev_view_flag, self._dev_conn_err_flag, self._remove_dev_view_flag,
                               self.mdi_area, self.ch)

        self._exp_created = False
        self._save_file_name = str()
        self._save_dir = str()
        self._tasks = []
        self._setup_handlers()
        self._initialize_view()
        self._start()
        self._logger.debug("Initialized")
        self._exp_running = False
        self._curr_cond_name = ""

    async def handle_new_device_view(self) -> None:
        """
        Check for and handle any new device view objects from model.
        :return None:
        """
        self._logger.debug("running")
        dev_type: str
        dev_port: AioSerial
        while True:
            await self._new_dev_view_flag.wait()
            self.mdi_area.add_window(self._model.get_next_new_view())
            if not self._model.has_unhandled_new_views():
                self._new_dev_view_flag.clear()

    async def remove_device_view(self) -> None:
        """
        Check for and handle any device views to remove from model.
        :return None:
        """
        while True:
            await self._remove_dev_view_flag.wait()
            self.mdi_area.remove_window(self._model.get_next_view_to_remove())
            if not self._model.has_unhandled_views_to_remove():
                self._remove_dev_view_flag.clear()

    async def handle_device_conn_error(self) -> None:
        """
        Alert user to device connection error.
        :return None:
        """
        while True:
            await self._dev_conn_err_flag.wait()
            self.main_window.show_help_window("Error", device_connection_error)
            self._dev_conn_err_flag.clear()

    def set_language_handler(self) -> None:
        """
        Sets the app language to the user selection.
        :return None:
        """
        # TODO: Get language setting and pass it in to model.set_lang()
        # self._model.set_lang()
        self._logger.debug("running")
        print("Implement handling for this button.")
        self._logger.debug("done")

    def create_end_exp_handler(self) -> None:
        """
        Handler for create/end button.
        :return None:
        """
        self._logger.debug("running")
        print(__name__, "create_end_exp_handler running")
        if not self._exp_created:
            self._logger.debug("creating experiment")
            if not self._get_save_file_name():
                print(__name__, "You didn't select a save directory.")
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

    def post_handler(self) -> None:
        """
        Handler for post button.
        :return:
        """
        self._logger.debug("running")
        print("Implement handling for this button.")
        self._logger.debug("done")

    def about_rs_handler(self) -> None:
        """
        Handler for about company button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def about_app_handler(self) -> None:
        """
        Handler for about app button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

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

    def last_save_dir_handler(self) -> None:
        """
        Handler for last save dir button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def toggle_cam_handler(self) -> None:
        """
        Handler for use cam button.
        :return None:
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def _create_exp(self) -> None:
        """
        Create an experiment.
        :return None:
        """
        self._logger.debug("running")
        self._update_drive_info_box()
        # self.menu_bar.set_cam_action_enabled(False)  # TODO: Implement cams
        date_time = get_current_time(device=True)
        self.button_box.toggle_create_button()
        self._exp_created = self._model.signal_create_exp()
        if self._exp_created:
            self._check_toggle_post_button()
            self.info_box.set_start_time(get_current_time(time=True, date_time=date_time))
        else:
            self.button_box.toggle_create_button()
            self._exp_created = False
        self._logger.debug("done")

    def _end_exp(self) -> None:
        """
        End an experiment.
        :return None:
        """
        self._logger.debug("running")
        self.__exp_created = False
        # self.menu_bar.set_cam_action_enabled(True)
        self.button_box.toggle_create_button()
        # use_cams = eval(self.settings.value('Camera manager/active'))   # TODO: Implement cams
        # if use_cams:
        #     self.__show_video_save_prog_bar()
        self._model.signal_end_exp()
        self._check_toggle_post_button()
        self.info_box.set_block_num(0)
        # self._check_device_backlog()  # TODO Add this functionality?
        self._update_drive_info_box()
        # if eval(self.settings.value("Camera manager/active")):
        #     self.button_box.setEnabled(False)
        self._logger.debug("done")

    def _start_exp(self) -> None:
        """
        Start an experiment.
        :return None:
        """
        self._logger.debug("running")
        self._exp_running = self._model.signal_start_exp()
        if not self._exp_running:
            return
        self.info_box.set_block_num(str(int(self.info_box.get_block_num()) + 1))
        self._curr_cond_name = self.button_box.get_condition_name()
        # TODO implement _add_break_in_graph_lines()?
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self._logger.debug("done")

    def _stop_exp(self) -> None:
        """
        Stop an experiment.
        :return None:
        """
        self._logger.debug("running")
        self._exp_running = False
        self._model.signal_stop_exp()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self._logger.debug("done")

    def _update_drive_info_box(self, filename: str = '') -> None:
        """
        Update drive info display with drive information.
        :param filename: The drive to look at.
        :return None:
        """
        if filename == '' and not self._save_dir == "":
            filename = self._save_dir
        info = get_remaining_disk_size(filename)
        self.d_info_box.set_name_val(str(info[0]))
        self.d_info_box.set_perc_val(str(info[1]))
        self.d_info_box.set_gb_val(str(info[2]))
        self.d_info_box.set_mb_val(str(info[3]))

    def _check_toggle_post_button(self) -> None:
        """
        If an experiment is created and running and there is a note then allow user access to post button.
        :return None:
        """
        self._logger.debug("running")
        if self._exp_created and len(self.note_box.get_note()) > 0:  # and self.__exp_running:
            self._logger.debug("button = true")
            self.note_box.toggle_post_button(True)
        else:
            self._logger.debug("button = false")
            self.note_box.toggle_post_button(False)
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
        self.menu_bar.add_cam_bool_handler(self.toggle_cam_handler)

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
        self._tasks.append(create_task(self.handle_new_device_view()))
        self._tasks.append(create_task(self.handle_device_conn_error()))
        self._tasks.append(create_task(self.remove_device_view()))
        self._model.start()

    def _cleanup(self) -> None:
        """
        Cleanup any code that would cause problems for shutdown and prep for app closure.
        :return None:
        """
        create_task(self.end_tasks())
        self._model.cleanup()

    async def end_tasks(self) -> None:
        """
        Cleanup all async loops
        :return None:
        """
        for task in self._tasks:
            task.cancel()
            await gather(self._tasks)
