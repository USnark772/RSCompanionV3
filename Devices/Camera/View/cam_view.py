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
    QSizePolicy, QSpacerItem, QMenuBar, QAction, QGridLayout
from PySide2.QtGui import QPixmap, QMouseEvent, QResizeEvent
from PySide2.QtCore import Qt, QSize
from Devices.AbstractDevice.View.abstract_view import AbstractView
from Devices.AbstractDevice.View.ConfigPopUp import ConfigPopUp
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
        self._initialization_bar_frame.setMouseTracking(True)
        self._initialization_bar_frame.setMaximumHeight(70)
        self._initialization_bar_layout = QVBoxLayout(self._initialization_bar_frame)

        self._initialization_bar_label = QLabel(self._initialization_bar_frame)
        self._initialization_bar_label.setMouseTracking(True)
        self._initialization_bar = QProgressBar(self._initialization_bar_frame)
        self._initialization_bar.setMouseTracking(True)
        self._initialization_bar.setMaximumHeight(15)
        self._initialization_bar.setTextVisible(True)
        self._initialization_bar.setAlignment(Qt.AlignHCenter)

        self._initialization_bar_layout.addWidget(self._initialization_bar_label)
        self._initialization_bar_layout.addWidget(self._initialization_bar)

        self._cam_settings_frame = EasyFrame()
        self._cam_settings_layout = QGridLayout(self._cam_settings_frame)

        self._resolution_selector_label = QLabel(self._cam_settings_frame)
        self._resolution_selector_label.setAlignment(Qt.AlignLeft)

        self._resolution_selector = QComboBox(self._cam_settings_frame)
        self._resolution_selector.setMaximumHeight(22)

        self._cam_settings_layout.addWidget(self._resolution_selector_label, 0, 0)
        self._cam_settings_layout.addWidget(self._resolution_selector, 0, 1)

        self._fps_selector_label = QLabel(self._cam_settings_frame)
        self._fps_selector_label.setAlignment(Qt.AlignLeft)

        self._fps_selector = QComboBox(self._cam_settings_frame)
        self._fps_selector.setMaximumHeight(22)

        self._cam_settings_layout.addWidget(self._fps_selector_label, 1, 0)
        self._cam_settings_layout.addWidget(self._fps_selector, 1, 1)

        self._show_feed_checkbox_label = QLabel(self._cam_settings_frame)
        self._show_feed_checkbox_label.setAlignment(Qt.AlignLeft)

        self._show_feed_checkbox = QCheckBox()
        self._show_feed_checkbox.setChecked(True)
        self._show_feed_checkbox.setLayoutDirection(Qt.RightToLeft)

        self._cam_settings_layout.addWidget(self._show_feed_checkbox_label, 2, 0)
        self._cam_settings_layout.addWidget(self._show_feed_checkbox, 2, 1)

        self._use_cam_checkbox_label = QLabel(self._cam_settings_frame)
        self._use_cam_checkbox_label.setAlignment(Qt.AlignLeft)

        self._use_cam_checkbox = QCheckBox()
        self._use_cam_checkbox.setChecked(True)
        self._use_cam_checkbox.setLayoutDirection(Qt.RightToLeft)

        self._cam_settings_layout.addWidget(self._use_cam_checkbox_label, 3, 0)
        self._cam_settings_layout.addWidget(self._use_cam_checkbox, 3, 1)

        self._image_display_frame = EasyFrame()
        self._image_display_layout = QVBoxLayout(self._image_display_frame)

        self._image_display_label = QLabel(self._image_display_frame)
        self._image_display_label.setAlignment(Qt.AlignHCenter)
        self._image_display = QLabel(self._image_display_frame)
        self._image_display.setAlignment(Qt.AlignHCenter)
        self._image_display.setMouseTracking(True)
        self._image_display_layout.addWidget(self._image_display_label)
        self._image_display_layout.addWidget(self._image_display)

        spacer = QSpacerItem(1, 1, vData=QSizePolicy.Expanding)

        self._dev_sets_frame = EasyFrame()
        self._dev_sets_layout = QVBoxLayout(self._dev_sets_frame)

        self._menu_bar = QMenuBar()
        self._menu_bar.setMaximumWidth(self.width()-17)
        self._menu_bar.setMouseTracking(True)
        self._config_action = QAction()
        self._menu_bar.addAction(self._config_action)
        self._config_action.triggered.connect(self._config_button_handler)
        self.layout().setMenuBar(self._menu_bar)

        self._dev_sets_layout.addWidget(self._cam_settings_frame)
        self._dev_sets_layout.addItem(spacer)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._image_display)
        self.layout().addWidget(self._initialization_bar_frame)

        self._config_win = ConfigPopUp()
        self._config_win.setLayout(self._dev_sets_layout)
        self._config_win.setFixedSize(350, 130)

        self._aspect_ratio = 3/4
        self._window_changing = False
        self._showing_images = False
        self.resize(400, int(400 * self._aspect_ratio))
        self._strings = dict()
        self._lang_enum = LangEnum.ENG
        self.old_size = QSize(self.width(), self.height())
        self._logger.debug("Initialized")

    def set_show_feed_button_handler(self, func) -> None:
        """
        Add handler for show camera selector.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._show_feed_checkbox.toggled.connect(func)
        self._logger.debug("done")

    def set_resolution_selector_handler(self, func) -> None:
        """
        Add handler for resolution selector.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._resolution_selector.activated.connect(func)
        self._logger.debug("done")

    def set_fps_selector_handler(self, func) -> None:
        """
        Add handler for resolution selector.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._fps_selector.activated.connect(func)
        self._logger.debug("done")

    def set_frame_rotation_handler(self, func):
        self._logger.debug("running")
        # self._frame_rotation_setting_entry_box.textChanged.connect(func)
        self._logger.debug("done")

    def set_use_cam_button_handler(self, func) -> None:
        """
        Add handler for use camera selector.
        :param func: The handler.
        :return None:
        """
        self._logger.debug("running")
        self._use_cam_checkbox.toggled.connect(func)
        self._logger.debug("done")

    def _config_button_handler(self) -> None:
        """
        Show config pop up.
        :return None:
        """
        self._logger.debug("running")
        self._config_win.exec_()
        self._logger.debug("done")

    @property
    def language(self) -> LangEnum:
        """
        :return: The current lang enum being used.
        """
        return self._lang_enum

    @language.setter
    def language(self, lang: LangEnum) -> None:
        """
        Set the language for this view object.
        :param lang: The language to use.
        :return None:
        """
        self._logger.debug("running")
        self._lang_enum = lang
        self._strings = strings[lang]
        self._set_texts()
        self._set_tooltips()
        self._logger.debug("done")

    @property
    def resolution_list(self) -> list:
        """
        Get list of resolutions.
        :return list: The list of resolutions.
        """
        ret = list()
        return ret

    @resolution_list.setter
    def resolution_list(self, res_list: list) -> None:
        """
        Set list of resolutions available to res_list.
        :param res_list: The list of available resolutions.
        :return None:
        """
        self._logger.debug("running")
        self._resolution_selector.clear()
        for item in res_list:
            self._resolution_selector.addItem(str(item))
        self._logger.debug("done")

    @property
    def resolution(self) -> str:
        """
        Get the current resolution selection.
        :return str: The current resolution.
        """
        return self._resolution_selector.currentText()

    @resolution.setter
    def resolution(self, res: str) -> None:
        """
        Set the current resolution selection.
        :param res: The resolution to set to.
        :return None:
        """
        self._resolution_selector.setCurrentIndex(self._resolution_selector.findText(res))

    @property
    def fps_list(self) -> list:
        """
        Get list of fps options.
        :return list: The list of fps options.
        """
        ret = list()
        return ret

    @fps_list.setter
    def fps_list(self, fps_list: list) -> None:
        """
        Set list of available fps to fps_list.
        :param fps_list:
        :return None:
        """
        self._logger.debug("running")
        self._fps_selector.clear()
        for item in fps_list:
            self._fps_selector.addItem(str(item))
        self._logger.debug("done")

    @property
    def fps(self) -> str:
        """
        Get the current fps selection.
        :return str: The current fps selection.
        """
        return self._fps_selector.currentText()

    @fps.setter
    def fps(self, fps: str) -> None:
        """
        Set the current fps selection.
        :param fps: The fps to set to.
        :return None:
        """
        self._fps_selector.setCurrentIndex(self._fps_selector.findText(fps))

    @property
    def use_feed(self) -> bool:
        """
        Get the current use_cam setting.
        :return bool: User selection for using cam.
        """
        return self._show_feed_checkbox.isChecked()

    @use_feed.setter
    def use_feed(self, useable: bool) -> None:
        """
        Set use_cam setting.
        :param useable: The setting to set to.
        :return None:
        """
        self._logger.debug("running")
        self._show_feed_checkbox.setChecked(useable)
        self._logger.debug("Done")

    @property
    def use_cam(self) -> bool:
        """
        Get the current use_cam setting.
        :return bool: User selection for using cam.
        """
        return self._use_cam_checkbox.isChecked()

    @use_cam.setter
    def use_cam(self, useable: bool) -> None:
        """
        Set use_cam setting.
        :param useable: The setting to set to.
        :return None:
        """
        self._logger.debug("running")
        self._use_cam_checkbox.setChecked(useable)
        self._logger.debug("Done")

    # TODO: This could be much better.
    def resizeEvent(self, resizeEvent: QResizeEvent) -> None:
        if resizeEvent.size().width() != self.old_size.width():
            self.resize(self.width(), int(self.width() * self._aspect_ratio))
        elif resizeEvent.size().height() != self.old_size.height():
            self.resize(int(self.height() / self._aspect_ratio), self.height())
        self.old_size = resizeEvent.size()
        self._menu_bar.setMaximumWidth(self.width()-17)
        return super().resizeEvent(resizeEvent)

    def mousePressEvent(self, mouseEvent: QMouseEvent) -> None:
        """
        Detect when user is possibly resizing window.
        :param mouseEvent: The event to check.
        :return None:
        """
        self._logger.debug("running")
        super(CamView, self).mousePressEvent(mouseEvent)
        pos = mouseEvent.localPos()
        if 8 < pos.x() < self.width() - 8 and 48 < pos.y() < self.height() - 8:
            return
        self._window_changing = True
        self._image_display.hide()
        self._logger.debug("done")

    def mouseReleaseEvent(self, mouseEvent: QMouseEvent) -> None:
        """
        Detect when use releases mouse event to tell when user is possibly done resizing window.
        :param mouseEvent: The event to check.
        :return None:
        """
        self._logger.debug("running")
        super(CamView, self).mousePressEvent(mouseEvent)
        pos = mouseEvent.localPos()
        if 9 < pos.x() < self.width() - 9 and 49 < pos.y() < self.height() - 9:
            return
        self._window_changing = False
        if self._showing_images:
            self._image_display.show()
        self._logger.debug("done")

    def update_image(self, image: QPixmap = None, msg: str = None) -> None:
        """
        Update image viewer with new image.
        :param image: The new image to show.
        :param msg: The text to show if no image.
        :return None:
        """
        self._logger.debug("running")
        if not self._window_changing:
            if image is not None:
                h = image.height()
                w = image.width()
                self._aspect_ratio = h/w
                self._image_display.setPixmap(image.scaled(self.width(), self.width() * self._aspect_ratio))
            elif msg is not None:
                self._image_display.setText(msg)
        self._logger.debug("done")

    def show_images(self) -> None:
        """
        Show image display and hide initialization bar.
        :return None:
        """
        self._logger.debug("running")
        self._showing_images = True
        self._initialization_bar_frame.hide()
        self._image_display.show()
        self._logger.debug("done")

    def show_initialization(self) -> None:
        """
        Show initialization bar and hide image display.
        :return None:
        """
        self._logger.debug("running")
        self._showing_images = False
        self._image_display.hide()
        self._initialization_bar_frame.show()
        self._logger.debug("done")

    def update_init_bar(self, progress: int) -> None:
        """
        set progress bar value to progress.
        :param progress: The value to set progress bar to.
        :return None:
        """
        self._logger.debug("running")
        if progress > 100:
            progress = 100
        elif progress < 0:
            progress = 0
        self._initialization_bar.setValue(progress)
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
        self._show_feed_checkbox_label.setText(self._strings[StringsEnum.SHOW_FEED_CHECKBOX_LABEL])
        self._use_cam_checkbox_label.setText(self._strings[StringsEnum.USE_CAM_CHECKBOX_LABEL])
        self._resolution_selector_label.setText(self._strings[StringsEnum.RESOLUTION_SELECTOR_LABEL])
        self._fps_selector_label.setText(self._strings[StringsEnum.FPS_SELECTOR_LABEL])
        self._config_win.setWindowTitle(self.get_name() + " " + self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._config_action.setText(self._strings[StringsEnum.CONFIG_TAB_LABEL])
        self._logger.debug("done")

    def _set_tooltips(self) -> None:
        """
        Set the tooltips in this view object.
        :return None:
        """
        self._logger.debug("running")
        self._cam_settings_frame.setToolTip(self._strings[StringsEnum.FRAME_SIZE_TOOLTIP])
        self._image_display_frame.setToolTip(self._strings[StringsEnum.IMAGE_DISPLAY_TOOLTIP])
        self._logger.debug("done")
