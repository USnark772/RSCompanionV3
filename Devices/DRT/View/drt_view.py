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

from logging import getLogger
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QSlider, QGridLayout, QLineEdit
from PySide2.QtCore import Qt, QSize
from Model.app_helpers import ClickAnimationButton, EasyFrame
from Model.app_defs import tab_line_edit_compliant_style, tab_line_edit_error_style
from Devices.AbstractDevice.View.abstract_view import AbstractView


class DRTView(AbstractView):
    def __init__(self, parent, name, ch):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        super().__init__(parent, name)
        self.setLayout(QHBoxLayout())

        # Data output display
        self.dev_data_layout = QVBoxLayout()

        # device settings display
        self.dev_sets_frame = EasyFrame()
        self.layout().addWidget(self.dev_sets_frame)
        self.dev_sets_layout = QVBoxLayout(self.dev_sets_frame)

        self.config_horizontal_layout = QHBoxLayout()
        # TODO: fix EasyFrame QLayout issue
        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        # Set configuration value display area
        self.config_frame = EasyFrame()
        self.config_layout = QHBoxLayout(self.config_frame)
        self.config_label = QLabel(self.config_frame)
        self.config_label.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_label)
        self.config_val = QLabel(self.config_frame)
        self.config_val.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_val)
        self.dev_sets_layout.addWidget(self.config_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        # Set preset button selection area.
        self.presets_frame = EasyFrame()
        self.presets_layout = QVBoxLayout(self.presets_frame)
        self.iso_button = ClickAnimationButton(self.presets_frame)
        self.presets_layout.addWidget(self.iso_button)
        self.dev_sets_layout.addWidget(self.presets_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        # Set stim intensity settings display area.
        self.slider_frame = EasyFrame()
        self.slider_layout = QVBoxLayout(self.slider_frame)
        self.slider_label_layout = QHBoxLayout(self.slider_frame)
        self.stim_intens_label = QLabel(self.slider_frame)
        self.stim_intens_label.setAlignment(Qt.AlignLeft)
        self.slider_label_layout.addWidget(self.stim_intens_label)
        self.stim_intens_val = QLabel(self.slider_frame)
        self.stim_intens_val.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.slider_label_layout.addWidget(self.stim_intens_val)
        self.slider_layout.addLayout(self.slider_label_layout)
        self.stim_intens_slider = QSlider(self.slider_frame)
        self.stim_intens_slider.setMinimum(1)
        self.stim_intens_slider.setMaximum(100)
        self.stim_intens_slider.setSliderPosition(100)
        self.stim_intens_slider.setOrientation(Qt.Horizontal)
        self.stim_intens_slider.setTickPosition(QSlider.TicksBelow)
        self.stim_intens_slider.setTickInterval(10)
        self.slider_layout.addWidget(self.stim_intens_slider)
        self.dev_sets_layout.addWidget(self.slider_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        # Set stim duration, upper isi and lower isi settings display area.
        self.input_box_frame = EasyFrame()
        self.input_box_layout = QGridLayout(self.input_box_frame)
        self.stim_dur_line_edit = QLineEdit(self.input_box_frame)
        self.stim_dur_line_edit.setMaximumSize(QSize(100, 16777215))
        self.input_box_layout.addWidget(self.stim_dur_line_edit, 0, 1, 1, 1)
        self.upper_isi_label = QLabel(self.input_box_frame)
        self.input_box_layout.addWidget(self.upper_isi_label, 1, 0, 1, 1)
        self.upper_isi_line_edit = QLineEdit(self.input_box_frame)
        self.upper_isi_line_edit.setMaximumSize(QSize(100, 16777215))
        self.input_box_layout.addWidget(self.upper_isi_line_edit, 1, 1, 1, 1)
        self.stim_dur_label = QLabel(self.input_box_frame)
        self.input_box_layout.addWidget(self.stim_dur_label, 0, 0, 1, 1)
        self.lower_isi_line_edit = QLineEdit(self.input_box_frame)
        self.lower_isi_line_edit.setMaximumSize(QSize(100, 16777215))
        self.input_box_layout.addWidget(self.lower_isi_line_edit, 2, 1, 1, 1)
        self.lower_isi_label = QLabel(self.input_box_frame)
        self.input_box_layout.addWidget(self.lower_isi_label, 2, 0, 1, 1)
        self.dev_sets_layout.addWidget(self.input_box_frame)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        # Set upload button selection area.
        self.upload_settings_button = ClickAnimationButton()
        self.dev_sets_layout.addWidget(self.upload_settings_button)

        self.dev_sets_layout.addWidget(EasyFrame(line=True))

        self._logger.debug("Initialized")

    def set_stim_dur_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self._logger.debug("running")
        self.stim_dur_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_stim_intens_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self._logger.debug("running")
        self.stim_intens_slider.valueChanged.connect(func)
        self._logger.debug("done")

    def set_upper_isi_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self._logger.debug("running")
        self.upper_isi_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_lower_isi_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self._logger.debug("running")
        self.lower_isi_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_iso_button_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self.iso_button.clicked.connect(func)

    def set_upload_button_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self.upload_settings_button.clicked.connect(func)

    def get_stim_dur(self):
        """

        :return:
        """
        return self.stim_dur_line_edit.text()

    def set_stim_dur(self, val) -> None:
        """
        Set display value of stim duration
        :param val:
        :return:
        """
        self._logger.debug("running")
        self.stim_dur_line_edit.setText(str(val))
        self._logger.debug("done")

    def set_stim_dur_err(self, is_error) -> None:
        """
        Set display of error in stim duration
        :param is_error:
        :return:
        """
        self._logger.debug("running")
        if is_error:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    def get_stim_intens(self):
        """

        :return:
        """
        return self.stim_intens_slider.value()

    def set_stim_intens(self, val) -> None:
        """
        Set display value of stim intensity
        :param val:
        :return:
        """
        self._logger.debug("running")
        self.stim_intens_slider.setValue(int(val))
        self.set_stim_intens_val_label(val)
        self._logger.debug("done")

    def set_stim_intens_err(self) -> None:
        """

        :return:
        """

    def get_upper_isi(self):
        """

        :return:
        """
        return self.upper_isi_line_edit.text()

    def set_upper_isi(self, val) -> None:
        """
        Set display value of upper isi
        :param val:
        :return:
        """
        self._logger.debug("running")
        self.upper_isi_line_edit.setText(str(val))
        self._logger.debug("done")

    def set_upper_isi_err(self, is_error) -> None:
        """
        Set display of error in upper isi line edit
        :param is_error:
        :return:
        """
        self._logger.debug("running")
        if is_error:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    def get_lower_isi(self):
        """

        :return:
        """
        return self.lower_isi_line_edit.text()

    def set_lower_isi(self, val) -> None:
        """
        Set display value of lower isi
        :param val:
        :return:
        """
        self._logger.debug("running")
        self.lower_isi_line_edit.setText(str(val))
        self._logger.debug("done")

    def set_lower_isi_err(self, is_error) -> None:
        """
        Set display of error in lower isi line edit
        :param is_error:
        :return:
        """
        self._logger.debug("running")
        if is_error:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    def set_upload_button(self, is_active) -> None:
        """

        :return:
        """
        self._logger.debug("running")
        self.upload_settings_button.setEnabled(is_active)
        self._logger.debug("done")
