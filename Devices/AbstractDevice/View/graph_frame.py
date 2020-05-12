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
from Devices.AbstractDevice.View.base_graph import BaseGraph
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from Model.app_helpers import ClickAnimationButton


class GraphFrame(QFrame):
    """ This code is to contain and properly size graph widgets. """
    def __init__(self, parent, graph: BaseGraph, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        super().__init__(parent)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout(self))
        self._visible = True
        self._graph = graph
        self._graph_height = 400
        self.layout().addWidget(self._graph)
        self.setFixedHeight(self._graph_height)
        self._logger.debug("Initialized")

    def set_graph_height(self, height: int = None):
        """ Each display type will be a different size. """
        self._logger.debug("running")
        if height is not None:
            self._graph_height = height
        self._logger.debug("done")

    def get_graph(self):
        return self._graph
