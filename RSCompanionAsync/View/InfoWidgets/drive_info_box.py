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
from PySide2.QtWidgets import QLabel, QGridLayout, QGroupBox
from PySide2.QtCore import QSize, Qt
from RSCompanionAsync.Resources.Strings.drive_info_strings import strings, StringsEnum, LangEnum


class DriveInfoBox(QGroupBox):
    """ This code is for displaying information about storage usage. """
    def __init__(self, parent=None, size: QSize = QSize(10, 10), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        """
        Initialize this view module.
        :param parent: parent of this view module.
        :param size: size this view module should occupy
        :param log_handlers:
        """
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setFixedSize(size)
        self.setLayout(QGridLayout())

        self._drive_name_label = QLabel()
        self._drive_name_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._drive_name_label, 0, 0, 1, 1)

        self._drive_name_val = QLabel()
        self._drive_name_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._drive_name_val, 0, 1, 1, 1)

        self._drive_percent_label = QLabel()
        self._drive_percent_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._drive_percent_label, 1, 0, 1, 1)

        self._drive_percent_val = QLabel()
        self._drive_percent_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._drive_percent_val, 1, 1, 1, 1)

        self._drive_gb_label = QLabel()
        self._drive_gb_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._drive_gb_label, 2, 0, 1, 1)

        self._drive_gb_val = QLabel()
        self._drive_gb_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._drive_gb_val, 2, 1, 1, 1)

        self._drive_mb_label = QLabel()
        self._drive_mb_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._drive_mb_label, 3, 0, 1, 1)

        self._drive_mb_val = QLabel()
        self._drive_mb_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._drive_mb_val, 3, 1, 1, 1)

        self._strings = dict()
        self.set_lang(lang)
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The enum for the language.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    def set_name_val(self, value: str) -> None:
        """
        Set the value for drive name
        :param value: the value to show
        :return: None
        """
        self._drive_name_val.setText(value)

    def set_perc_val(self, value: str) -> None:
        """
        Set the value for percentage
        :param value: the value to show
        :return: None
        """
        self._drive_percent_val.setText(value + '%')

    def set_gb_val(self, value: str) -> None:
        """
        Set the value for gb
        :param value: the value to show
        :return: None
        """
        self._drive_gb_val.setText(value)

    def set_mb_val(self, value: str) -> None:
        """
        Set the value for mb
        :param value: the value to show
        :return: None
        """
        self._drive_mb_val.setText(value)

    def _set_texts(self) -> None:
        """
        Set the text for each element in this view module
        :return: None
        """
        self._logger.debug("running")
        self.setTitle(self._strings[StringsEnum.TITLE])
        self._drive_name_label.setText(self._strings[StringsEnum.STORAGE_ID])
        self._drive_percent_label.setText(self._strings[StringsEnum.PERC_USED])
        self._drive_gb_label.setText(self._strings[StringsEnum.GB_FREE])
        self._drive_mb_label.setText(self._strings[StringsEnum.MB_FREE])
        self._drive_name_val.setText('-')
        self._drive_percent_val.setText('0%')
        self._drive_gb_val.setText('0')
        self._drive_mb_val.setText('0')
        self._logger.debug("Done")
