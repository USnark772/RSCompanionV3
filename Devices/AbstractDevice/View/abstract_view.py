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


from abc import ABCMeta, ABC, abstractmethod
from Model.app_helpers import EasyFrame
from PySide2.QtWidgets import QMdiSubWindow, QMdiArea, QHBoxLayout, QGridLayout, QLayout
from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent


class AbstractMeta(ABCMeta, type(QMdiSubWindow)):
    pass


class SubWindow(QMdiSubWindow):
    def __init__(self):
        QMdiSubWindow.__init__(self)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)  # TODO: Figure out how to do this at construction
        self.setLayout(QHBoxLayout())
        self.main_frame = EasyFrame()
        self.main_frame.setMouseTracking(True)
        super().layout().addWidget(self.main_frame)
        self.main_frame.setLayout(QGridLayout())

    def layout(self) -> QLayout:
        return self.main_frame.layout()


class AbstractView(ABC, SubWindow, metaclass=AbstractMeta):
    def __init__(self, name: str = ""):
        ABC.__init__(self)
        SubWindow.__init__(self)
        self._name = name
        self.setWindowTitle(self._name)

    def get_name(self) -> str:
        """
        :return: This object's device name.
        """
        return self._name

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Do not allow user to close window directly.
        :param event: The close event.
        :return: None
        """
        event.ignore()
