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

# TODO reset cursor when leaving edge.

from abc import ABCMeta, ABC, abstractmethod
from PySide2.QtWidgets import QMdiSubWindow, QWidget, QMdiArea
from PySide2.QtCore import QEvent
from PySide2.QtGui import QCloseEvent, QMouseEvent, QCursor


class AbstractMeta(ABCMeta, type(QMdiSubWindow)):
    pass


class SubWindow(QMdiSubWindow):
    def __init__(self, parent: QMdiArea, contents: QWidget = None):
        QMdiSubWindow.__init__(self, parent)
        self.setWidget(contents)

    def mouseMoveEvent(self, mouseEvent: QMouseEvent):
        super(SubWindow, self).mouseMoveEvent(mouseEvent)
        mouse_pos = mouseEvent.pos()
        print(__name__, mouse_pos)
        print(__name__, self.size())
        if 0 < mouse_pos.x() < self.size().width() and 0 < mouse_pos.y() < self.size().height():
            QMdiSubWindow.unsetCursor(self)

    # def enterEvent(self, event: QEvent) -> None:
    #     print(__name__, "reached")
    #     QMdiSubWindow.unsetCursor(self)

class AbstractView(ABC, SubWindow, metaclass=AbstractMeta):
    def __init__(self, parent: QMdiArea, name: str = "", contents: QWidget = None):
        ABC.__init__(self)
        SubWindow.__init__(self, parent, contents)
        self._name = name
        self.setWindowTitle(self._name)

    def get_name(self):
        return self._name

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Do not allow user to close window directly.
        :param event: The close event.
        :return: None
        """
        event.ignore()
