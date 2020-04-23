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
from asyncio import Event, create_task
from queue import Queue
# from PySide2.QtWidgets import *
# from PySide2.QtGui import *
from PySide2.QtCore import QSettings, QSize
from Model.app_model import AppModel
from Model.app_defs import current_version, log_format, RS_Devices
from Model.app_helpers import setup_log_file
from Model.strings_english import log_out_filename, company_name, app_name, logging_version_identifier
from Model.rs_device_com_scanner import RSDeviceCommScanner
from View.OutputLogWindow.output_window import OutputWindow
from View.MainWindow.main_window import AppMainWindow
from View.MenuBarWidget.menu_bar import AppMenuBar
from View.MainWindow.button_box import ButtonBox
from View.MainWindow.info_box import InfoBox
from View.MainWindow.drive_info_box import DriveInfoBox
from View.MainWindow.flag_box import FlagBox
from View.MainWindow.note_box import NoteBox


# TODO: Figure out logging for asyncio
class AppController:
    def __init__(self):
        # App settings and logging.
        self.__settings = QSettings(company_name, app_name)
        self.__settings.beginGroup("logging")
        # TODO: Give user control over logging level
        if not self.__settings.contains("level"):
            self.__settings.setValue("level", "DEBUG")
        log_level = eval('logging.' + self.__settings.value('level'))
        self.__settings.endGroup()
        logging.basicConfig(filename=setup_log_file(log_out_filename), filemode='w', level=log_level, format=log_format)
        self.logger = logging.getLogger(__name__)
        self.log_output = OutputWindow()
        self.formatter = logging.Formatter(log_format)
        self.ch = logging.StreamHandler(self.log_output)
        self.ch.setLevel(log_level)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        self.logger.info(logging_version_identifier + str(current_version))

        self.logger.debug("Initializing")
        # Flags
        self.__new_device_flag = Event()
        self.__device_conn_error_flag = Event()
        self.__close_event_flag = Event()

        # Model
        self.__new_device_queue = Queue()
        self.__model = AppModel()
        self.__dev_com_scanner = RSDeviceCommScanner(RS_Devices, self.__new_device_flag,
                                                     self.__device_conn_error_flag, self.__new_device_queue)

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

        self.__setup_handlers()
        self.__setup_flags()
        self.__initialize_view()
        self.__start()
        self.logger.debug("Initialized")

    # TODO: Figure out why this does not run every time.
    async def handle_new_devices(self) -> None:
        """
        Check for and handle any new Devices from the com scanner.
        :return: None
        """
        self.logger.debug("running")
        while True:
            print("waiting for new devices")
            await self.__new_device_flag.wait()
            print("Got new device")
            self.__new_device_flag.clear()

    async def handle_device_conn_error(self) -> None:
        """
        Alert user to device connection error
        :return: None
        """
        while True:
            await self.__device_conn_error_flag.wait()
            print("Error connecting")
            self.__device_conn_error_flag.clear()

    def __start(self) -> None:
        """
        Start all recurring functions.
        :return: None
        """
        create_task(self.handle_new_devices())
        create_task(self.handle_device_conn_error())
        self.__dev_com_scanner.start()

    def __setup_handlers(self) -> None:
        """
        Attach event handlers as needed.
        :return: None
        """
        self.logger.debug("running")
        self.logger.debug("done")

    def __setup_flags(self) -> None:
        """
        Attach event flags as needed.
        :return: None
        """
        self.logger.debug("running")
        self.main_window.add_close_handler(self.__close_handler)
        self.logger.debug("done")

    def __initialize_view(self) -> None:
        """
        Put the different components of the view together and then show the view.
        :return: None
        """
        self.logger.debug("running")
        self.main_window.add_menu_bar(self.menu_bar)
        self.menu_bar.add_log_window_handler(self.__log_window_handler)
        self.main_window.add_control_bar_widget(self.button_box)
        self.main_window.add_control_bar_widget(self.flag_box)
        self.main_window.add_control_bar_widget(self.note_box)
        self.main_window.add_control_bar_widget(self.info_box)
        self.main_window.add_control_bar_widget(self.d_info_box)
        self.main_window.show()

    def __log_window_handler(self) -> None:
        """
        Handler for the output log
        :return None:
        """
        self.logger.debug("running")
        self.log_output.show()
        self.logger.debug("done")

    def __close_handler(self):
        self.__dev_com_scanner.cleanup()
        create_task(self.__model.cleanup())
