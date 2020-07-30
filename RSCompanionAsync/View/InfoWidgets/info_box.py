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
from RSCompanionAsync.Resources.Strings.info_box_strings import strings, StringsEnum, LangEnum


class InfoBox(QGroupBox):
    """ This code is for displaying information about the current experiment. """
    def __init__(self, parent=None, size: QSize = QSize(10, 10), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setFixedSize(size)
        self.setLayout(QGridLayout())

        self._start_time_label = QLabel()
        self._start_time_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._start_time_label, 1, 0, 1, 1)

        self._start_time_val = QLabel()
        self._start_time_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._start_time_val, 1, 1, 1, 1)

        self._block_num_label = QLabel()
        self._block_num_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._block_num_label, 3, 0, 1, 1)

        self._block_num_val = QLabel()
        self._block_num_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._block_num_val, 3, 1, 1, 1)

        self._current_time_label = QLabel()
        self._current_time_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._current_time_label, 0, 0, 1, 1)

        self._current_time_val = QLabel()
        self._current_time_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._current_time_val, 0, 1, 1, 1)

        self._block_start_time_label = QLabel()
        self._block_start_time_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self._block_start_time_label, 2, 0, 1, 1)

        self._block_start_time_val = QLabel()
        self._block_start_time_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self._block_start_time_val, 2, 1, 1, 1)

        self.setMinimumWidth(260)

        self._default_time = '00:00:00'
        self._strings = dict()
        self.set_lang(lang)
        self._set_default_values()
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language of this view item.
        :param lang: The language enum to use.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    def set_current_time(self, time: str) -> None:
        """
        Set current time display.
        :param time: The new value to display.
        :return None:
        """
        self._logger.debug("running")
        self._current_time_val.setText(time)
        self._logger.debug("done")

    def set_exp_start_time(self, time: str) -> None:
        """
        Set exp start time display.
        :param time: The new value to display.
        :return None:
        """
        self._logger.debug("running")
        self._start_time_val.setText(time)
        self._logger.debug("done")

    def reset_exp_start_time(self) -> None:
        """
        Set exp start time to '00:00:00'
        :return None:
        """
        self._logger.debug("running")
        self._start_time_val.setText(self._default_time)
        self._logger.debug("done")

    def set_block_num(self, num: str) -> None:
        """
        Set block number display.
        :param num: The new value to display.
        :return None:
        """
        self._logger.debug("running")
        self._block_num_val.setText(num)
        self._logger.debug("done")

    def get_block_num(self) -> str:
        """
        :return str: The value of block num display.
        """
        return self._block_num_val.text()

    def set_block_start_time(self, time: str) -> None:
        """
        Set block start time display.
        :param time: The new value to display.
        :return None:
        """
        self._logger.debug("running")
        self._block_start_time_val.setText(time)
        self._logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set text of all display labels.
        :return:
        """
        self._logger.debug("running")
        self.setTitle(self._strings[StringsEnum.TITLE])
        self._current_time_label.setText(self._strings[StringsEnum.CUR_TIME])
        self._block_start_time_label.setText(self._strings[StringsEnum.BLK_ST_TIME])
        self._start_time_label.setText(self._strings[StringsEnum.START_TIME])
        self._block_num_label.setText(self._strings[StringsEnum.BLOCK_NUM])
        self._logger.debug("done")

    def _set_default_values(self) -> None:
        """
        Set text of all display values to default.
        :return:
        """
        self._logger.debug("running")
        self._block_num_val.setText("0")
        self.set_current_time(self._default_time)
        self.set_block_start_time(self._default_time)
        self.reset_exp_start_time()
        self._logger.debug("done")
