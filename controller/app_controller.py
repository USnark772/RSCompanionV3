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
from tempfile import gettempdir
from asyncio import create_task, sleep as a_sleep
from queue import Queue
# from PySide2.QtWidgets import *
# from PySide2.QtGui import *
from PySide2.QtCore import QSettings, QSize
from Model.app_model import AppModel
from Model.app_defs import current_version_str, logging_format
from Model.strings_english import program_output_hdr, logging_output_filename, company_name, app_name
from View.OutputLogWindow.output_window import OutputWindow
from View.MainWindow.main_window import AppMainWindow
from View.MenuBarWidget.menu_bar import AppMenuBar


class AppController:
    def __init__(self):
        self.__model = AppModel()
        self.log_output = OutputWindow()
        self.settings = QSettings(company_name, app_name)

        self.settings.beginGroup("logging")
        # TODO: Give user control over logging level
        if not self.settings.contains("level"):
            self.settings.setValue("level", "DEBUG")
        logginglevel = eval('logging.' + self.settings.value('level'))
        self.settings.endGroup()

        logging.basicConfig(filename=self.__model.setup_log_output_file(logging_output_filename), filemode='w',
                            level=logginglevel, format=logging_format)
        self.logger = logging.getLogger(__name__)

        self.formatter = logging.Formatter(logging_format)
        self.ch = logging.StreamHandler(self.log_output)
        self.ch.setLevel(logginglevel)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)

        self.logger.info("RS Companion app version: " + current_version_str)
        self.logger.debug("Initializing")

        ui_min_size = QSize(950, 740)
        self.main_window = AppMainWindow(ui_min_size, self.ch)
        self.menu_bar = AppMenuBar(self.main_window, self.ch)

        self.__setup_handlers()
        self.__initialize_view()
        self.logger.debug("Initialized")

    async def check_for_new_devices(self) -> None:
        """
        Check for and handle any new Devices from the com scanner.
        :return: None
        """
        self.logger.debug("running")
        while True:
            await a_sleep(1)

    def __setup_handlers(self) -> None:
        """
        Attach event handlers as needed.
        :return: None
        """
        self.logger.debug("running")
        # self.main_window.add_close_handler()
        pass

    def __initialize_view(self) -> None:
        """
        Put the different components of the view together and then show the view.
        :return: None
        """
        self.logger.debug("running")
        self.main_window.add_menu_bar(self.menu_bar)
        self.menu_bar.add_log_window_handler(self.__log_window_handler)
        self.main_window.show()

    def __log_window_handler(self) -> None:
        """
        Handler for the output log
        :return None:
        """
        self.logger.debug("running")
        self.log_output.show()


