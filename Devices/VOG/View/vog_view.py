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
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSlider, QGridLayout, QLineEdit, QVBoxLayout, QTabWidget,\
    QCheckBox, QComboBox
from PySide2.QtCore import Qt, QSize
from Model.app_helpers import ClickAnimationButton, EasyFrame
from Model.app_defs import tab_line_edit_compliant_style, tab_line_edit_error_style
from Devices.VOG.Resources.vog_strings import strings, StringsEnum, LangEnum
from Devices.AbstractDevice.View.abstract_view import AbstractView
from Devices.AbstractDevice.View.collapsible_tab_widget import CollapsingTab


class VOGView(AbstractView):
    def __init__(self, name, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(name)

        # device settings display
        self.dev_sets_frame = EasyFrame()
        # self.dev_sets_frame.setMaximumSize(250, 350)

        self.dev_sets_layout = QVBoxLayout(self.dev_sets_frame)
        self.config_horizontal_layout = QHBoxLayout()
        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        # Show/Hide Configuration tab
        self.config_tab = CollapsingTab(self, self.dev_sets_frame, log_handlers, 400)
        self.layout().addWidget(self.config_tab, 0, 1, Qt.AlignRight)
        self.config_tab.set_tab_height(450)

        """ Set configuration value display area"""
        self._config_frame = EasyFrame()
        self._config_vertical_layout = QVBoxLayout(self._config_frame)
        self._config_label = QLabel(self._config_frame)
        self._config_label.setAlignment(Qt.AlignCenter)
        self._config_vertical_layout.addWidget(self._config_label)
        self._config_val_line_edit = QLineEdit(self._config_frame)
        self._config_val_line_edit.setAlignment(Qt.AlignCenter)
        self._config_vertical_layout.addWidget(self._config_val_line_edit)
        self.dev_sets_layout.addWidget(self._config_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        """ Set preset button selection area. """
        self._presets_frame = EasyFrame()
        self._presets_vert_layout = QVBoxLayout(self._presets_frame)
        self._nhtsa_button = ClickAnimationButton(self._presets_frame)
        self._presets_vert_layout.addWidget(self._nhtsa_button)
        self._eblindfold_button = ClickAnimationButton(self._presets_frame)
        self._presets_vert_layout.addWidget(self._eblindfold_button)
        self._direct_control_button = ClickAnimationButton(self._presets_frame)
        self._presets_vert_layout.addWidget(self._direct_control_button)
        self.dev_sets_layout.addWidget(self._presets_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        """ Set open duration, close duration, and debounce time settings display area. """
        self._input_box_frame = EasyFrame()
        self._input_box_grid_layout = QGridLayout(self._input_box_frame)
        self._input_box_grid_layout.setContentsMargins(0, 6, 0, 6)
        self._open_dur_label = QLabel(self._input_box_frame)
        self._input_box_grid_layout.addWidget(self._open_dur_label, 0, 0, 1, 1)
        self._open_dur_line_edit = QLineEdit(self._input_box_frame)
        self._open_dur_line_edit.setFixedWidth(80)
        self._input_box_grid_layout.addWidget(self._open_dur_line_edit, 0, 1, 1, 1)
        self._open_inf_check_box = QCheckBox(self._input_box_frame)
        self._input_box_grid_layout.addWidget(self._open_inf_check_box, 0, 2, 1, 1)
        self._close_dur_label = QLabel(self._input_box_frame)
        self._input_box_grid_layout.addWidget(self._close_dur_label, 1, 0, 1, 1)
        self._close_dur_line_edit = QLineEdit(self._input_box_frame)
        self._close_dur_line_edit.setFixedWidth(80)
        self._input_box_grid_layout.addWidget(self._close_dur_line_edit, 1, 1, 1, 1)
        self._close_inf_check_box = QCheckBox(self._input_box_frame)
        self._input_box_grid_layout.addWidget(self._close_inf_check_box, 1, 2, 1, 1)
        self._debounce_label = QLabel(self._input_box_frame)
        self._input_box_grid_layout.addWidget(self._debounce_label, 2, 0, 1, 1)
        self._debounce_time_line_edit = QLineEdit(self._input_box_frame)
        self._debounce_time_line_edit.setFixedWidth(80)
        self._input_box_grid_layout.addWidget(self._debounce_time_line_edit, 2, 1, 1, 1)
        self.dev_sets_layout.addWidget(self._input_box_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        """ Set button mode setting display area. """
        self._button_mode_frame = EasyFrame()
        self._button_mode_horiz_layout = QHBoxLayout(self._button_mode_frame)
        self._button_mode_label = QLabel(self._button_mode_frame)
        self._button_mode_horiz_layout.addWidget(self._button_mode_label)
        self._button_mode_selector = QComboBox(self._button_mode_frame)
        self._button_mode_selector.addItem("")
        self._button_mode_selector.addItem("")
        self._button_mode_horiz_layout.addWidget(self._button_mode_selector)
        self.dev_sets_layout.addWidget(self._button_mode_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        """ Set upload button selection area. """
        self._upload_settings_button = ClickAnimationButton()
        self.dev_sets_layout.addWidget(self._upload_settings_button)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        """ Set manual control selection area. """
        self._manual_control_button = ClickAnimationButton()
        self.dev_sets_layout.addWidget(self._manual_control_button)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        self._strings = dict()
        self.setMinimumWidth(760)
        self.setFixedHeight(500)
        self._logger.debug("Initialized")

    def add_graph(self, graph) -> None:
        """
        Add Graph to view
        :return None:
        """
        self.layout().addWidget(graph, 0, 0)

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this view's language and reload the text and tooltips.
        :param lang: The lang enum to use.
        :return: None.
        """
        self._strings = strings[lang]
        self._set_texts()
        self._set_tooltips()

    def _set_texts(self) -> None:
        """
        Set text fields of view object.
        :return None:
        """
        self._logger.debug("running")
        self._config_label.setText(self._strings[StringsEnum.CONFIG_LABEL])
        self._config_val_line_edit.setText(self._strings[StringsEnum.DCON_LABEL])
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
        self._upload_settings_button.setText(self._strings[StringsEnum.UPLOAD_BUTTON_LABEL])
        self._manual_control_button.setText(self._strings[StringsEnum.TOGGLE_LABEL])
        self.config_tab.set_tab_text(self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._logger.debug("done")

    # TODO: implement this
    def _set_tooltips(self) -> None:
        """
        Set tooltip text fields of view object.
        :return None:
        """
        self._logger.debug("running")
        self._logger.debug("done")
