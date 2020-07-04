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

from PySide2.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide2.QtGui import QTextCursor
from RSCompanionAsync.Resources.Strings.output_window_strings import strings, StringsEnum, LangEnum


class OutputWindow(QWidget):
    """ This is to display small messages to the user. """
    def __init__(self, lang: LangEnum = LangEnum.ENG):
        super().__init__()
        self.resize(400, 200)
        self.move(100, 100)
        self.setLayout(QVBoxLayout())
        self._textBox = QTextEdit()
        self.layout().addWidget(self._textBox)
        self._strings = dict()
        self.set_lang(lang)
        self._textBox.setReadOnly(True)

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The enum for the language.
        :return None:
        """
        self._strings = strings[lang]
        self.setWindowTitle(self._strings[StringsEnum.TITLE])

    def write(self, message) -> None:
        """
        Add text to output window.
        :param message: The text to add.
        :return: None.
        """
        self._textBox.moveCursor(QTextCursor.End)
        self._textBox.insertPlainText(message)
        self._textBox.moveCursor(QTextCursor.End)
