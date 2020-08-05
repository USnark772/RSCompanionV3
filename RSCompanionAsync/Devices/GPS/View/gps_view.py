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

Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from logging import getLogger, StreamHandler
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide2.QtCore import Qt, QSize
from RSCompanionAsync.Model.app_helpers import ClickAnimationButton, EasyFrame
from RSCompanionAsync.Devices.GPS.Resources.gps_strings import strings, StringsEnum, LangEnum
from RSCompanionAsync.Devices.AbstractDevice.View.abstract_view import AbstractView
from RSCompanionAsync.Devices.AbstractDevice.View.config_pop_up import ConfigPopUp


class GPSView(AbstractView):
    def __init__(self, name: str = "GPS_NONE", log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(name)

        """ Min size for the GPS window """
        self._subwindow_size = (222, 518)

        """ Sizes for configuration menu """
        self._popup_min = (168, 313)
        self._popup_max = (300, 313)

        """ Device settings display """
        self._dev_sets_frame = EasyFrame()
        self._dev_sets_layout = QVBoxLayout(self._dev_sets_frame)
        self._config_horizontal_layout = QHBoxLayout()

        self.config_button = ClickAnimationButton()
        self.config_button.clicked.connect()

        self.layout().addWidget(self.config_button, 0, 0, Qt.AlignTop | Qt.AlignRight)
        self.config_button.setFixedSize(30, 25)

        self._config_win = ConfigPopUp()
        self._config_win.setMinimumSize(self._popup_min[0], self._popup_min[1])
        self._config_win.setMaximumSize(self._popup_max[0], self._popup_max[1])
        self._config_win.setLayout(self._dev_sets_layout)

        """ Add all of the widgets to the layout. """

        self.layout().setMargin(0)

        self._strings = dict()
        self._lang_enum = LangEnum.ENG
        self.setMinimumSize(self._subwindow_size[0], self._subwindow_size[1])
        self.resize(self._subwindow_size)
        self._logger.debug("Initialized")

    def _config_button_handler(self) -> None:
        """
        handles the config button
        :return None:
        """
        self._logger.debug("running")
        self._config_win.exec_()
        self._logger.debug("done")

    @property
    def language(self) -> LangEnum:
        """
        Get the current language setting
        :return LangEnum: The current language enumerator being used
        """
        return self._lang_enum

    @language.setter
    def language(self, lang: LangEnum) -> None:
        """
        Set the language for this view object and reload the text and tooltips.
        :param lang: the language to use.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._set_texts()
        self._set_tooltips()
        self._logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set text values for this view object
        :return None:
        """
        self._logger.debug("running")
        print("implement gps _set_texts()")
        self._logger.debug("done")

    def _set_tooltips(self) -> None:
        """
        Set the text values of the tooltips for this view object
        :return None:
        """
        self._logger.debug("running")
        print("implement gps _set_tooltips()")
        self._logger.debug("done")
