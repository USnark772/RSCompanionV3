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


import logging
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QLabel
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QSize, Qt
from Model.app_helpers import ClickAnimationButton
from Model.app_defs import button_box_start_image_filepath, button_box_pause_image_filepath
from Model.app_strings import button_box_create, button_box_create_tooltip, button_box_text_entry_placeholder, \
    button_box_title, button_box_prog_bar_label, button_box_start_tooltip, button_box_resume_tooltip, \
    button_box_end_tooltip, button_box_end, button_box_pause_tooltip


class ButtonBox(QGroupBox):
    """ This code is to contain the overall controls which govern running experiments. """
    def __init__(self, parent, size, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
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

        self._play_icon = QIcon()
        self._play_icon.addPixmap(QPixmap(button_box_start_image_filepath))
        self._pause_icon = QIcon()
        self._pause_icon.addPixmap(QPixmap(button_box_pause_image_filepath))
        self._playing = False

        self.prog_bar_label = QLabel()
        self.prog_bar = QProgressBar()
        self.prog_bar.setTextVisible(True)
        self.prog_bar.setAlignment(Qt.AlignHCenter)
        self.prog_bar.setMaximumHeight(12)
        self.layout().addWidget(self.prog_bar_label)
        self.layout().addWidget(self.prog_bar)

        self._set_texts()
        self.toggle_show_prog_bar(False)
        self._set_button_states()
        self._set_tooltips()
        self.logger.debug("Initialized")

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

    def toggle_condition_name_box(self) -> None:
        """
        Toggle whether the text entry is usable.
        :return: None
        """
        self.logger.debug("running")
        self._text_entry.setEnabled(not self._text_entry.isEnabled())
        self.logger.debug("done")

    def toggle_create_button(self) -> None:
        """
        Set create button to either create or end depending on what state any current experiment is in.
        :return: None.
        """
        self.logger.debug("running")
        state = self._create_button.text()
        if state == button_box_create:
            self._create_button.setText(button_box_end)
            self._create_button.setToolTip(button_box_end_tooltip)
            self._start_button.setEnabled(True)
        else:
            self._create_button.setText(button_box_create)
            self._create_button.setToolTip(button_box_create_tooltip)
            self._start_button.setToolTip(button_box_start_tooltip)
            self._start_button.setEnabled(False)
        self.logger.debug("done")

    def toggle_start_button(self) -> None:
        """
        Set start button state depending on if there is an experiment created and running or not.
        :return: None.
        """
        self.logger.debug("running")
        if self._playing:
            self._playing = False
            self._start_button.setIcon(self._play_icon)
            self._start_button.setIconSize(QSize(26, 26))
            self._create_button.setEnabled(True)
            self._start_button.setToolTip(button_box_resume_tooltip)
        else:
            self._playing = True
            self._start_button.setIcon(self._pause_icon)
            self._start_button.setIconSize(QSize(36, 36))
            self._create_button.setEnabled(False)
            self._start_button.setToolTip(button_box_pause_tooltip)
        self.logger.debug("done")

    def toggle_show_prog_bar(self, is_visible: bool) -> None:
        """
        Toggle showing the progress bar.
        :param is_visible: Whether or not to show the progress bar.
        :return: None.
        """
        if is_visible:
            self.prog_bar.show()
            self.prog_bar_label.show()
        else:
            self.prog_bar.hide()
            self.prog_bar_label.hide()

    def update_prog_bar_value(self, value: int) -> None:
        """
        Update the progress bar to the given value
        :param value: The value to use when updating the progress bar.
        :return: None.
        """
        self.prog_bar.setValue(value)

    def _set_texts(self) -> None:
        """
        Set the texts of this view item.
        :return: None.
        """
        self.logger.debug("running")
        self.setTitle(button_box_title)
        self._text_entry.setPlaceholderText(button_box_text_entry_placeholder)
        self._create_button.setText(button_box_create)
        self._start_button.setIcon(self._play_icon)
        self._start_button.setIconSize(QSize(32, 32))
        self.prog_bar_label.setText(button_box_prog_bar_label)
        self.prog_bar.setValue(0)
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
        self._create_button.setToolTip(button_box_create_tooltip)
        self._start_button.setToolTip(button_box_start_tooltip)
        self.logger.debug("done")
