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


from abc import ABCMeta, ABC
from Model.app_helpers import EasyFrame
from Resources.Strings.app_strings import company_name, app_name
from PySide2.QtWidgets import QMdiSubWindow, QHBoxLayout, QGridLayout, QLayout
from PySide2.QtCore import Qt, QSettings
from PySide2.QtGui import QCloseEvent


class AbstractMeta(ABCMeta, type(QMdiSubWindow)):
    pass


class SubWindow(QMdiSubWindow):
    def __init__(self, empty: bool = False):
        QMdiSubWindow.__init__(self)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        if not empty:
            self.setLayout(QHBoxLayout())
            self.main_frame = EasyFrame()
            self.main_frame.setMouseTracking(True)
            super().layout().addWidget(self.main_frame)
            self.main_frame.setLayout(QGridLayout())
            self.layout = self.new_layout

    def new_layout(self) -> QLayout:
        """
        Returns a QGridLayout.
        :return QLayout: The grid layout.
        """
        return self.main_frame.layout()


class AbstractView(ABC, SubWindow, metaclass=AbstractMeta):
    def __init__(self, name: str = "DEFAULT", empty: bool = False):
        ABC.__init__(self)
        SubWindow.__init__(self, empty)
        self._name = name
        self.setWindowTitle(self._name)
        self._win_geo_ident = self._name + "_geo"
        self._win_state_ident = self._name + "_state"
        self._settings_group_ident = "subwindow_settings"

    def get_name(self) -> str:
        """
        :return: This object's device name.
        """
        return self._name

    # TODO find why graph disappears if we want to use this
    # def moveEvent(self, event: QMoveEvent) -> None:
    #     """
    #     Prevent subwindow from moving outside of parent window.
    #     :return None:
    #     """
    #     right = self.width()
    #     bottom = self.height()
    #     parent_right = self.parent().width()
    #     parent_bottom = self.parent().height()
    #
    #     if self.pos().x() < self.parent().pos().x():
    #         self.move(0, self.pos().y())
    #     if self.pos().x() + right > self.parent().pos().x() + parent_right:
    #         self.move(parent_right - right, self.pos().y())
    #     if self.pos().y() + bottom > self.parent().pos().y() + parent_bottom:
    #         self.move(self.pos().x(), parent_bottom - bottom)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Do not allow user to close window directly.
        :param event: The close event.
        :return: None
        """
        event.ignore()
        self.setWindowState(Qt.WindowMinimized)
        if self.windowState() == Qt.WindowMinimized:
            self.setWindowState(Qt.WindowNoState)
        elif self.windowState() == Qt.WindowNoState:
            self.setWindowState(Qt.WindowMinimized)

    def save_window_state(self) -> None:
        """
        Save this window's current state for next time app is used.
        :return None:
        """
        self._logger.debug("running")
        settings = QSettings(company_name, app_name)
        settings.beginGroup(self._settings_group_ident)
        cur_geo = self.saveGeometry()
        settings.setValue(self._win_geo_ident, cur_geo)
        settings.endGroup()
        self._logger.debug("done")

    def restore_window(self) -> None:
        """
        Restore window state and geometry from previous session if exists.
        :return None:
        """
        self._logger.debug("running")
        settings = QSettings(company_name, app_name)
        settings.beginGroup(self._settings_group_ident)
        if not settings.contains(self._win_geo_ident):
            settings.setValue(self._win_geo_ident, self.saveGeometry())
        self.restoreGeometry(settings.value(self._win_geo_ident))
        settings.endGroup()
        self._logger.debug("done")
