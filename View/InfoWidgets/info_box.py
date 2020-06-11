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
from PySide2.QtCore import Qt, QSize
from Resources.Strings.info_box_strings import strings, StringsEnum, LangEnum


class InfoBox(QGroupBox):
    """ This code is for displaying information about the current experiment. """
    def __init__(self, parent=None, size: QSize = QSize(10, 10), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        self.logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self.logger.addHandler(h)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setFixedSize(size)
        self.setLayout(QGridLayout())

        self.__start_time_label = QLabel()
        self.__start_time_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.__start_time_label, 0, 0, 1, 1)

        self.__start_time_val = QLabel()
        self.__start_time_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self.__start_time_val, 0, 1, 1, 1)

        self.__block_num_label = QLabel()
        self.__block_num_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.__block_num_label, 1, 0, 1, 1)

        self.__block_num_val = QLabel()
        self.__block_num_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self.__block_num_val, 1, 1, 1, 1)

        self._empty_block_1_label = QLabel()
        self._empty_block_1_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._empty_block_1_label, 2, 0, 1, 1)

        self._empty_block_1_val = QLabel()
        self._empty_block_1_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._empty_block_1_val, 2, 1, 1, 1)

        self._empty_block_2_label = QLabel()
        self._empty_block_2_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._empty_block_2_label, 3, 0, 1, 1)

        self._empty_block_2_val = QLabel()
        self._empty_block_2_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._empty_block_2_val, 3, 1, 1, 1)

        self._strings = dict()
        self.set_lang(lang)
        self.logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language of this view item.
        :param lang: The language enum to use.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    def set_start_time(self, time):
        self.logger.debug("running")
        self.__start_time_val.setText(time)
        self.logger.debug("done")

    def reset_start_time(self):
        self.logger.debug("running")
        self.__start_time_val.setText("00:00:00")
        self.logger.debug("done")

    def set_block_num(self, num):
        self.logger.debug("running")
        self.__block_num_val.setText(str(num))
        self.logger.debug("done")

    def get_block_num(self):
        return self.__block_num_val.text()

    def _set_texts(self):
        self.logger.debug("running")
        self.setTitle(self._strings[StringsEnum.TITLE])
        self.__start_time_label.setText(self._strings[StringsEnum.START_TIME])
        self.__block_num_label.setText(self._strings[StringsEnum.BLOCK_NO])
        self.__block_num_val.setText("0")
        self.reset_start_time()
        self.logger.debug("done")
