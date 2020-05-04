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

from logging import getLogger, StreamHandler
from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox, QMdiArea
from PySide2.QtGui import QFont, QIcon, QCloseEvent
from PySide2.QtCore import QSize
from View.HelpWidgets.help_window import HelpWindow
from View.MainWindow.central_widget import CentralWidget
from Model.app_defs import image_file_path
from Resources.Strings.main_window_strings import strings, StringsEnum, LangEnum


class AppMainWindow(QMainWindow):
    """ The main window the app will be displayed in. """
    def __init__(self, min_size: QSize, log_handlers: [StreamHandler], lang: LangEnum):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__()
        self._icon = QIcon(image_file_path + "rs_icon.png")
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setMinimumSize(min_size)
        self.setWindowIcon(self._icon)
        self.setCentralWidget(CentralWidget(self))

        self._control_layout = QHBoxLayout()
        self.centralWidget().layout().addLayout(self._control_layout)

        self.unsaved = False
        self._checker = QMessageBox()
        self._close_callback = None
        self._help_window = None

        self._strings = dict()
        self.set_lang(lang)
        self._setup_checker_buttons()
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language of this view item.
        :param lang: The language enum to use.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Check if user really wants to close the app and only if so alert close and close.
        :param event: The close event.
        :return: None.
        """
        self._logger.debug("running")
        if self.unsaved:
            if not self._checker.exec_() == QMessageBox.Yes:
                event.ignore()
                return
        if self._close_callback:
            self._close_callback()
        event.accept()
        self._logger.debug("done")

    def add_mdi_area(self, mdi_area: QMdiArea) -> None:
        """
        Add MDI area to the main window.
        :param mdi_area: The MDI area to add.
        :return: None.
        """
        self._logger.debug("running")
        self.centralWidget().layout().addWidget(mdi_area)
        self._logger.debug("done")

    def add_control_bar_widget(self, widget, stretch: int=0) -> None:
        """
        Add widget to the control layout.
        :param widget: The widget to add.
        :param stretch: stretch factor
        :return: None.
        """
        self._logger.debug("running")
        self._control_layout.addWidget(widget, stretch)
        self._logger.debug("done")

    def add_spacer_item(self, stretch) -> None:
        """
        Add spacer item to maintain control bar format.
        :return: None.
        """
        self._logger.debug("running")
        self._control_layout.addStretch(stretch)
        self._logger.debug("done")

    def add_close_handler(self, func: classmethod) -> None:
        """
        Add handler to handle close events.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._close_callback = func
        self._logger.debug("done")

    def add_menu_bar(self, widget) -> None:
        """
        Add menu bar to main window.
        :param widget: The menu bar.
        :return: None.
        """
        self._logger.debug("running")
        self.setMenuBar(widget)
        self._logger.debug("done")

    def show_help_window(self, title, msg) -> None:
        """
        Show a pop up message window.
        :param title: The title of the window.
        :param msg: The message to be shown.
        :return: None
        """
        self._logger.debug("running")
        self._help_window = HelpWindow(title, msg)
        self._help_window.setWindowIcon(self._icon)
        self._help_window.show()
        self._logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set the texts for the main window.
        :return: None.
        """
        self._logger.debug("running")
        self.setWindowTitle(self._strings[StringsEnum.TITLE])
        self._checker.setWindowTitle(self._strings[StringsEnum.CLOSE_TITLE])
        self._checker.setText(self._strings[StringsEnum.CLOSE_APP_CONFIRM])
        self._logger.debug("done")

    def _setup_checker_buttons(self) -> None:
        """
        Setup window for close check.
        :return: None.
        """
        self._logger.debug("running")
        self._checker.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        self._checker.setDefaultButton(QMessageBox.Cancel)
        self._checker.setEscapeButton(QMessageBox.Cancel)
        self._logger.debug("done")
