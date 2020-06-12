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
from PySide2.QtWidgets import QHBoxLayout, QLabel, QSlider, QGridLayout, QLineEdit, QVBoxLayout, QMenuBar, QAction
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QResizeEvent
from Model.app_helpers import ClickAnimationButton, EasyFrame
from Model.app_defs import tab_line_edit_compliant_style, tab_line_edit_error_style
from Devices.DRT.Resources.drt_strings import strings, StringsEnum, LangEnum
from Devices.AbstractDevice.View.abstract_view import AbstractView
from Devices.AbstractDevice.View.ConfigPopUp import ConfigPopUp


class DRTView(AbstractView):
    def __init__(self, name: str = "DRT_NONE", log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(name)

        """ Min size for the DRT window """
        self._subwindow_height = 300
        self._subwindow_width = 550

        # self.tab_height = int(self.subwindow_height * 0.9)
        """ min and max sizes for the configuration popup """
        self._popup_min = (168, 313)
        self._popup_max = (300, 313)

        """ Set configuration value display area """
        self._config_frame = EasyFrame()
        self._config_layout = QVBoxLayout(self._config_frame)

        self._config_label = QLabel(self._config_frame)
        self._config_label.setAlignment(Qt.AlignCenter)

        self._config_val = QLabel(self._config_frame)
        self._config_val.setAlignment(Qt.AlignCenter)

        self._config_layout.addWidget(self._config_label)
        self._config_layout.addWidget(self._config_val)

        """ Set preset button selection area. """
        self._iso_button = ClickAnimationButton()

        """ Set stim intensity settings display area. """
        self._slider_frame = EasyFrame()
        self._slider_layout = QVBoxLayout(self._slider_frame)
        self._slider_label_layout = QHBoxLayout(self._slider_frame)

        self._stim_intens_label = QLabel(self._slider_frame)
        self._stim_intens_label.setAlignment(Qt.AlignLeft)
        self._stim_intens_val = QLabel(self._slider_frame)
        self._stim_intens_val.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self._slider_layout.addLayout(self._slider_label_layout)

        self._stim_intens_slider = QSlider(self._slider_frame)
        self._stim_intens_slider.setMinimum(1)
        self._stim_intens_slider.setMaximum(100)
        self._stim_intens_slider.setSliderPosition(100)
        self._stim_intens_slider.setOrientation(Qt.Horizontal)
        self._stim_intens_slider.setTickPosition(QSlider.TicksBelow)
        self._stim_intens_slider.setTickInterval(10)

        self._slider_label_layout.addWidget(self._stim_intens_label)
        self._slider_label_layout.addWidget(self._stim_intens_val)
        self._slider_layout.addWidget(self._stim_intens_slider)

        """ Set stim duration, upper isi and lower isi settings display area. """
        self._input_box_frame = EasyFrame()
        self._input_box_layout = QGridLayout(self._input_box_frame)

        self._stim_dur_line_edit = QLineEdit(self._input_box_frame)
        self._stim_dur_line_edit.setMaximumSize(QSize(100, 16777215))
        self._stim_dur_label = QLabel(self._input_box_frame)

        self._upper_isi_label = QLabel(self._input_box_frame)
        self._upper_isi_line_edit = QLineEdit(self._input_box_frame)
        self._upper_isi_line_edit.setMaximumSize(QSize(100, 16777215))

        self._lower_isi_line_edit = QLineEdit(self._input_box_frame)
        self._lower_isi_line_edit.setMaximumSize(QSize(100, 16777215))
        self._lower_isi_label = QLabel(self._input_box_frame)

        self._input_box_layout.addWidget(self._stim_dur_line_edit, 0, 1, 1, 1)
        self._input_box_layout.addWidget(self._upper_isi_label, 1, 0, 1, 1)
        self._input_box_layout.addWidget(self._upper_isi_line_edit, 1, 1, 1, 1)
        self._input_box_layout.addWidget(self._stim_dur_label, 0, 0, 1, 1)
        self._input_box_layout.addWidget(self._lower_isi_line_edit, 2, 1, 1, 1)
        self._input_box_layout.addWidget(self._lower_isi_label, 2, 0, 1, 1)

        """ Set upload button selection area. """
        self._upload_settings_button = ClickAnimationButton()
        self._upload_settings_button.setEnabled(False)

        """ device settings display """
        self._dev_sets_frame = EasyFrame()
        self._dev_sets_layout = QVBoxLayout(self._dev_sets_frame)
        self._config_horizontal_layout = QHBoxLayout()

        """ Configuration popup """
        # check set_texts and set_tooltips if commenting/uncommenting
        self._config_button_frame = EasyFrame()
        self._config_button_frame_layout = QHBoxLayout(self._config_button_frame)

        self.config_button = ClickAnimationButton()
        self.config_button.clicked.connect(self._config_button_handler)

        self._config_button_frame_layout.addWidget(self.config_button)
        self.layout().addWidget(self._config_button_frame, 0, 0, Qt.AlignTop)
        self._config_button_frame.setFixedSize(50, 40)

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

        """ Add all of the widgets to the layout. """
        self._dev_sets_layout.addWidget(self._config_frame)
        self._dev_sets_layout.addWidget(self._input_box_frame)
        self._dev_sets_layout.addWidget(self._slider_frame)
        self._dev_sets_layout.addWidget(EasyFrame(line=True))
        self._dev_sets_layout.addWidget(self._iso_button)
        self._dev_sets_layout.addWidget(self._upload_settings_button)

        self._strings = dict()
        self._lang_enum = LangEnum.ENG
        self.setMinimumSize(self._subwindow_width, self._subwindow_height)
        # self.resize(self._subwindow_width, self._subwindow_height)
        self._logger.debug("Initialized")

    def add_graph(self, graph) -> None:
        """
        Add graph to view
        :return None:
        """
        self._logger.debug("running")
        self.layout().addWidget(graph, 0, 0)
        self._config_button_frame.raise_()
        self._logger.debug("done")

    def _config_button_handler(self) -> None:
        """
        handles the config button
        :return None:
        """
        self._logger.debug("running")
        self._config_win.exec_()
        self._logger.debug("done")

    def set_stim_dur_entry_changed_handler(self, func: classmethod) -> None:
        """
        Add handler for when user changes input value in this field.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._stim_dur_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_stim_intens_entry_changed_handler(self, func: classmethod) -> None:
        """
        Add handler for when user changes input value in this field.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._stim_intens_slider.valueChanged.connect(func)
        self._logger.debug("done")

    def set_upper_isi_entry_changed_handler(self, func: classmethod) -> None:
        """
        Add handler for when user changes input value in this field.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._upper_isi_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_lower_isi_entry_changed_handler(self, func: classmethod) -> None:
        """
        Add handler for when user changes input value in this field.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._lower_isi_line_edit.textChanged.connect(func)
        self._logger.debug("done")

    def set_iso_button_handler(self, func: classmethod) -> None:
        """
        Add handler for when user clicks this button.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._iso_button.clicked.connect(func)
        self._logger.debug("done")

    def set_upload_button_handler(self, func: classmethod) -> None:
        """
        Add handler for when user clicks this button.
        :param func: The handler.
        :return: None.
        """
        self._logger.debug("running")
        self._upload_settings_button.clicked.connect(func)
        self._logger.debug("done")

    @property
    def config_text(self) -> str:
        """
        Get configuration text value
        :return str: text value
        """
        return self._config_val.text()

    @config_text.setter
    def config_text(self, val: str) -> None:
        """
        Set configuration text value
        :param val: text to set
        :return None:
        """
        self._logger.debug("running")
        self._config_val.setText(val)
        self._logger.debug("done")

    @property
    def stim_duration(self) -> str:
        """
        Get the display value of stim duration
        :return str: the display value
        """
        return self._stim_dur_line_edit.text()

    @stim_duration.setter
    def stim_duration(self, val: str) -> None:
        """
        Set display value of stim duration
        :param val:
        :return:
        """
        self._logger.debug("running")
        self._stim_dur_line_edit.setText(str(val))
        self._logger.debug("done")

    def set_stim_dur_err(self, is_error: bool) -> None:
        """
        Set display of error in stim duration
        :param is_error: Whether this line edit should display error.
        :return None:
        """
        self._logger.debug("running")
        if is_error:
            self._stim_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self._stim_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    @property
    def stim_intensity(self) -> int:
        """
        Get the integer value for the stim intensity
        :return int: stim intensity
        """
        return self._stim_intens_slider.value()

    @stim_intensity.setter
    def stim_intensity(self, val: str) -> None:
        """
        Set display value of stim intensity
        :param val:
        :return:
        """
        self._logger.debug("running")
        self._stim_intens_slider.setValue(int(val))
        self.update_stim_intens_val_tooltip()
        self._logger.debug("done")

    def update_stim_intens_val_tooltip(self) -> None:
        """
        Update slider tooltip.
        :return: None.
        """
        self._logger.debug("running")
        self._stim_intens_slider.setToolTip(str(self._stim_intens_slider.value()) + "%")
        self._logger.debug("done")

    @property
    def upper_isi(self) -> str:
        """

        :return str:
        """
        return self._upper_isi_line_edit.text()

    @upper_isi.setter
    def upper_isi(self, val: str) -> None:
        """
        Set display value of upper isi
        :param val:
        :return:
        """
        self._logger.debug("running")
        self._upper_isi_line_edit.setText(str(val))
        self._logger.debug("done")

    def set_upper_isi_err(self, is_error: bool) -> None:
        """
        Set display of error in upper isi line edit
        :param is_error: Whether this line edit should display error.
        :return None:
        """
        self._logger.debug("running")
        if is_error:
            self._upper_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self._upper_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    @property
    def lower_isi(self) -> str:
        """

        :return str:
        """
        return self._lower_isi_line_edit.text()

    @lower_isi.setter
    def lower_isi(self, val: str) -> None:
        """
        Set display value of lower isi
        :param val: string value the display will be set to
        :return None:
        """
        self._logger.debug("running")
        self._lower_isi_line_edit.setText(str(val))
        self._logger.debug("done")

    def set_lower_isi_err(self, is_error: bool) -> None:
        """
        Set display of error in lower isi line edit
        :param is_error: Whether this line edit should display error.
        :return None:
        """
        self._logger.debug("running")
        if is_error:
            self._lower_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self._lower_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self._logger.debug("done")

    def set_upload_button(self, is_active) -> None:
        """

        :return:
        """
        self._logger.debug("running")
        self._upload_settings_button.setEnabled(is_active)
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

    def _set_texts(self):
        self._logger.debug("running")
        self._config_label.setText(self._strings[StringsEnum.CONFIG_LABEL])
        self._config_val.setText(self._strings[StringsEnum.ISO_LABEL])
        self._iso_button.setText(self._strings[StringsEnum.ISO_BUTTON_LABEL])
        self._stim_dur_label.setText(self._strings[StringsEnum.DURATION_LABEL])
        self._stim_intens_label.setText(self._strings[StringsEnum.INTENSITY_LABEL])
        self._upper_isi_label.setText(self._strings[StringsEnum.UPPER_ISI_LABEL])
        self._lower_isi_label.setText(self._strings[StringsEnum.LOWER_ISI_LABEL])
        self._upload_settings_button.setText(self._strings[StringsEnum.UPLOAD_BUTTON_LABEL])
        # self.config_button.setText(self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self.config_button.setText("...")
        # self._config_action.setText(self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._config_win.setWindowTitle(self.get_name() + " " + self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._logger.debug("done")

    def _set_tooltips(self):
        self._logger.debug("running")
        self._config_label.setToolTip(self._strings[StringsEnum.CONFIG_LABEL_TOOLTIP])
        self._iso_button.setToolTip(self._strings[StringsEnum.ISO_BUTTON_TOOLTIP])
        self._upper_isi_label.setToolTip(self._strings[StringsEnum.UPPER_ISI_TOOLTIP])
        self._lower_isi_label.setToolTip(self._strings[StringsEnum.LOWER_ISI_TOOLTIP])
        self._stim_dur_label.setToolTip(self._strings[StringsEnum.DURATION_TOOLTIP])
        self._stim_intens_label.setToolTip(self._strings[StringsEnum.INTENSITY_TOOLTIP])
        self._upload_settings_button.setToolTip(self._strings[StringsEnum.UPLOAD_BUTTON_TOOLTIP])
        self._stim_intens_slider.setToolTip(str(self._stim_intens_slider.value()) + "%")
        self.config_button.setToolTip(self._strings[StringsEnum.CONFIG_TAB_TOOLTIP])
        self._logger.debug("done")

    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     self._menu_bar.setMaximumWidth(self.width())
    #     return super().resizeEvent(event)
