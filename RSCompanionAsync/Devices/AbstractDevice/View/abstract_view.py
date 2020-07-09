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
from RSCompanionAsync.Model.app_helpers import EasyFrame
from RSCompanionAsync.Model.app_defs import image_file_path, settings_info
from PySide2.QtWidgets import QMdiSubWindow, QHBoxLayout, QGridLayout, QLayout
from PySide2.QtCore import Qt, QSettings
from PySide2.QtGui import QCloseEvent, QIcon


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

            self._icon = QIcon(image_file_path + "rs_icon.png")
            self.setWindowIcon(self._icon)

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
        self._minimized = False

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
        if self._minimized:
            self.setWindowState(Qt.WindowNoState)
            self._minimized = False
        elif not self._minimized:
            self.setWindowState(Qt.WindowMinimized)
            self._minimized = True

    def save_window_state(self) -> None:
        """
        Save this window's current state for next time app is used.
        :return None:
        """
        self._logger.debug("running")
        settings = QSettings(settings_info[0], settings_info[1])
        settings.beginGroup(self._settings_group_ident)
        cur_geo = self.frameGeometry()
        settings.setValue(self._win_geo_ident, cur_geo)
        settings.endGroup()
        self._logger.debug("done")

    def restore_window(self) -> None:
        """
        Restore window state and geometry from previous session if exists.
        :return None:
        """
        self._logger.debug("running")
        settings = QSettings(settings_info[0], settings_info[1])
        settings.beginGroup(self._settings_group_ident)
        if not settings.contains(self._win_geo_ident):
            settings.setValue(self._win_geo_ident, self.frameGeometry())
        self.setGeometry(settings.value(self._win_geo_ident))
        settings.endGroup()
        self._logger.debug("done")
