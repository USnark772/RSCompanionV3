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

import logging
from importlib import import_module
from asyncio import Event, create_task
from queue import Queue
from aioserial import AioSerial
from PySide2.QtCore import QSettings, QSize
from Model.app_model import AppModel
from Model.app_defs import current_version, log_format
from Model.app_helpers import setup_log_file
from Model.strings_english import log_out_filename, company_name, app_name, log_version_id, device_connection_error
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
        drive_info_box_size = QSize(250, 120)
        self.main_window = AppMainWindow(ui_min_size, self.ch)
        self.menu_bar = AppMenuBar(self.main_window, self.ch)
        self.button_box = ButtonBox(self.main_window, button_box_size, self.ch)
        self.info_box = InfoBox(self.main_window, info_box_size, self.ch)
        self.d_info_box = DriveInfoBox(self.main_window, drive_info_box_size, self.ch)
        self.flag_box = FlagBox(self.main_window, flag_box_size, self.ch)
        self.note_box = NoteBox(self.main_window, note_box_size, self.ch)
        self.mdi_area = MDIArea(self.main_window, self.ch)

        # Flags
        self._new_dev_flag = Event()
        self._dev_conn_err_flag = Event()
        self._close_flag = Event()

        # Model
        self._model = AppModel(self._new_dev_flag, self._dev_conn_err_flag, self._close_flag, self.mdi_area, self.ch)

        self._setup_handlers()
        self._initialize_view()
        self._start()
        self._logger.debug("Initialized")

    async def handle_new_devices(self) -> None:
        """
        Check for and handle any new Devices from the com scanner.
        :return: None.
        """
        self._logger.debug("running")
        dev_type: str
        dev_port: AioSerial
        while True:
            await self._new_dev_flag.wait()
            # TODO: Handle new device here.
            self._model.add_new_device()
            self._new_dev_flag.clear()

    async def handle_device_conn_error(self) -> None:
        """
        Alert user to device connection error.
        :return: None.
        """
        while True:
            await self._dev_conn_err_flag.wait()
            self.main_window.show_help_window("Error", device_connection_error)
            self._dev_conn_err_flag.clear()

    def create_end_exp_handler(self) -> None:
        """
        Handler for create/end button.
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button.")
        self._logger.debug("done")

    def start_stop_exp_handler(self) -> None:
        """
        Handler play/pause button.
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button.")
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
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def about_app_handler(self) -> None:
        """
        Handler for about app button.
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def check_for_updates_handler(self) -> None:
        """
        Handler for update button.
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def log_window_handler(self) -> None:
        """
        Handler for output log button.
        :return: None.
        """
        self._logger.debug("running")
        self.log_output.show()
        self._logger.debug("done")

    def last_save_dir_handler(self) -> None:
        """
        Handler for last save dir button.
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    def toggle_cam_handler(self) -> None:
        """
        Handler for use cam button.
        :return: None.
        """
        self._logger.debug("running")
        print("Implement handling for this button")
        self._logger.debug("done")

    # TODO: Implement these.
    def create_exp(self):
        pass

    def end_exp(self):
        pass

    def start_exp(self):
        pass

    def stop_exp(self):
        pass

    def _setup_handlers(self) -> None:
        """
        Attach events to handlers
        :return: None.
        """
        self._logger.debug("running")
        # Control bar
        self.button_box.add_create_button_handler(self.create_end_exp_handler)
        self.button_box.add_start_button_handler(self.start_stop_exp_handler)
        self.note_box.add_post_handler(self.post_handler)

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
        :return: None.
        """
        self._logger.debug("running")
        self.main_window.add_menu_bar(self.menu_bar)
        self.main_window.add_control_bar_widget(self.button_box)
        self.main_window.add_control_bar_widget(self.flag_box)
        self.main_window.add_control_bar_widget(self.note_box)
        self.main_window.add_spacer_item(100000)
        self.main_window.add_control_bar_widget(self.info_box)
        self.main_window.add_control_bar_widget(self.d_info_box)
        self.main_window.add_mdi_area(self.mdi_area)
        self.main_window.show()

    def _start(self) -> None:
        """
        Start all recurring functions.
        :return: None.
        """
        create_task(self.handle_new_devices())
        create_task(self.handle_device_conn_error())
        self._model.start()

    def _cleanup(self) -> None:
        """
        Cleanup any code that would cause problems for shutdown and prep for app closure.
        :return: None.
        """
        self._model.cleanup()
