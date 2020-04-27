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
from PySide2.QtWidgets import QGroupBox, QGridLayout, QTextEdit
from Model.app_helpers import ClickAnimationButton


class NoteBox(QGroupBox):
    """ This code is for the user to input notes as desired. """
    def __init__(self, parent, size, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self.setMaximumSize(size)
        self._text_edit = QTextEdit()
        self.layout().addWidget(self._text_edit, 0, 1, 1, 1)
        self._post_button = ClickAnimationButton()
        self.layout().addWidget(self._post_button, 1, 1, 1, 1)

        self._set_texts()
        self._set_button_state()
        self._set_tooltips()
        self.logger.debug("Initialized")

    def get_note(self):
        return self._text_edit.toPlainText()

    def clear_note(self):
        self.logger.debug("running")
        self._text_edit.clear()
        self.logger.debug("done")

    def toggle_post_button(self, is_active):
        self.logger.debug("running")
        self._post_button.setEnabled(is_active)
        self.logger.debug("done")

    def add_post_handler(self, func):
        self.logger.debug("running")
        self._post_button.clicked.connect(func)
        self.logger.debug("done")

    def add_note_box_changed_handler(self, func):
        self.logger.debug("running")
        self._text_edit.textChanged.connect(func)
        self.logger.debug("done")

    def _set_texts(self):
        self.logger.debug("running")
        self.setTitle("Note")
        self._post_button.setText("Post")
        self._text_edit.setPlaceholderText("Enter note here")
        self.logger.debug("done")

    def _set_button_state(self):
        self.logger.debug("running")
        self._post_button.setEnabled(False)
        self.logger.debug("done")

    def _set_tooltips(self):
        self.logger.debug("running")
        self._post_button.setToolTip("Post note")
        self.logger.debug("done")
