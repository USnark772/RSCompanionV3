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
Date: 2019 - 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from logging import getLogger, StreamHandler, DEBUG, WARNING
from PySide2.QtWidgets import QMenuBar, QMenu, QAction
from PySide2.QtCore import QRect
from RSCompanionAsync.Resources.Strings.menu_bar_strings import strings, StringsEnum, LangEnum


class AppMenuBar(QMenuBar):
    """ This code is for the menu bar at the top of the main window. File, help, etc. """
    def __init__(self, parent=None, lang: LangEnum = LangEnum.ENG, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 840, 22))

        self._file_menu = QMenu(self)

        self._open_last_save_dir_action = QAction(self)

        self._exit_action = QAction(self)

        # self._cam_list_menu = QMenu(self)
        # self._file_menu.addMenu(self._cam_list_menu)

        # self._use_cams_action = QAction(self)
        # self._use_cams_action.setCheckable(True)
        # self._cam_list_menu.addAction(self._use_cams_action)

        # sep = self._cam_list_menu.addSeparator()

        self._settings_menu = QMenu(self)

        """ Display layout options """
        self._subwindow_layout_actions = []
        self._subwindow_layout_menu = QMenu(self)

        self._horiz_action = QAction(self)
        self._subwindow_layout_actions.append(self._horiz_action)
        self._horiz_action.triggered.connect(self._horiz_clicked)

        self._vert_action = QAction(self)
        self._subwindow_layout_actions.append(self._vert_action)
        self._vert_action.triggered.connect(self._vert_clicked)

        self._tiled_action = QAction(self)
        self._subwindow_layout_actions.append(self._tiled_action)
        self._tiled_action.triggered.connect(self._tiled_clicked)

        self._cascade_action = QAction(self)
        self._subwindow_layout_actions.append(self._cascade_action)
        self._cascade_action.triggered.connect(self._cascade_clicked)

        """ Language options """
        self._lang_actions = []
        self._language_menu = QMenu(self)

        # English
        self._english_action = QAction(self)
        self._lang_actions.append(self._english_action)
        self._english_action.setCheckable(True)
        self._english_action.triggered.connect(self._eng_clicked)

        # Dutch
        self._dutch_action = QAction(self)
        self._lang_actions.append(self._dutch_action)
        self._dutch_action.setCheckable(True)
        self._dutch_action.triggered.connect(self._dut_clicked)

        # French
        self._french_action = QAction(self)
        self._lang_actions.append(self._french_action)
        self._french_action.setCheckable(True)
        self._french_action.triggered.connect(self._fre_clicked)

        # German
        self._german_action = QAction(self)
        self._lang_actions.append(self._german_action)
        self._german_action.setCheckable(True)
        self._german_action.triggered.connect(self._ger_clicked)

        # Spanish
        self._spanish_action = QAction(self)
        self._lang_actions.append(self._spanish_action)
        self._spanish_action.setCheckable(True)
        self._spanish_action.triggered.connect(self._spa_clicked)

        # TODO: issue with Chinese, Japanese, and Russian characters.
        #       seems to be an issue with matplotlib
        # Chinese
        # self._chinese_action = QAction(self)
        # self._lang_actions.append(self._chinese_action)
        # self._chinese_action.setCheckable(True)
        # self._chinese_action.triggered.connect(self._chi_clicked)

        # Japanese
        # self._japanese_action = QAction(self)
        # self._lang_actions.append(self._japanese_action)
        # self._japanese_action.setCheckable(True)
        # self._japanese_action.triggered.connect(self._jpn_clicked)

        # Russian
        # self._russian_action = QAction(self)
        # self._lang_actions.append(self._russian_action)
        # self._russian_action.setCheckable(True)
        # self._russian_action.triggered.connect(self._rus_clicked)

        """ Debug options """
        self._debug_actions = []
        self._debug_menu = QMenu(self)

        self._debug_action = QAction(self)
        self._debug_action.setCheckable(True)
        self._debug_action.triggered.connect(self._debug_clicked)
        self._debug_actions.append(self._debug_action)

        self._warning_action = QAction(self)
        self._warning_action.setCheckable(True)
        self._warning_action.triggered.connect(self._warning_clicked)
        self._debug_actions.append(self._warning_action)

        """ Help options """
        self._help_menu = QMenu(self)

        self._about_app_action = QAction(self)

        self._about_company_action = QAction(self)

        self._update_action = QAction(self)

        self._log_window_action = QAction(self)

        self._cam_actions = {}

        """ Menus order """
        # Menu bar options
        self.addAction(self._file_menu.menuAction())
        self.addAction(self._settings_menu.menuAction())
        self.addAction(self._help_menu.menuAction())

        # Menu bar -> File menu options
        self._file_menu.addAction(self._open_last_save_dir_action)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self._exit_action)

        # Menu bar -> Settings menu options
        self._settings_menu.addMenu(self._subwindow_layout_menu)
        self._settings_menu.addMenu(self._language_menu)
        self._settings_menu.addMenu(self._debug_menu)

        # Menu bar -> Settings -> Window Layout options
        self._subwindow_layout_menu.addAction(self._horiz_action)
        self._subwindow_layout_menu.addAction(self._vert_action)
        self._subwindow_layout_menu.addAction(self._tiled_action)
        self._subwindow_layout_menu.addAction(self._cascade_action)

        # Menu bar -> Settings -> Language menu options
        self._language_menu.addAction(self._english_action)
        self._language_menu.addAction(self._dutch_action)
        self._language_menu.addAction(self._french_action)
        self._language_menu.addAction(self._german_action)
        self._language_menu.addAction(self._spanish_action)
        # self._language_menu.addAction(self._russian_action)
        # self._language_menu.addAction(self._chinese_action)
        # self._language_menu.addAction(self._japanese_action)

        # Menu bar -> Settings -> Debug menu options
        self._debug_menu.addAction(self._debug_action)
        self._debug_menu.addAction(self._warning_action)

        # Menu bar -> Help menu options
        self._help_menu.addAction(self._about_app_action)
        self._help_menu.addAction(self._about_company_action)
        self._help_menu.addAction(self._update_action)
        self._help_menu.addAction(self._log_window_action)

        self._debug_callback = None
        self._lang_callback = None
        self._layout_callback = None
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
        if lang == LangEnum.ENG:
            self._reset_lang_actions(self._english_action)
        elif lang == LangEnum.DUT:
            self._reset_lang_actions(self._dutch_action)
        elif lang == LangEnum.FRE:
            self._reset_lang_actions(self._french_action)
        elif lang == LangEnum.GER:
            self._reset_lang_actions(self._german_action)
        elif lang == LangEnum.SPA:
            self._reset_lang_actions(self._spanish_action)
        # elif lang == LangEnum.RUS:
        #     self._reset_lang_actions(self._russian_action)
        # elif lang == LangEnum.CHI:
        #     self._reset_lang_actions(self._chinese_action)
        # elif lang == LangEnum.JPN:
        #     self._reset_lang_actions(self._japanese_action)

    def add_window_layout_handler(self, func: classmethod) -> None:
        """
        Add handler for window layout.
        :param func: The handler function.
        :return None:
        """
        self._layout_callback = func

    def add_lang_select_handler(self, func: classmethod) -> None:
        """
        Add handler for these selectable. Handler must take a LangEnum
        :param func: The handler.
        :return None:
        """
        self._lang_callback = func

    def set_debug_action(self, level) -> None:
        """
        Set which debug action is checked.
        :param level: The debug level.
        :return None:
        """
        if level == DEBUG:
            self._reset_debug_actions(self._debug_action)
        elif level == WARNING:
            self._reset_debug_actions(self._warning_action)

    def add_debug_select_handler(self, func: classmethod) -> None:
        """
        Add handler for these selectables. Handler must take a string.
        :param func: The handler.
        :return None:
        """
        self._debug_callback = func

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

    def add_exit_handler(self, func: classmethod) -> None:
        """
        Add handler to this selectable.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._exit_action.triggered.connect(func)
        self._logger.debug("done")

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

    def _horiz_clicked(self) -> None:
        """
        Private handler for self._horiz_action
        :return None:
        """
        self._logger.debug("running")
        self._layout_callback("horizontal")
        self._logger.debug("done")

    def _vert_clicked(self) -> None:
        """
        Private handler for self._vert_action
        :return None:
        """
        self._logger.debug("running")
        self._layout_callback("vertical")
        self._logger.debug("done")

    def _tiled_clicked(self) -> None:
        """
        Private handler for self._tiled_action
        :return None:
        """
        self._logger.debug("running")
        self._layout_callback("tiled")
        self._logger.debug("done")

    def _cascade_clicked(self) -> None:
        """
        Private handler for self._cascade_action
        :return None:
        """
        self._logger.debug("running")
        self._layout_callback("cascade")
        self._logger.debug("done")

    def _eng_clicked(self) -> None:
        """
        Private handler for self._english_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.ENG)

    def _dut_clicked(self) -> None:
        """
        Private handler for self._english_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.DUT)

    def _fre_clicked(self) -> None:
        """
        Private handler for self._french_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.FRE)

    def _ger_clicked(self) -> None:
        """
        Private handler for self._german_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.GER)

    def _spa_clicked(self) -> None:
        """
        Private handler for self._spanish_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.SPA)

    def _rus_clicked(self) -> None:
        """
        Private handler for self._russian_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.RUS)

    def _chi_clicked(self) -> None:
        """
        Private handler for self._chinese_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.CHI)

    def _jpn_clicked(self) -> None:
        """
        Private handler for self._japanese_action
        :return None:
        """
        if self._lang_callback:
            self._lang_callback(LangEnum.JPN)

    def _debug_clicked(self) -> None:
        """
        Private handler for self._french_action
        :return None:
        """
        if self._debug_callback:
            self._debug_callback(DEBUG)
        self._reset_debug_actions(self._debug_action)

    def _warning_clicked(self) -> None:
        """
        Private handler for self._french_action
        :return None:
        """
        if self._debug_callback:
            self._debug_callback(WARNING)
        self._reset_debug_actions(self._warning_action)

    def _reset_debug_actions(self, keep_checked: QAction) -> None:
        """
        Unset all except for keep_checked QAction.
        :param keep_checked: The QAction to keep checked.
        :return None:
        """
        for action in self._debug_actions:
            action.setChecked(False)
        keep_checked.setChecked(True)

    def _reset_lang_actions(self, keep_checked: QAction) -> None:
        """
        Unset all except for keep_checked QAction.
        :param keep_checked: The QAction to keep checked.
        :return None:
        """
        for action in self._lang_actions:
            action.setChecked(False)
        keep_checked.setChecked(True)

    def _set_texts(self) -> None:
        """
        Set the texts of this view object.
        :return None:
        """
        self._logger.debug("running")
        self._file_menu.setTitle(self._strings[StringsEnum.FILE])
        self._open_last_save_dir_action.setText(self._strings[StringsEnum.LAST_DIR])
        self._exit_action.setText(self._strings[StringsEnum.EXIT])
        self._settings_menu.setTitle(self._strings[StringsEnum.SETTINGS])
        self._subwindow_layout_menu.setTitle(self._strings[StringsEnum.LAYOUT])
        self._horiz_action.setText(self._strings[StringsEnum.HORIZONTAL])
        self._vert_action.setText(self._strings[StringsEnum.VERTICAL])
        self._tiled_action.setText(self._strings[StringsEnum.TILED])
        self._cascade_action.setText(self._strings[StringsEnum.CASCADE])
        self._debug_menu.setTitle(self._strings[StringsEnum.DEBUG_MENU])
        self._debug_action.setText(self._strings[StringsEnum.DEBUG])
        self._warning_action.setText(self._strings[StringsEnum.WARNING])
        # self._cam_list_menu.setTitle(self._strings[StringsEnum.ATTACHED_CAMS])
        # self._use_cams_action.setText(self._strings[StringsEnum.USE_CAMS])
        self._language_menu.setTitle(self._strings[StringsEnum.LANG])
        self._english_action.setText(self._strings[StringsEnum.ENG])
        self._dutch_action.setText(self._strings[StringsEnum.DUT])
        self._french_action.setText(self._strings[StringsEnum.FRE])
        self._german_action.setText(self._strings[StringsEnum.GER])
        self._spanish_action.setText(self._strings[StringsEnum.SPA])
        # self._russian_action.setText(self._strings[StringsEnum.RUS])
        # self._chinese_action.setText(self._strings[StringsEnum.CHI])
        # self._japanese_action.setText(self._strings[StringsEnum.JPN])
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
