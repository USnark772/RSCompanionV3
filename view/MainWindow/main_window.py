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
Date: 2019
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

import logging
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox, QMdiArea
from PySide2.QtGui import QFont, QIcon, QCloseEvent
from View.MainWindow.help_window import HelpWindow
from View.MainWindow.central_widget import CentralWidget
from Model.app_defs import image_file_path
from Model.strings_english import app_name, closing_app_text, close_confirmation_text


class AppMainWindow(QMainWindow):
    """ The main window the app will be displayed in. """
    def __init__(self, min_size, ch):
        self.__logger = logging.getLogger(__name__)
        self.__logger.addHandler(ch)
        self.__logger.debug("Initializing")
        super().__init__()
        self.__icon = QIcon(image_file_path + "rs_icon.png")
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setMinimumSize(min_size)
        self.setWindowIcon(self.__icon)
        self.setCentralWidget(CentralWidget(self))

        self.__control_layout = QHBoxLayout()
        self.centralWidget().layout().addLayout(self.__control_layout)

        self.__checker = QMessageBox()
        self.__close_callback = None
        self.__help_window = None
        self.__set_texts()
        self.__setup_checker_buttons()
        self.__logger.debug("Initialized")

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Check if user really wants to close the app and only if so alert close and close.
        :param event: The close event
        :return: None
        """
        self.__logger.debug("running")
        if self.__checker.exec_() == QMessageBox.Yes:
            if self.__close_callback:
                self.__close_callback()
            event.accept()
        else:
            event.ignore()
        self.__logger.debug("done")

    def add_mdi_area(self, mdi_area: QMdiArea) -> None:
        """
        Add MDI area to the main window.
        :param mdi_area: The MDI area to add.
        :return: None.
        """
        self.add_mdi_area(mdi_area)
        pass

    def add_control_bar_widget(self, widget) -> None:
        """
        Add widget to the control layout.
        :param widget: The widget to add.
        :return: None
        """
        self.__control_layout.addWidget(widget)

    def add_close_handler(self, func: classmethod) -> None:
        """
        Add handler to handle close events.
        :param func: The handler.
        :return: None
        """
        self.__logger.debug("running")
        self.__close_callback = func
        self.__logger.debug("done")

    def add_menu_bar(self, widget) -> None:
        """
        Add menu bar to main window.
        :param widget: The menu bar.
        :return: None
        """
        self.__logger.debug("running")
        self.setMenuBar(widget)
        self.__logger.debug("done")

    def show_help_window(self, title, msg) -> None:
        """
        Show a pop up message window.
        :param title: The title of the window.
        :param msg: The message to be shown.
        :return: None
        """
        self.__logger.debug("running")
        self.__help_window = HelpWindow(title, msg)
        self.__help_window.setWindowIcon(self.__icon)
        self.__help_window.show()
        self.__logger.debug("done")

    def __set_texts(self) -> None:
        """
        Set the texts for the main window.
        :return: None
        """
        self.__logger.debug("running")
        self.setWindowTitle(app_name)
        self.__checker.setWindowTitle(closing_app_text)
        self.__checker.setText(close_confirmation_text)
        self.__logger.debug("done")

    def __setup_checker_buttons(self) -> None:
        """
        Setup window for close check.
        :return:
        """
        self.__checker.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        self.__checker.setDefaultButton(QMessageBox.Cancel)
        self.__checker.setEscapeButton(QMessageBox.Cancel)
