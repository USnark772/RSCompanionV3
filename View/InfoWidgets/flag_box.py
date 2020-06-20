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


from logging import getLogger, StreamHandler
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, QSize
from Resources.Strings.flag_box_strings import strings, StringsEnum, LangEnum


class FlagBox(QGroupBox):
    """ This code is for showing and storing the keyflag which in this case is the last letter key the user pressed. """
    def __init__(self, parent=None, size: QSize = QSize(10, 10), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setMaximumSize(size)
        self._flag = QLabel(self)
        font = QFont()
        font.setPointSize(16)
        self._flag.setFont(font)
        self.layout().addWidget(self._flag, 0, Qt.AlignHCenter)

        self.setMinimumWidth(105)

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
        self._set_tooltips()

    def set_flag(self, text):
        self._logger.debug("running")
        self._flag.setText(text)
        self._logger.debug("done")

    def get_flag(self):
        return self._flag.text()

    def _set_texts(self):
        self._logger.debug("running")
        self.setTitle(self._strings[StringsEnum.TITLE])
        self._flag.setText("")
        self._logger.debug("done")

    def _set_tooltips(self):
        self._logger.debug("running")
        self._flag.setToolTip(self._strings[StringsEnum.FLAG_TT])
        self._logger.debug("done")
