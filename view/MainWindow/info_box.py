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
from PySide2.QtWidgets import QLabel, QGridLayout, QGroupBox
from PySide2.QtCore import Qt


class InfoBox(QGroupBox):
    """ This code is for displaying information about the current experiment. """
    def __init__(self, parent, size, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setMaximumSize(size)
        self.setLayout(QGridLayout())

        self.__start_time_label = QLabel()
        self.__start_time_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.__start_time_label, 1, 0, 1, 1)

        self.__start_time_val = QLabel()
        self.__start_time_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self.__start_time_val, 1, 1, 1, 1)

        self.__block_num_label = QLabel()
        self.__block_num_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.__block_num_label, 2, 0, 1, 1)

        self.__block_num_val = QLabel()
        self.__block_num_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self.__block_num_val, 2, 1, 1, 1)

        self.__set_texts()
        self.logger.debug("Initialized")

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

    def __set_texts(self):
        self.logger.debug("running")
        self.setTitle("Information")
        self.__start_time_label.setText("Experiment start time:")
        self.__block_num_label.setText("Block number:")
        self.__block_num_val.setText("0")
        self.reset_start_time()
        self.logger.debug("done")
