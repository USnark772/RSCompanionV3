from PySide2.QtWidgets import QMdiSubWindow, QLabel
from PySide2.QtGui import QColor, QPixmap, QIcon, QImage
from PySide2 import QtCore
from PySide2.QtCore import QTimer
import time
import numpy as np


class MDIWidget(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.w = 640
        self.h_scale = .75
        self.win_frame_offset = 25
        self.mdi_w = self.w
        self.mdi_h = int(self.w * self.h_scale) + self.win_frame_offset

        self.image_w = int(self.w)
        self.image_h = int(self.w * self.h_scale)

        self.image_active = None

        self.resize(self.mdi_w, self.mdi_h)
        self.mid_text = QLabel("Nothing yet...", alignment=QtCore.Qt.AlignCenter)
        self.setWidget(self.mid_text)
        self.setWindowTitle("Video")
        self.setWindowIcon(self.create_icon_by_color(QColor("transparent")))


    def display(self, image):
        image8 = image.astype(np.uint8)
        height, width, colors = image8.shape

        image = QImage(image8.data, width, height, 3 * width,
                       QImage.Format_RGB888)

        self.image_active = QPixmap.fromImage(image.rgbSwapped())
        self.rescale_active_image()

    def rescale_active_image(self):
        if self.image_active is not None:
            self.image_active = self.image_active.scaled(self.image_w, self.image_h)
            self.mid_text.setPixmap(self.image_active)

    def mousePressEvent(self, mousePressEvent):
        self.mid_text.hide()
        return super().mousePressEvent(mousePressEvent)

    def mouseReleaseEvent(self, mouseReleaseEvent):
        self.image_h = int(self.width() * self.h_scale)
        self.image_w = int(self.width())
        self.rescale_active_image()
        self.mid_text.show()
        return super().mouseReleaseEvent(mouseReleaseEvent)

    def resizeEvent(self, resizeEvent):
        self.resize(self.width(), int(self.width() * self.h_scale) + self.win_frame_offset)
        return super().resizeEvent(resizeEvent)

    def create_icon_by_color(self, color):
        pixmap = QPixmap(512, 512)
        pixmap.fill(color)
        return QIcon(pixmap)
