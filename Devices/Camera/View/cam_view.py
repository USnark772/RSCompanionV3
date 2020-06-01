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
from PySide2.QtWidgets import QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QCheckBox, QComboBox, QLineEdit,\
    QSizePolicy, QSpacerItem
from PySide2.QtGui import QPixmap, QMouseEvent, QResizeEvent
from PySide2.QtCore import Qt, QSize
from Devices.AbstractDevice.View.abstract_view import AbstractView
from Devices.Camera.Resources.cam_strings import strings, StringsEnum, LangEnum
from Model.app_helpers import EasyFrame


class CamView(AbstractView):
    def __init__(self, name: str = "CAM_NONE", log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(name, empty=True)

        self._initialization_bar_frame = EasyFrame()
        self._initialization_bar_frame.setMaximumHeight(70)
        self._initialization_bar_layout = QVBoxLayout(self._initialization_bar_frame)

        self._initialization_bar_label = QLabel(self._initialization_bar_frame)
        self._initialization_bar = QProgressBar(self._initialization_bar_frame)
        self._initialization_bar.setMaximumHeight(15)
        self._initialization_bar.setTextVisible(True)
        self._initialization_bar.setAlignment(Qt.AlignHCenter)

        self._initialization_bar_layout.addWidget(self._initialization_bar_label)
        self._initialization_bar_layout.addWidget(self._initialization_bar)

        self._show_cam_checkbox_frame = EasyFrame()
        self._show_cam_checkbox_frame.setMaximumHeight(50)
        self._show_cam_checkbox_layout = QHBoxLayout(self._show_cam_checkbox_frame)

        self._show_cam_checkbox_label = QLabel(self._show_cam_checkbox_frame)
        self._show_cam_checkbox_label.setAlignment(Qt.AlignLeft)

        self._show_cam_checkbox = QCheckBox()
        self._show_cam_checkbox.setChecked(True)
        self._show_cam_checkbox.setLayoutDirection(Qt.RightToLeft)

        self._show_cam_checkbox_layout.addWidget(self._show_cam_checkbox_label)
        self._show_cam_checkbox_layout.addWidget(EasyFrame(vert=True))
        self._show_cam_checkbox_layout.addWidget(self._show_cam_checkbox)

        self._frame_size_selector_frame = EasyFrame()
        self._frame_size_selector_layout = QHBoxLayout(self._frame_size_selector_frame)
        self._frame_size_selector_frame.setMaximumHeight(50)

        self._frame_size_selector_label = QLabel(self._frame_size_selector_frame)
        self._frame_size_selector_label.setAlignment(Qt.AlignLeft)

        self._frame_size_selector = QComboBox(self._frame_size_selector_frame)
        self._frame_size_selector.setMaximumHeight(22)

        self._frame_size_selector_layout.addWidget(self._frame_size_selector_label)
        self._frame_size_selector_layout.addWidget(EasyFrame(vert=True))
        self._frame_size_selector_layout.addWidget(self._frame_size_selector)

        self._frame_rotation_setting_frame = EasyFrame()
        self._frame_rotation_setting_frame.setMaximumHeight(50)
        self._frame_rotation_setting_layout = QHBoxLayout(self._frame_rotation_setting_frame)

        self._frame_rotation_setting_label = QLabel(self._frame_rotation_setting_frame)
        self._frame_rotation_setting_label.setAlignment(Qt.AlignLeft)

        self._frame_rotation_setting_entry_box = QLineEdit(self._frame_rotation_setting_frame)
        self._frame_rotation_setting_entry_box.setMaximumSize(90, 20)
        self._frame_rotation_setting_entry_box.setAlignment(Qt.AlignRight)

        self._frame_rotation_setting_layout.addWidget(self._frame_rotation_setting_label)
        self._frame_rotation_setting_layout.addWidget(EasyFrame(vert=True))
        self._frame_rotation_setting_layout.addWidget(self._frame_rotation_setting_entry_box)

        self._image_display_frame = EasyFrame()
        self._image_display_layout = QVBoxLayout(self._image_display_frame)

        self._image_display_label = QLabel(self._image_display_frame)
        self._image_display_label.setAlignment(Qt.AlignHCenter)
        self._image_display = QLabel(self._image_display_frame)
        self._image_display.setAlignment(Qt.AlignHCenter)

        self._image_display_layout.addWidget(self._image_display_label)
        self._image_display_layout.addWidget(self._image_display)

        self._fps_display_frame = EasyFrame()
        self._fps_display_layout = QHBoxLayout(self._fps_display_frame)

        self._fps_display_label = QLabel(self._fps_display_frame)
        self._fps_display_label.setAlignment(Qt.AlignRight)

        self._fps_display_value = QLabel(self._fps_display_frame)
        self._fps_display_value.setAlignment(Qt.AlignLeft)

        self._fps_display_layout.addWidget(self._fps_display_label)
        self._fps_display_layout.addWidget(self._fps_display_value)

        spacer = QSpacerItem(1, 1, vData=QSizePolicy.Expanding)

        self._dev_sets_frame = EasyFrame()
        self._dev_sets_layout = QVBoxLayout(self._dev_sets_frame)

        self._dev_sets_layout.addWidget(self._initialization_bar_frame)
        self._dev_sets_layout.addWidget(EasyFrame(line=True))
        self._dev_sets_layout.addWidget(self._frame_size_selector_frame)
        self._dev_sets_layout.addWidget(self._frame_rotation_setting_frame)
        self._dev_sets_layout.addWidget(EasyFrame(line=True))
        self._dev_sets_layout.addWidget(self._show_cam_checkbox_frame)
        self._dev_sets_layout.addWidget(self._fps_display_frame)
        self._dev_sets_layout.addWidget(EasyFrame(line=True))
        self._dev_sets_layout.addItem(spacer)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._image_display)

        self._aspect_ratio = 3/4
        self._window_changing = False
        self.resize(400, int(400 * self._aspect_ratio))
        self._strings = dict()
        self.old_size = QSize(self.width(), self.height())
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

    def set_show_cam_button_handler(self, func):
        self._logger.debug("running")
        self._show_cam_checkbox.toggled.connect(func)
        self._logger.debug("done")

    def set_frame_size_selector_handler(self, func):
        self._logger.debug("running")
        self._frame_size_selector.activated.connect(func)
        self._logger.debug("done")

    def set_frame_rotation_handler(self, func):
        self._logger.debug("running")
        self._frame_rotation_setting_entry_box.textChanged.connect(func)
        self._logger.debug("done")

    # TODO: Fix this scaling ratio.
    def update_image(self, image: QPixmap) -> None:
        """
        Update image viewer with new image.
        :param image: The new image to show.
        :return None:
        """
        self._logger.debug("running")
        if not self._window_changing:
            h = image.height()
            w = image.width()
            self._aspect_ratio = h/w
            self._image_display.setPixmap(image.scaled(self.width(), self.width() * self._aspect_ratio))
        self._logger.debug("done")

    def resizeEvent(self, resizeEvent: QResizeEvent) -> None:
        if resizeEvent.size().width() != self.old_size.width():
            self.resize(self.width(), int(self.width() * self._aspect_ratio))
        elif resizeEvent.size().height() != self.old_size.height():
            self.resize(int(self.height() / self._aspect_ratio), self.height())
        self.old_size = resizeEvent.size()
        return super().resizeEvent(resizeEvent)

    def mousePressEvent(self, mouseEvent: QMouseEvent) -> None:
        """
        Detect when user is possibly resizing window.
        :param mouseEvent: The event to check.
        :return None:
        """
        self._logger.debug("running")
        self._window_changing = True
        super(CamView, self).mousePressEvent(mouseEvent)
        self._image_display.hide()
        self._logger.debug("done")

    def mouseReleaseEvent(self, mouseEvent: QMouseEvent) -> None:
        """
        Detect when use releases mouse event to tell when user is possibly done resizing window.
        :param mouseEvent: The event to check.
        :return None:
        """
        self._logger.debug("running")
        self._window_changing = False
        super(CamView, self).mousePressEvent(mouseEvent)
        self._image_display.show()
        self._logger.debug("done")

    def _set_texts(self) -> None:
        """
        Set the texts in this view object.
        :return None:
        """
        self._logger.debug("running")
        self._initialization_bar_label.setText(self._strings[StringsEnum.INITIALIZATION_BAR_LABEL])
        self._initialization_bar.setValue(0)
        self._image_display_label.setText(self._strings[StringsEnum.IMAGE_DISPLAY_LABEL])
        self._image_display.setText(self._strings[StringsEnum.IMAGE_DISPLAY])
        self._show_cam_checkbox_label.setText(self._strings[StringsEnum.SHOW_CAM_CHECKBOX_LABEL])
        self._frame_size_selector_label.setText(self._strings[StringsEnum.FRAME_SIZE_SELECTOR_LABEL])
        self._frame_rotation_setting_label.setText(self._strings[StringsEnum.FRAME_ROTATION_SETTING_LABEL])
        self._fps_display_label.setText(self._strings[StringsEnum.FPS_DISPLAY_LABEL])
        self._fps_display_value.setText(self._strings[StringsEnum.FPS_DISPLAY_VALUE])
        self._logger.debug("done")

    def _set_tooltips(self) -> None:
        """
        Set the tooltips in this view object.
        :return None:
        """
        self._logger.debug("running")
        self._show_cam_checkbox_frame.setToolTip(self._strings[StringsEnum.SHOW_CAM_TOOLTIP])
        self._frame_size_selector_frame.setToolTip(self._strings[StringsEnum.FRAME_SIZE_TOOLTIP])
        self._frame_rotation_setting_frame.setToolTip(self._strings[StringsEnum.ROTATION_TOOLTIP])
        self._image_display_frame.setToolTip(self._strings[StringsEnum.IMAGE_DISPLAY_TOOLTIP])
        self._fps_display_frame.setToolTip(self._strings[StringsEnum.FPS_DISPLAY_TOOLTIP])
        self._logger.debug("done")
