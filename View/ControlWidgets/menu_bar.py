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
Date: 2019 - 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from logging import getLogger, StreamHandler
from PySide2.QtWidgets import QMenuBar, QMenu, QAction
from PySide2.QtCore import QRect, Signal
from Resources.Strings.menu_bar_strings import strings, StringsEnum, LangEnum


class AppMenuBar(QMenuBar):
    """ This code is for the menu bar at the top of the main window. File, help, etc. """
    lang_clicked_sig = Signal(int)

    def __init__(self, parent, ch: StreamHandler, lang: LangEnum):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 840, 22))

        self._file_menu = QMenu(self)
        self.addAction((self._file_menu.menuAction()))

        self._open_last_save_dir_action = QAction(self)
        self._file_menu.addAction(self._open_last_save_dir_action)

        self._language_menu = QMenu(self)
        self._file_menu.addMenu(self._language_menu)

        self._english_action = QAction(self, 0)
        self._english_action.setCheckable(True)
        self._english_action.toggled.connect(self._eng_clicked)
        self._language_menu.addAction(self._english_action)

        self._french_action = QAction(self)
        self._french_action.setCheckable(True)
        self._french_action.toggled.connect(self._fre_clicked)
        self._language_menu.addAction(self._french_action)

        # self._cam_list_menu = QMenu(self)
        # self._file_menu.addMenu(self._cam_list_menu)

        # self._use_cams_action = QAction(self)
        # self._use_cams_action.setCheckable(True)
        # self._cam_list_menu.addAction(self._use_cams_action)

        # sep = self._cam_list_menu.addSeparator()

        self._help_menu = QMenu(self)
        self.addAction(self._help_menu.menuAction())

        self._about_app_action = QAction(self)
        self._help_menu.addAction(self._about_app_action)

        self._about_company_action = QAction(self)
        self._help_menu.addAction(self._about_company_action)

        self._update_action = QAction(self)
        self._help_menu.addAction(self._update_action)

        self._log_window_action = QAction(self)
        self._help_menu.addAction(self._log_window_action)

        self._cam_actions = {}

        self._lang_callback = None
        self._strings = dict()
        self.set_lang(lang)
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language of this view item.
        :param lang: The language enum to use.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    # TODO: Implement this
    def get_lang(self) -> LangEnum:
        """
        Get user's choice of language.
        :return LangEnum: The user's choice.
        """

        return LangEnum.ENG

    def add_lang_select_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._lang_callback = func

    def set_cam_action_enabled(self, is_active: bool) -> None:
        """
        Set whether or not the camera actions can be used.
        :param is_active: can be used.
        :return None:
        """

        self._use_cams_action.setEnabled(is_active)
        for action in self._cam_actions.values():
            action.setEnabled(is_active)

    def set_cam_bool_checked(self, is_active: bool) -> None:
        """
        Set whether or not this action is checked.
        :param is_active: whether or not this action should be checked.
        :return None:
        """
        self._use_cams_action.setChecked(is_active)
        self.empty_cam_actions()

    def add_cam_bool_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._use_cams_action.toggled.connect(func)
        self._logger.debug("done")

    def set_use_cams_action_active(self, is_active: bool) -> None:
        """
        Set whether or not this action is usable.
        :param is_active: whether or not to let this action be usable.
        :return None:
        """

        self._use_cams_action.setEnabled(is_active)

    def add_open_last_save_dir_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._open_last_save_dir_action.triggered.connect(func)
        self._logger.debug("done")

    def add_about_app_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._about_app_action.triggered.connect(func)
        self._logger.debug("done")

    def add_about_company_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._about_company_action.triggered.connect(func)
        self._logger.debug("done")

    def add_update_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._update_action.triggered.connect(func)
        self._logger.debug("done")

    def add_log_window_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._log_window_action.triggered.connect(func)
        self._logger.debug("done")

    def add_cam_action(self, name: str, handler: classmethod, is_active: bool = True) -> None:
        """
        Add a new action in the camera menu by name.
        :param name: The name of the camera being added.
        :param handler: The button handler.
        :param is_active: Whether or not this camera is considered active.
        :return None:
        """

        new_cam_action = QAction(self)
        new_cam_action.setText(name)
        new_cam_action.setCheckable(True)
        new_cam_action.setChecked(is_active)
        new_cam_action.toggled.connect(handler)
        self._cam_actions[name] = new_cam_action
        self._cam_list_menu.addAction(new_cam_action)

    def remove_cam_action(self, name: str) -> None:
        """
        Remove a cam action by name.
        :param name: The name of the camera being removed.
        :return None:
        """

        if name in self._cam_actions.keys():
            self._cam_list_menu.removeAction(self._cam_actions[name])
            del self._cam_actions[name]

    def _eng_clicked(self) -> None:
        """
        Private handler for self._english_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.ENG)

    def _fre_clicked(self) -> None:
        """
        Private handler for self._french_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.FRE)

    def _set_texts(self) -> None:
        """
        Set the texts of this view object.
        :return None:
        """
        self._logger.debug("running")
        self._file_menu.setTitle(self._strings[StringsEnum.FILE])
        self._open_last_save_dir_action.setText(self._strings[StringsEnum.LAST_DIR])
        # self._cam_list_menu.setTitle(self._strings[StringsEnum.ATTACHED_CAMS])
        # self._use_cams_action.setText(self._strings[StringsEnum.USE_CAMS])
        self._language_menu.setTitle(self._strings[StringsEnum.LANG])
        self._english_action.setText(self._strings[StringsEnum.ENG])
        self._french_action.setText(self._strings[StringsEnum.FRE])
        self._help_menu.setTitle(self._strings[StringsEnum.HELP])
        self._about_app_action.setText(self._strings[StringsEnum.ABOUT_APP])
        self._about_company_action.setText(self._strings[StringsEnum.ABOUT_COMPANY])
        self._update_action.setText(self._strings[StringsEnum.UPDATE_CHECK])
        self._log_window_action.setText(self._strings[StringsEnum.SHOW_LOG_WINDOW])
        self._logger.debug("done")

    def empty_cam_actions(self) -> None:
        """
        :return None:
        """
        for name in self._cam_actions.keys():
            self._cam_list_menu.removeAction(self._cam_actions[name])
        self._cam_actions = {}
