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

from logging import getLogger, StreamHandler

from PySide2.QtWidgets import QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QCheckBox, QComboBox, QLineEdit, \
    QSizePolicy, QSpacerItem
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from Devices.AbstractDevice.View.abstract_view import AbstractView
from Devices.AbstractDevice.View.collapsible_tab_widget import CollapsingTab
from Devices.Camera.Resources.cam_strings import strings, StringsEnum, LangEnum
from Model.app_helpers import EasyFrame

max_height = 500
combo_box_height = 22


class CamView(AbstractView):
    def __init__(self, name: str, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(name)

        self.subwindow_height = 600
        self.tab_height = int(self.subwindow_height * 0.9)

        self.initialization_bar_frame = EasyFrame()
        self.initialization_bar_layout = QVBoxLayout(self.initialization_bar_frame)
        self.initialization_bar_label = QLabel(self.initialization_bar_frame)
        self.initialization_bar_layout.addWidget(self.initialization_bar_label)
        self.initialization_bar = QProgressBar(self.initialization_bar_frame)
        self.initialization_bar.setTextVisible(True)
        self.initialization_bar.setAlignment(Qt.AlignHCenter)
        self.initialization_bar.setMaximumHeight(15)
        self.initialization_bar_layout.addWidget(self.initialization_bar)
        self.initialization_bar_frame.setMaximumHeight(70)

        self.show_cam_checkbox_frame = EasyFrame()
        self.show_cam_checkbox_layout = QHBoxLayout(self.show_cam_checkbox_frame)
        self.show_cam_checkbox_label = QLabel(self.show_cam_checkbox_frame)
        self.show_cam_checkbox_label.setAlignment(Qt.AlignLeft)
        self.show_cam_checkbox_layout.addWidget(self.show_cam_checkbox_label)
        self.show_cam_checkbox_layout.addWidget(EasyFrame(vert=True))
        self.show_cam_checkbox = QCheckBox()
        self.show_cam_checkbox.setChecked(True)
        self.show_cam_checkbox.setLayoutDirection(Qt.RightToLeft)
        self.show_cam_checkbox_layout.addWidget(self.show_cam_checkbox)
        self.show_cam_checkbox_frame.setMaximumHeight(50)

        self.frame_size_selector_frame = EasyFrame()
        self.frame_size_selector_layout = QHBoxLayout(self.frame_size_selector_frame)
        self.frame_size_selector_label = QLabel(self.frame_size_selector_frame)
        self.frame_size_selector_label.setAlignment(Qt.AlignLeft)
        self.frame_size_selector_layout.addWidget(self.frame_size_selector_label)
        self.frame_size_selector_layout.addWidget(EasyFrame(vert=True))
        self.frame_size_selector = QComboBox(self.frame_size_selector_frame)
        self.frame_size_selector.setMaximumHeight(combo_box_height)
        self.frame_size_selector_layout.addWidget(self.frame_size_selector)
        self.frame_size_selector_frame.setMaximumHeight(50)

        self.frame_rotation_setting_frame = EasyFrame()
        self.frame_rotation_setting_layout = QHBoxLayout(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_label = QLabel(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_label.setAlignment(Qt.AlignLeft)
        self.frame_rotation_setting_layout.addWidget(self.frame_rotation_setting_label)
        self.frame_rotation_setting_layout.addWidget(EasyFrame(vert=True))
        self.frame_rotation_setting_entry_box = QLineEdit(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_entry_box.setMaximumSize(90, 20)
        self.frame_rotation_setting_entry_box.setAlignment(Qt.AlignRight)
        self.frame_rotation_setting_layout.addWidget(self.frame_rotation_setting_entry_box)
        self.frame_rotation_setting_frame.setMaximumHeight(50)

        self.image_display_frame = EasyFrame()
        self.image_display_layout = QVBoxLayout(self.image_display_frame)
        self.image_display_label = QLabel(self.image_display_frame)
        self.image_display_label.setAlignment(Qt.AlignHCenter)
        self.image_display_layout.addWidget(self.image_display_label)
        self.image_display = QLabel(self.image_display_frame)
        self.image_display.setAlignment(Qt.AlignHCenter)
        self.image_display_layout.addWidget(self.image_display)

        self.fps_display_frame = EasyFrame()
        self.fps_display_layout = QHBoxLayout(self.fps_display_frame)
        self.fps_display_label = QLabel(self.fps_display_frame)
        self.fps_display_label.setAlignment(Qt.AlignRight)
        self.fps_display_layout.addWidget(self.fps_display_label)
        self.fps_display_value = QLabel(self.fps_display_frame)
        self.fps_display_value.setAlignment(Qt.AlignLeft)
        self.fps_display_layout.addWidget(self.fps_display_value)

        spacer = QSpacerItem(1, 1, vData=QSizePolicy.Expanding)

        self.dev_sets_frame = EasyFrame()

        self.dev_sets_layout = QVBoxLayout(self.dev_sets_frame)

        self.config_tab = CollapsingTab(self, self.dev_sets_frame, log_handlers, max_width=350)
        self.layout().addWidget(self.config_tab, 0, 1, Qt.AlignRight)
        self.config_tab.set_tab_height(self.tab_height)

        self.dev_sets_layout.addWidget(self.initialization_bar_frame)
        self.dev_sets_layout.addWidget(EasyFrame(line=True))
        self.dev_sets_layout.addWidget(self.frame_size_selector_frame)
        self.dev_sets_layout.addWidget(self.frame_rotation_setting_frame)
        self.dev_sets_layout.addWidget(EasyFrame(line=True))
        self.dev_sets_layout.addWidget(self.show_cam_checkbox_frame)
        self.dev_sets_layout.addWidget(self.fps_display_frame)
        self.dev_sets_layout.addWidget(EasyFrame(line=True))
        self.dev_sets_layout.addItem(spacer)
        self.layout().addWidget(self.image_display_frame, 0, 0)

        self._strings = dict()
        self._logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The language to use.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._set_texts()
        self._set_tooltips()
        self._logger.debug("done")

    def add_use_cam_button_handler(self, func):
        self.logger.debug("running")
        self.use_cam_button.clicked.connect(func)
        self.logger.debug("done")

    def add_show_cam_button_handler(self, func):
        self.logger.debug("running")
        self.show_cam_checkbox.toggled.connect(func)
        self.logger.debug("done")

    def add_bw_button_handler(self, func):
        self.logger.debug("running")
        self.bw_button.clicked.connect(func)
        self.logger.debug("done")

    def add_settings_toggle_button_handler(self, func):
        self.logger.debug("running")
        self.settings_toggle_button.clicked.connect(func)
        self.logger.debug("done")

    def add_frame_size_selector_handler(self, func):
        self.logger.debug("running")
        self.frame_size_selector.activated.connect(func)
        self.logger.debug("done")

    def add_frame_rotation_handler(self, func):
        self.logger.debug("running")
        self.frame_rotation_setting_entry_box.textChanged.connect(func)
        self.logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set the texts in this view object.
        :return None:
        """
        self._logger.debug("running")
        self.initialization_bar_label.setText(self._strings[StringsEnum.INITIALIZATION_BAR_LABEL])
        self.initialization_bar.setValue(0)
        self.image_display_label.setText(self._strings[StringsEnum.IMAGE_DISPLAY_LABEL])
        self.image_display.setText(self._strings[StringsEnum.IMAGE_DISPLAY])
        self.show_cam_checkbox_label.setText(self._strings[StringsEnum.SHOW_CAM_CHECKBOX_LABEL])
        self.frame_size_selector_label.setText(self._strings[StringsEnum.FRAME_SIZE_SELECTOR_LABEL])
        self.frame_rotation_setting_label.setText(self._strings[StringsEnum.FRAME_ROTATION_SETTING_LABEL])
        self.fps_display_label.setText(self._strings[StringsEnum.FPS_DISPLAY_LABEL])
        self.fps_display_value.setText(self._strings[StringsEnum.FPS_DISPLAY_VALUE])
        self._logger.debug("done")

    def _set_tooltips(self) -> None:
        """
        Set the tooltips in this view object.
        :return None:
        """
        self._logger.debug("running")
        self.show_cam_checkbox_frame.setToolTip(self._strings[StringsEnum.SHOW_CAM_TOOLTIP])
        self.frame_size_selector_frame.setToolTip(self._strings[StringsEnum.FRAME_SIZE_TOOLTIP])
        self.frame_rotation_setting_frame.setToolTip(self._strings[StringsEnum.ROTATION_TOOLTIP])
        self.image_display_frame.setToolTip(self._strings[StringsEnum.IMAGE_DISPLAY_TOOLTIP])
        self.fps_display_frame.setToolTip(self._strings[StringsEnum.FPS_DISPLAY_TOOLTIP])
        self._logger.debug("done")
