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
        self._model = DRTModel(port, save_dir, self._new_msg_e, self._cleanup_e, self._err_e, ch)
        super().__init__(DRTView(self._device_name))
        self._exp = False
        self._updating_config = False  # TODO: Finish using this.
        self._logger.debug("Initialized")

    def cleanup(self) -> None:
        self._logger.debug("running")
        if self._exp:
            self.stop_exp()
        self._model.cleanup()
        self._logger.debug("done")

    async def msg_handler(self) -> None:
        """
        Handle messages sent from device.
        :return: None.
        """
        while True:
            await self._new_msg_e.wait()
            ret, (msg, timestamp) = self._model.get_msg()
            if ret:
                msg_type = msg['type']
                if msg_type == "data":
                    # self._display_data(msg['values'], timestamp)
                    self._model.save_data(msg['values'], timestamp)
                elif msg_type == "settings":
                    self._update_config(msg['values'])

    def start_exp(self) -> None:
        """
        Start this device.
        :return: None.
        """
        self._logger.debug("running")
        self._model.send_start()
        self._logger.debug("done")

    def stop_exp(self) -> None:
        """
        Stop this device.
        :return: None.
        """
        self._logger.debug("running")
        self._model.send_stop()
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        """
        Attach handlers to view.
        :return: None.
        """
        self._logger.debug("running")
        self.view.set_stim_dur_entry_changed_handler(self._stim_dur_entry_changed_handler)
        self.view.set_stim_int_entry_changed_handler(self._stim_int_entry_changed_handler)
        self.view.set_upper_isi_entry_changed_handler(self._isi_entry_changed_handler)
        self.view.set_lower_isi_entry_changed_handler(self._isi_entry_changed_handler)
        self._logger.debug("done")

    def _init_values(self):
        """
        Send for device config.
        :return: None.
        """
        self._logger.debug("running")
        self._model.query_config()
        self._logger.debug("done")

    def _update_config(self, msg: dict) -> None:
        self._logger.debug("running")
        self._updating_config = True
        for key in msg:
            self._set_val(key, msg[key])
        self._updating_config = False
        self._logger.debug("done")

    def _set_val(self, var: str, val: int) -> None:
        self._logger.debug("running")
        if var == "stimDur":
            self._model.set_current_vals(duration=val)
            self.view.set_stim_dur_val(val)
            self.view.set_stim_dur_err(False)
        elif var == "intensity":
            self._model.set_current_vals(intensity=val)
            self.view.set_stim_intens_val(self._model.calc_val_to_percent(val))
        elif var == "upperISI":
            self._model.set_current_vals(upper_isi=val)
            self.view.set_upper_isi_val(val)
            self.view.set_upper_isi_err(False)
        elif var == "lowerISI":
            self._model.set_current_vals(lower_isi=val)
            self.view.set_lower_isi_val(val)
            self.view.set_lower_isi_err(False)
        self._logger.debug("done")

    def _stim_dur_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in stim duration.
        :return: None.
        """
        self._logger.debug("running")
        self.view.set_stim_dur_err(self._model.check_stim_dur_entry(self.view.get_stim_dur()))
        self._logger.debug("done")

    def _stim_int_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in stim intensity.
        :return: None.
        """
        self._logger.debug("running")
        self.view.set_stim_int_err(self._model.check_stim_int_entry(self.view.get_stim_int()))
        self._logger.debug("done")

    def _isi_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in upper or lower isi.
        :return: None.
        """
        self._logger.debug("running")
        upper = self.view.get_upper_isi
        lower = self.view.get_lower_isi
        err_upper = self._model.check_upper_isi_entry(upper, lower)
        err_lower = self._model.check_lower_isi_entry(upper, lower)
        self.view.set_upper_isi_err(err_upper)
        self.view.set_lower_isi_err(err_lower)
        self._logger.debug("done")
