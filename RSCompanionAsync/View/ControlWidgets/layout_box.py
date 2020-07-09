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
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QRadioButton
from PySide2.QtCore import QSize
from RSCompanionAsync.Resources.Strings.menu_bar_strings import strings, StringsEnum, LangEnum


class LayoutBox(QGroupBox):
    def __init__(self, parent=None, size: QSize = QSize(10, 10), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        self.logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self.logger.addHandler(h)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setMaximumSize(size)

        self._horizontal_button = QRadioButton(self)
        self._horizontal_button.clicked.connect(self._horizontal_toggled)

        self._vertical_button = QRadioButton(self)
        self._vertical_button.clicked.connect(self._vertical_toggled)

        self._tiled_button = QRadioButton(self)
        self._tiled_button.clicked.connect(self._tiled_toggled)

        self._cascade_button = QRadioButton(self)
        self._cascade_button.clicked.connect(self._cascade_toggled)

        self.layout().addWidget(self._horizontal_button)
        self.layout().addWidget(self._vertical_button)
        self.layout().addWidget(self._tiled_button)
        self.layout().addWidget(self._cascade_button)

        self._layout_callback = None
        self._strings = dict()
        self.set_lang(lang)

        self.logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The enum for the language.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    def add_window_layout_handler(self, func: classmethod) -> None:
        """
        Add handler for window layout.
        :param func: The handler function
        :return None:
        """
        self._layout_callback = func

    def _horizontal_toggled(self):
        self.logger.debug("running")
        if self._horizontal_button.isChecked():
            self._layout_callback("horizontal")
        self.logger.debug("done")

    def _vertical_toggled(self):
        self.logger.debug("running")
        if self._vertical_button.isChecked():
            self._layout_callback("vertical")
        self.logger.debug("done")

    def _tiled_toggled(self):
        self.logger.debug("running")
        if self._tiled_button.isChecked():
            self._layout_callback("tiled")
        self.logger.debug("done")

    def _cascade_toggled(self):
        self.logger.debug("running")
        if self._cascade_button.isChecked():
            self._layout_callback("cascade")
        self.logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set the texts of this view item
        :return None:
        """
        self.logger.debug("running")
        self.setTitle(self._strings[StringsEnum.LAYOUT])
        self._horizontal_button.setText(self._strings[StringsEnum.HORIZONTAL])
        self._vertical_button.setText(self._strings[StringsEnum.VERTICAL])
        self._tiled_button.setText(self._strings[StringsEnum.TILED])
        self._cascade_button.setText(self._strings[StringsEnum.CASCADE])
        self.logger.debug("done")
