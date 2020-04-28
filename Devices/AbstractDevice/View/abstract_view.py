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
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from abc import ABCMeta, ABC, abstractmethod
from PySide2.QtWidgets import QMdiSubWindow


class AbstractMeta(ABCMeta, type(QMdiSubWindow)):
    pass


class SubWindow(QMdiSubWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


# TODO: Figure out how to use multiple inheritance with ABC and QMdiSubWindow.
#  Having issue with QMdiSubWindow or any QWidget apparently. 0xC0000409
class AbstractView(ABC, SubWindow, metaclass=AbstractMeta):
    def __init__(self, parent, name):
        ABC.__init__(parent)
        SubWindow.__init__(parent)
        self._name = name

    def get_name(self):
        return self._name


if __name__ == '__main__':
    test = AbstractView(None, "HI")
    print(test.get_name())
