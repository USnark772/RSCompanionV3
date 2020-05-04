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
Date: 2019
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""


from logging import getLogger, StreamHandler
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QLabel
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize
from Model.app_helpers import ClickAnimationButton
from Model.app_defs import button_box_start_image_filepath, button_box_pause_image_filepath
from Resources.Strings.button_box_strings import strings, StringsEnum, LangEnum


class ButtonBox(QGroupBox):
    """ This code is to contain the overall controls which govern running experiments. """
    def __init__(self, parent, size: QSize, log_handlers: [StreamHandler], lang: LangEnum):
        self.logger = getLogger(__name__)
        for h in log_handlers:
            self.logger.addHandler(h)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setMaximumSize(size)
        self._button_layout = QHBoxLayout()

        self._create_button = ClickAnimationButton()
        self._create_button.setFixedSize(60, 40)
        self._start_button = ClickAnimationButton()
        self._start_button.setFixedSize(120, 40)
        self._button_layout.addWidget(self._create_button)
        self._button_layout.addWidget(self._start_button)
        self._text_entry = QLineEdit()
        self.layout().addLayout(self._button_layout)
        self.layout().addWidget(self._text_entry)

        self._play_icon = QIcon(button_box_start_image_filepath)
        self._pause_icon = QIcon(button_box_pause_image_filepath)

        # self.prog_bar_label = QLabel()
        # self.prog_bar = QProgressBar()
        # self.prog_bar.setTextVisible(True)
        # self.prog_bar.setAlignment(Qt.AlignHCenter)
        # self.prog_bar.setMaximumHeight(12)
        # self.layout().addWidget(self.prog_bar_label)
        # self.layout().addWidget(self.prog_bar)

        self._start_button_state = 0
        self._create_button_state = 0
        self._set_button_states()
        self._strings = dict()
        self.set_lang(lang)
        # self.toggle_show_prog_bar(False)
        self.logger.debug("Initialized")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The enum for the language.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()
        self._set_tooltips()

    def get_condition_name(self) -> str:
        """
        Return the text from the condition name text entry
        :return: The text from the text entry.
        """
        return self._text_entry.text()

    def add_create_button_handler(self, func: classmethod) -> None:
        """
        Add handler for the create button click event.
        :param func: The handler.
        :return: None.
        """
        self.logger.debug("running")
        self._create_button.clicked.connect(func)
        self.logger.debug("done")

    def add_start_button_handler(self, func: classmethod) -> None:
        """
        Add handler for the start button click event.
        :param func: The handler
        :return: None.
        """
        self.logger.debug("running")
        self._start_button.clicked.connect(func)
        self.logger.debug("done")

    def set_condition_name_box_enabled(self, is_active: bool) -> None:
        """
        Set whether this text entry is enabled.
        :param is_active: Whether this button is active.
        :return: None
        """
        self.logger.debug("running")
        self._text_entry.setEnabled(is_active)
        self.logger.debug("done")

    def set_create_button_enabled(self, is_active: bool) -> None:
        """
        Toggle whether this button is active.
        :param is_active: Whether this button is active.
        :return None:
        """
        self._create_button.setEnabled(is_active)

    def set_create_button_state(self, button_state: int) -> None:
        """
        Set create button state to given state. 0: Create. 1: End.
        :param button_state: The state to show on this button.
        :return: None.
        """
        self.logger.debug("running")
        if button_state == 0:
            self._create_button.setText(self._strings[StringsEnum.CREATE])
            self._create_button.setToolTip(self._strings[StringsEnum.CREATE_TT])
        elif button_state == 1:
            self._create_button.setText(self._strings[StringsEnum.END])
            self._create_button.setToolTip(self._strings[StringsEnum.END_TT])
        self.logger.debug("done")

    def set_start_button_enabled(self, is_active: bool) -> None:
        """
        Toggle whether this button is active.
        :param is_active: Whether this button is active.
        :return None:
        """
        self._start_button.setEnabled(is_active)

    def set_start_button_state(self, button_state: int = 0) -> None:
        """
        Set start button state to given state. 0: Start. 1: Pause. 2: Resume.
        :param button_state: The state to show on this button.
        :return: None.
        """
        self.logger.debug("running")
        if button_state == 0:
            self._start_button.setIcon(self._play_icon)
            self._start_button.setIconSize(QSize(26, 26))
            self._start_button.setToolTip(self._strings[StringsEnum.START_TT])
        elif button_state == 1:
            self._start_button.setIcon(self._pause_icon)
            self._start_button.setIconSize(QSize(36, 36))
            self._start_button.setToolTip(self._strings[StringsEnum.PAUSE_TT])
        elif button_state == 2:
            self._start_button.setIcon(self._play_icon)
            self._start_button.setIconSize(QSize(26, 26))
            self._start_button.setToolTip(self._strings[StringsEnum.RESUME_TT])
        self.logger.debug("done")

    def toggle_show_prog_bar(self, is_visible: bool) -> None:
        """
        Toggle showing the progress bar.
        :param is_visible: Whether or not to show the progress bar.
        :return: None.
        """
        pass
        # if is_visible:
        #     self.prog_bar.show()
        #     self.prog_bar_label.show()
        # else:
        #     self.prog_bar.hide()
        #     self.prog_bar_label.hide()

    def update_prog_bar_value(self, value: int) -> None:
        """
        Update the progress bar to the given value
        :param value: The value to use when updating the progress bar.
        :return: None.
        """
        pass
        # self.prog_bar.setValue(value)

    def _set_texts(self) -> None:
        """
        Set the texts of this view item.
        :return: None.
        """
        self.logger.debug("running")
        self.setTitle(self._strings[StringsEnum.TITLE])
        self._text_entry.setPlaceholderText(self._strings[StringsEnum.COND_NAME_SHADOW])
        if self._create_button_state == 0:
            self._create_button.setText(self._strings[StringsEnum.CREATE])
        elif self._create_button_state == 1:
            self._create_button.setText(self._strings[StringsEnum.END])
        if self._start_button_state == 0 or self._start_button_state == 2:
            self._start_button.setIcon(self._play_icon)
            self._start_button.setIconSize(QSize(32, 32))
        elif self._start_button_state == 1:
            self._start_button.setIcon(self._pause_icon)
            self._start_button.setIconSize(QSize(36, 36))
        # self.prog_bar_label.setText(button_box_prog_bar_label)
        # self.prog_bar.setValue(0)
        self.logger.debug("done")

    def _set_button_states(self) -> None:
        """
        Set default button states.
        :return: None.
        """
        self.logger.debug("running")
        self._start_button.setEnabled(False)
        self.logger.debug("done")

    def _set_tooltips(self) -> None:
        """
        Set the text for the tooltips in this view item.
        :return: None.
        """
        self.logger.debug("running")
        if self._create_button_state == 0:
            self._create_button.setToolTip(self._strings[StringsEnum.CREATE_TT])
        if self._create_button_state == 1:
            self._create_button.setToolTip(self._strings[StringsEnum.END_TT])
        if self._start_button_state == 0:
            self._start_button.setToolTip(self._strings[StringsEnum.START_TT])
        elif self._start_button_state == 1:
            self._start_button.setToolTip(self._strings[StringsEnum.PAUSE_TT])
        elif self._start_button_state == 2:
            self._start_button.setToolTip(self._strings[StringsEnum.RESUME_TT])
        self.logger.debug("done")
