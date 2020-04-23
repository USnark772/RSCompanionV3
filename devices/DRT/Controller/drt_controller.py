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
from asyncio import Event
from aioserial import AioSerial
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Devices.DRT.View.drt_view import DRTView
from Devices.DRT.Model.drt_model import DRTModel


class DRTController(AbstractController):
    def __init__(self, d_name: str, port: AioSerial, save_dir: str, ch: StreamHandler):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        self._device_name = d_name
        self._new_msg_e = Event()
        self._cleanup_e = Event()
        self._err_e = Event()
        self._model = DRTModel(port, save_dir, ch)
        super().__init__(DRTView(self._device_name))
        self._exp = False
        self._logger.debug("Initialized")

    def cleanup(self):
        self._logger.debug("running")
        if self._exp:
            self.stop_exp()
        self._logger.debug("done")

    def start_exp(self):
        self._logger.debug("running")
        # TODO: Send message to device
        self._logger.debug("done")

    def stop_exp(self):
        self._logger.debug("running")
        # TODO: Send message to device
        self._logger.debug("done")

    def _stim_dur_entry_changed_handler(self):
        self._logger.debug("running")
        self._logger.debug("done")

    def _stim_int_entry_changed_handler(self):
        self._logger.debug("running")
        self._logger.debug("done")

    def _upper_isi_entry_changed_handler(self):
        self._logger.debug("running")
        self._logger.debug("done")

    def _lower_isi_entry_changed_handler(self):
        self._logger.debug("running")
        self._logger.debug("done")

