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


class OutputWindow(QWidget):
    """ This is to display small messages to the user. """
    def __init__(self):
        super().__init__()
        self.resize(400, 200)
        self.move(100, 100)
        self.setWindowTitle('Program Output')
        self.setLayout(QVBoxLayout())
        self.textBox = QTextEdit()
        self.layout().addWidget(self.textBox)
        self.text = ""
        self.textBox.setReadOnly(True)

    def write(self, message):
        self.textBox.moveCursor(QTextCursor.End)
        self.textBox.insertPlainText(message)
        self.textBox.moveCursor(QTextCursor.End)
