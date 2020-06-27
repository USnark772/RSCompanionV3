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
from PySide2.QtWidgets import QHBoxLayout, QLabel, QGridLayout, QLineEdit, QVBoxLayout, QCheckBox, QComboBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QResizeEvent
from RSCompanionAsync.Model.app_helpers import ClickAnimationButton, EasyFrame
from RSCompanionAsync.Model.app_defs import tab_line_edit_compliant_style, tab_line_edit_error_style
from RSCompanionAsync.Devices.VOG.Resources.vog_strings import strings, StringsEnum, LangEnum
from RSCompanionAsync.Devices.AbstractDevice.View.abstract_view import AbstractView
from RSCompanionAsync.Devices.AbstractDevice.View.config_pop_up import ConfigPopUp


class VOGView(AbstractView):
    def __init__(self, name: str = "VOG_NONE", log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(name)

        """ Min size for the VOG window """
        self._subwindow_height = 222
        self._subwindow_width = 518

        """ min and max sizes for the configuration popup (width, height) """
        self._popup_min = (229, 409)
        self._popup_max = (300, 409)

        """ Set configuration value display area"""
        self._config_frame = EasyFrame()
        self._config_vertical_layout = QVBoxLayout(self._config_frame)
        self._config_label = QLabel(self._config_frame)
        self._config_label.setAlignment(Qt.AlignCenter)
        self._config_val_line_edit = QLineEdit(self._config_frame)
        self._config_val_line_edit.setAlignment(Qt.AlignCenter)

        self._config_vertical_layout.addWidget(self._config_label)
        self._config_vertical_layout.addWidget(self._config_val_line_edit)

        """ Set preset button selection area. """
        # self._presets_frame = EasyFrame()
        # self._presets_vert_layout = QVBoxLayout(self._presets_frame)
        self._nhtsa_button = ClickAnimationButton()
        self._eblindfold_button = ClickAnimationButton()
        self._direct_control_button = ClickAnimationButton()

        # self._presets_vert_layout.addWidget(self._nhtsa_button)
        # self._presets_vert_layout.addWidget(self._eblindfold_button)
        # self._presets_vert_layout.addWidget(self._direct_control_button)

        """ Set open duration, close duration, and debounce time settings display area. """
        self._input_box_frame = EasyFrame()
        self._input_box_grid_layout = QGridLayout(self._input_box_frame)
        self._input_box_grid_layout.setContentsMargins(0, 6, 0, 6)

        self._open_dur_label = QLabel(self._input_box_frame)
        self._open_dur_line_edit = QLineEdit(self._input_box_frame)
        self._open_dur_line_edit.setFixedWidth(80)
        self._open_inf_check_box = QCheckBox(self._input_box_frame)

        self._close_dur_label = QLabel(self._input_box_frame)
        self._close_dur_line_edit = QLineEdit(self._input_box_frame)
        self._close_dur_line_edit.setFixedWidth(80)
        self._close_inf_check_box = QCheckBox(self._input_box_frame)

        self._debounce_label = QLabel(self._input_box_frame)
        self._debounce_time_line_edit = QLineEdit(self._input_box_frame)
        self._debounce_time_line_edit.setFixedWidth(80)

        self._input_box_grid_layout.addWidget(self._open_dur_label, 0, 0, 1, 1)
        self._input_box_grid_layout.addWidget(self._open_dur_line_edit, 0, 1, 1, 1)
        self._input_box_grid_layout.addWidget(self._open_inf_check_box, 0, 2, 1, 1)
        self._input_box_grid_layout.addWidget(self._close_dur_label, 1, 0, 1, 1)
        self._input_box_grid_layout.addWidget(self._close_dur_line_edit, 1, 1, 1, 1)
        self._input_box_grid_layout.addWidget(self._close_inf_check_box, 1, 2, 1, 1)
        self._input_box_grid_layout.addWidget(self._debounce_label, 2, 0, 1, 1)
        self._input_box_grid_layout.addWidget(self._debounce_time_line_edit, 2, 1, 1, 1)

        """ Set button mode setting display area. """
        self._button_mode_frame = EasyFrame()
        self._button_mode_horiz_layout = QGridLayout(self._button_mode_frame)
        self._button_mode_horiz_layout.setContentsMargins(0, 6, 0, 6)
        self._button_mode_label = QLabel(self._button_mode_frame)
        self._button_mode_selector = QComboBox(self._button_mode_frame)

        self._button_mode_selector.addItem("")
        self._button_mode_selector.addItem("")

        self._button_mode_horiz_layout.addWidget(self._button_mode_label, 0, 0, 1, 1)
        self._button_mode_horiz_layout.addWidget(self._button_mode_selector, 0, 1, 1, 1)

        """ Set control mode setting display area. """
        self._control_mode_label = QLabel(self._button_mode_frame)
        self._control_mode_selector = QComboBox(self._button_mode_frame)

        self._control_mode_selector.addItem("")
        self._control_mode_selector.addItem("")

        self._button_mode_horiz_layout.addWidget(self._control_mode_label, 1, 0, 1, 1)
        self._button_mode_horiz_layout.addWidget(self._control_mode_selector, 1, 1, 1, 1)

        """ Set upload button selection area. """
        # self._upload_control_buttons_frame = EasyFrame()
        # self._upload_control_buttons_layout = QVBoxLayout(self._upload_control_buttons_frame)
        self._upload_settings_button = ClickAnimationButton()

        """ Set manual control selection area. """
        self._manual_control_button_frame = EasyFrame()
        self._manual_control_button_layout = QHBoxLayout(self._manual_control_button_frame)

        self._manual_control_open_button = ClickAnimationButton()
        self._manual_control_close_button = ClickAnimationButton()

        self._manual_control_button_layout.addWidget(self._manual_control_open_button)
        self._manual_control_button_layout.addWidget(self._manual_control_close_button)
        self._manual_control_button_layout.setMargin(0)

        # self._upload_control_buttons_layout.addWidget(self._manual_control_button_frame)
        # self._upload_control_buttons_layout.addWidget(self._presets_frame)
        # self._upload_control_buttons_layout.addWidget(self._upload_settings_button)

        """ device settings display """
        self._dev_sets_frame = EasyFrame()

        self._dev_sets_layout = QVBoxLayout(self._dev_sets_frame)

        """ Show/Hide Configuration tab """
        # self.config_tab = CollapsingTab(self, self.dev_sets_frame, max_width=400, log_handlers=log_handlers)
        # self.config_tab.set_tab_height(self.tab_height)
        # self.layout().addWidget(self.config_tab, 0, 1, Qt.AlignRight)

        """Configuration popup"""
        # self._config_button_frame = EasyFrame()
        # self._config_button_frame_layout = QHBoxLayout(self._config_button_frame)

        self.config_button = ClickAnimationButton()
        self.config_button.clicked.connect(self._config_button_handler)

        # self._config_button_frame_layout.addWidget(self.config_button)

        """ Configuration menu """
        # self._menu_bar = QMenuBar()
        # self._menu_bar.setMaximumWidth(self.width() - 17)
        # self._menu_bar.setMouseTracking(True)
        # self._config_action = QAction()
        # self._menu_bar.addAction(self._config_action)
        # self._config_action.triggered.connect(self._config_button_handler)
        # self.layout().setMenuBar(self._menu_bar)

        self._config_win = ConfigPopUp()
        self._config_win.setMinimumSize(self._popup_min[0], self._popup_min[1])
        self._config_win.setMaximumSize(self._popup_max[0], self._popup_max[1])
        self._config_win.setLayout(self._dev_sets_layout)

        """ Add widgets to layout. """
        self._dev_sets_layout.addWidget(self._config_frame)
        self._dev_sets_layout.addWidget(self._input_box_frame)
        self._dev_sets_layout.addWidget(self._button_mode_frame)
        # self._dev_sets_layout.addWidget(self._manual_control_button_frame)
        self._dev_sets_layout.addWidget(self._nhtsa_button)
        self._dev_sets_layout.addWidget(self._eblindfold_button)
        self._dev_sets_layout.addWidget(self._direct_control_button)
        self._dev_sets_layout.addWidget(self._upload_settings_button)

        self.layout().addWidget(self.config_button, 0, 0, Qt.AlignTop | Qt.AlignRight)
        self.config_button.setFixedSize(30, 25)

        # self.layout().addWidget(self._manual_control_button_frame, 0, 0, Qt.AlignBottom)
        # self._manual_control_button_frame.setFixedSize(150, 45)

        self.layout().addWidget(self._manual_control_button_frame, 0, 0, Qt.AlignBottom | Qt.AlignLeft)
        # self.layout().addWidget(self._manual_control_open_button, 0, 0, Qt.AlignBottom | Qt.AlignLeft)
        # self.layout().addWidget(self._manual_control_close_button, 0, 0, Qt.AlignBottom | Qt.AlignRight)
        self._manual_control_open_button.setFixedSize(70, 25)
        self._manual_control_close_button.setFixedSize(70, 25)

        self.layout().setMargin(0)

        self._strings = dict()
        self._lang_enum = LangEnum.ENG
        self.setMinimumSize(self._subwindow_width, self._subwindow_height)
        self.resize(self._subwindow_width, self._subwindow_height)
        self._logger.debug("Initialized")

    def add_graph(self, graph) -> None:
        """
        Add Graph to view.
        :return None:
        """
        self._logger.debug("running")
        self.layout().addWidget(graph, 0, 0)
        self.config_button.raise_()
        self._manual_control_button_frame.raise_()
        # self._manual_control_open_button.raise_()
        # self._manual_control_close_button.raise_()
        self._logger.debug("done")

    def _config_button_handler(self) -> None:
        """
        handles the config button
        :return None:
        """
        self._logger.debug("running")
        self._config_win.exec_()
        self._logger.debug("done")

    def set_config_val_line_edit_handler(self, func: classmethod) -> None:
        """
        Sets the config val line handler.
        :param func: classmethod that handles the config val line.
        :return None:
        """
        self._logger.debug("running")
        self._config_val_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_nhtsa_button_handler(self, func: classmethod) -> None:
        """
        Sets NHTSA button press handler.
        :param func: classmethod that handles the NHTSA button.
        :return None:
        """
        self._logger.debug("running")
        self._nhtsa_button.clicked.connect(func)
        self._logger.debug("done")

    def set_eblindfold_button_handler(self, func: classmethod) -> None:
        """
        Sets eBlindfold button press handler.
        :param func: classmethod that handles the eBlindfold button.
        :return None:
        """
        self._logger.debug("running")
        self._eblindfold_button.clicked.connect(func)
        self._logger.debug("done")

    def set_direct_control_button_handler(self, func: classmethod) -> None:
        """
        Sets Direct Control button press handler.
        :param func: classmethod that handles the Direct Control button.
        :return None:
        """
        self._logger.debug("running")
        self._direct_control_button.clicked.connect(func)
        self._logger.debug("done")

    def set_open_dur_line_edit_handler(self, func: classmethod) -> None:
        """
        Sets open duration line edit handler.
        :param func: classmethod that handles the line edit.
        :return None:
        """
        self._logger.debug("running")
        self._open_dur_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_close_dur_line_edit_handler(self, func: classmethod) -> None:
        """
        Sets close duration line edit handler.
        :param func: classmethod that handles the line edit.
        :return None:
        """
        self._logger.debug("running")
        self._close_dur_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_open_inf_check_box_handler(self, func: classmethod) -> None:
        """
        Sets open INF checkbox handler.
        :param func: classmethod that handles the checkbox, requires bool param.
        :return None:
        """
        self._logger.debug("running")
        self._open_inf_check_box.stateChanged.connect(func)
        self._logger.debug("done")

    def set_close_inf_check_box_handler(self, func: classmethod) -> None:
        """
        Sets close INF checkbox handler.
        :param func: classmethod that handles the checkbox, requires bool param.
        :return None:
        """
        self._logger.debug("running")
        self._close_inf_check_box.stateChanged.connect(func)
        self._logger.debug("done")

    def set_debounce_time_line_edit_handler(self, func: classmethod) -> None:
        """
        Sets debounce time line edit handler.
        :param func: classmethod that handles the line edit.
        :return None:
        """
        self._logger.debug("running")
        self._debounce_time_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_button_mode_selector_handler(self, func: classmethod) -> None:
        """
        Sets button mode combo box handler.
        :param func: classmethod that handles the combo.
        :return None:
        """
        self._logger.debug("running")
        self._button_mode_selector.currentIndexChanged.connect(func)
        self._logger.debug("done")

    def set_control_mode_selector_handler(self, func: classmethod) -> None:
        """
        Sets button mode combo box handler.
        :param func: classmethod that handles the combo.
        :return None:
        """
        self._logger.debug("running")
        self._control_mode_selector.currentIndexChanged.connect(func)
        self._logger.debug("done")

    def set_upload_settings_button_handler(self, func: classmethod) -> None:
        """
        Sets upload settings button handler.
        :param func: classmethod that handles the button.
        :return None:
        """
        self._logger.debug("running")
        self._upload_settings_button.clicked.connect(func)
        self._logger.debug("done")

    def set_manual_control_open_button_handler(self, func: classmethod) -> None:
        """
        Sets manual open button handler.
        :param func: classmethod that handles the button.
        :return None:
        """
        self._logger.debug("running")
        self._manual_control_open_button.clicked.connect(func)
        self._logger.debug("done")

    def set_manual_control_close_button_handler(self, func: classmethod) -> None:
        """
        Sets manual close button handler.
        :param func: classmethod that handles the button.
        :return None:
        """
        self._logger.debug("running")
        self._manual_control_close_button.clicked.connect(func)
        self._logger.debug("done")

    @property
    def config_text(self) -> str:
        """
        Get the string value found in the config text box.
        :return str: string value in the text box.
        """
        return self._config_val_line_edit.text()

    @config_text.setter
    def config_text(self, val: str) -> None:
        """
        Set the string value found in the config text box.
        :param val: string value to set the config text box.
        :return None:
        """
        self._logger.debug("running")
        self._config_val_line_edit.setText(val)
        self._logger.debug("done")

    @property
    def open_duration(self) -> str:
        """
        Get the string value found in the open duration text box.
        :return str: string value in the text box.
        """
        return self._open_dur_line_edit.text()

    @open_duration.setter
    def open_duration(self, val: str) -> None:
        """
        Set the string value found in the open duration text box.
        :param val: string value to set the open duration text box.
        :return None:
        """
        self._logger.debug("running")
        self._open_dur_line_edit.setText(val)
        self._logger.debug("done")

    @property
    def close_duration(self) -> str:
        """
        Get the string value found in the close duration text box.
        :return str: string value in the text box.
        """
        return self._close_dur_line_edit.text()

    @close_duration.setter
    def close_duration(self, val: str) -> None:
        """
        Set the string value found in the close duration text box.
        :param val: string value to set the close duration text box.
        :return None:
        """
        self._logger.debug("running")
        self._close_dur_line_edit.setText(val)
        self._logger.debug("done")

    @property
    def debounce_val(self) -> str:
        """
        Get the string value found in the debounce time text box.
        :return str: string value in the text box.
        """
        return self._debounce_time_line_edit.text()

    @debounce_val.setter
    def debounce_val(self, val: str) -> None:
        """
        Set the string value found in the debounce time text box.
        :param val: string value to set the debounce text box.
        :return None:
        """
        self._logger.debug("running")
        self._debounce_time_line_edit.setText(val)
        self._logger.debug("done")

    @property
    def open_inf_check_box(self) -> bool:
        """
        Get the check box state.
        :return bool: returns true if the box is checked.
        """
        return self._open_inf_check_box.isChecked()

    @open_inf_check_box.setter
    def open_inf_check_box(self, val: bool) -> None:
        """
        Set the check box state.
        :param val: bool value to set the check box.
        :return None:
        """
        self._logger.debug("running")
        self._open_inf_check_box.setChecked(val)
        self._logger.debug("done")

    @property
    def close_inf_check_box(self) -> bool:
        """
        Get the check box state.
        :return bool: returns true if the box is checked.
        """
        return self._close_inf_check_box.isChecked()

    @close_inf_check_box.setter
    def close_inf_check_box(self, val: bool) -> None:
        """
        Set the check box state.
        :param val: bool value to set the check box.
        :return None:
        """
        self._logger.debug("running")
        self._close_inf_check_box.setChecked(val)
        self._logger.debug("done")

    @property
    def button_mode(self) -> int:
        """
        Get index of button mode.
        :return int: index of current button mode.
        """
        return self._button_mode_selector.currentIndex()

    @button_mode.setter
    def button_mode(self, val: int) -> None:
        """
        Set index of button mode.
        :return None:
        """
        self._logger.debug("running")
        self._button_mode_selector.setCurrentIndex(val)
        self._logger.debug("done")

    @property
    def control_mode(self) -> int:
        """
        Get index of button mode.
        :return int: index of current button mode.
        """
        return self._control_mode_selector.currentIndex()

    @control_mode.setter
    def control_mode(self, val: int) -> None:
        """
        Set index of button mode.
        :return None:
        """
        self._logger.debug("running")
        self._control_mode_selector.setCurrentIndex(val)
        self._logger.debug("done")

    def set_open_dur_err(self, err: bool) -> None:
        """
        Set this text entry to error style depending on err.
        :param err: If this text entry needs to be error styel
        :return None:
        """
        self._logger.debug("running")
        if err:
            self._open_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self._open_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    def set_close_dur_err(self, err: bool) -> None:
        """
        Set this text entry to error style depending on err.
        :param err: If this text entry needs to be error styel
        :return None:
        """
        self._logger.debug("running")
        if err:
            self._close_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self._close_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    def set_debounce_err(self, err: bool) -> None:
        """
        Set this text entry to error style depending on err.
        :param err: If this text entry needs to be error styel
        :return None:
        """
        self._logger.debug("running")
        if err:
            self._debounce_time_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self._debounce_time_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    @property
    def language(self) -> LangEnum:
        """
        Get the current language setting
        :return LangEnum: The current language enumerator being used
        """
        return self._lang_enum

    @language.setter
    def language(self, lang: LangEnum) -> None:
        """
        Set the language for this view object and reload the text and tooltips.
        :param lang: the language to use.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._set_texts()
        self._set_tooltips()
        self._logger.debug("done")

    def set_upload_button(self, is_active: bool) -> None:
        """
        Set upload button activity to is_active.
        :param is_active: Whether this button should be active.
        :return None:
        """
        self._logger.debug("running")
        self._upload_settings_button.setEnabled(is_active)
        self._logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set text fields of view object.
        :return None:
        """
        self._logger.debug("running")
        self._config_label.setText(self._strings[StringsEnum.CONFIG_LABEL])
        self._config_val_line_edit.setText(self._strings[StringsEnum.CONFIG_LABEL])
        self._nhtsa_button.setText(self._strings[StringsEnum.NHTSA_LABEL])
        self._eblindfold_button.setText(self._strings[StringsEnum.EBLIND_LABEL])
        self._direct_control_button.setText(self._strings[StringsEnum.DCON_LABEL])
        self._open_dur_label.setText(self._strings[StringsEnum.OPEN_DURATION_LABEL])
        self._open_inf_check_box.setText(self._strings[StringsEnum.INF_LABEL])
        self._close_dur_label.setText(self._strings[StringsEnum.CLOSE_DURATION_LABEL])
        self._close_inf_check_box.setText(self._strings[StringsEnum.INF_LABEL])
        self._debounce_label.setText(self._strings[StringsEnum.DEBOUNCE_LABEL])
        self._button_mode_label.setText(self._strings[StringsEnum.BUTTON_MODE_LABEL])
        self._button_mode_selector.setItemText(0, self._strings[StringsEnum.HOLD_VAL_LABEL])
        self._button_mode_selector.setItemText(1, self._strings[StringsEnum.CLICK_VAL_LABEL])
        self._control_mode_label.setText(self._strings[StringsEnum.CONTROL_MODE_LABEL])
        self._control_mode_selector.setItemText(0, self._strings[StringsEnum.LENS_VAL_LABEL])
        self._control_mode_selector.setItemText(1, self._strings[StringsEnum.TRIAL_VAL_LABEL])
        self._upload_settings_button.setText(self._strings[StringsEnum.UPLOAD_BUTTON_LABEL])
        self._manual_control_open_button.setText(self._strings[StringsEnum.MANUAL_OPEN_LABEL])
        self._manual_control_close_button.setText(self._strings[StringsEnum.MANUAL_CLOSE_LABEL])
        self.config_button.setText(self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self.config_button.setText("...")
        # self._config_action.setText(self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._config_win.setWindowTitle(self.get_name() + " " + self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._logger.debug("done")

    def _set_tooltips(self) -> None:
        """
        Set tooltip text fields of view object.
        :return None:
        """
        self._logger.debug("running")
        self._config_label.setToolTip(self._strings[StringsEnum.CONFIG_LABEL_TOOLTIP])
        self._config_val_line_edit.setToolTip(self._strings[StringsEnum.CONFIG_LABEL_TOOLTIP])
        self._open_dur_label.setToolTip(self._strings[StringsEnum.OPEN_DURATION_TOOLTIP])
        self._close_dur_label.setToolTip(self._strings[StringsEnum.CLOSE_DURATION_TOOLTIP])
        self._debounce_label.setToolTip(self._strings[StringsEnum.DEBOUNCE_TOOLTIP])
        self._button_mode_label.setToolTip(self._strings[StringsEnum.BUTTON_MODE_TOOLTIP])
        self._control_mode_label.setToolTip(self._strings[StringsEnum.CONTROL_MODE_TOOLTIP])
        self._upload_settings_button.setToolTip(self._strings[StringsEnum.UPLOAD_BUTTON_TOOLTIP])
        self._manual_control_open_button.setToolTip(self._strings[StringsEnum.MANUAL_OPEN_TOOLTIP])
        self._manual_control_close_button.setToolTip(self._strings[StringsEnum.MANUAL_CLOSE_TOOLTIP])
        self.config_button.setToolTip(self._strings[StringsEnum.CONFIG_TAB_TOOLTIP])
        self._logger.debug("done")

    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     self._menu_bar.setMaximumWidth(self.width())
    #     return super().resizeEvent(event)
