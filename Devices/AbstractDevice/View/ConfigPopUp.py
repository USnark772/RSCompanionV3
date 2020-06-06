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
from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QCloseEvent, QResizeEvent


class ConfigPopUp(QDialog):
    """
    Configuration pop up object that inherits from QDialog
    """
    def __init__(self, parent=None):
        super(ConfigPopUp, self).__init__(parent)

    """ Used for testing purposes """
    # def resizeEvent(self, event: QResizeEvent):
    #     print("popup width:", self.width())
    #     print("popup height:", self.height())
    #     return super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Override closeEvent to set the Configuration popup to not visible instead of deleting it.
        :param event: QCloseEvent - the close event to capture and override
        :return None:
        """
        event.ignore()
        self.setVisible(False)
