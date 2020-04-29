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
from datetime import datetime
from asyncio import create_task
from threading import Event
from aioserial import AioSerial
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Devices.DRT.View.drt_view import DRTView
from Devices.DRT.Model.drt_model import DRTModel
from Devices.DRT.Model import drt_strings as strings


class Controller(AbstractController):
    def __init__(self, conn: AioSerial, view_parent, ch: StreamHandler):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        device_name = "DRT_" + conn.port.strip("COM")
        super().__init__(DRTView(view_parent, device_name, ch))
        self._new_msg_e = Event()
        self._cleanup_e = Event()
        self._err_e = Event()
        self._model = DRTModel(conn, self._new_msg_e, self._cleanup_e, self._err_e, ch)
        self._exp = False
        self._updating_config = False
        self._setup_handlers()
        self._init_values()
        self._msg_handler_task = create_task(self.msg_handler())
        self._logger.debug("Initialized")

    def cleanup(self) -> None:
        """
        Cleanup this code for removal or app closure.
        :return: None.
        """
        self._logger.debug("running")
        if self._exp:
            self.stop_exp()
        self._msg_handler_task.cancel()
        self._model.cleanup()
        self._logger.debug("done")

    async def msg_handler(self) -> None:
        """
        Handle messages sent from device.
        :return: None.
        """
        while True:
            print(__name__, "Awaiting msg")
            msg, timestamp = await self._model.get_msg()
            print(__name__, "got msg")
            msg_type = msg['type']
            if msg_type == "data":
                self._update_view_data(msg['values'], timestamp)
                self._model.save_data(msg['values'], timestamp)
            elif msg_type == "settings":
                self._update_view_config(msg['values'])

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
        # button handlers
        self.view.set_iso_button_handler(self._iso)
        self.view.set_upload_button_handler(self._update_device)

        # value handlers
        self.view.set_stim_dur_entry_changed_handler(self._stim_dur_entry_changed_handler)
        self.view.set_stim_intens_entry_changed_handler(self._stim_int_entry_changed_handler)
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

    def _update_device(self) -> None:
        """
        If user input has changed, send updates.
        :return: None.
        """
        changed = False
        self._logger.debug("running")
        if self._model.dur_changed():
            self._model.send_stim_dur(self.view.get_stim_dur())
            changed = True
        if self._model.int_changed():
            self._model.send_stim_intensity(self.view.get_stim_intens())
            changed = True
        if self._model.upper_changed():
            self._model.send_upper_isi(self.view.get_upper_isi())
            changed = True
        if self._model.lower_changed():
            self._model.send_lower_isi(self.view.get_lower_isi())
            changed = True
        if changed:
            self.view.set_config_val(strings.custom_label)  # TODO: Fix this.
        self._model.reset_changed()
        self._logger.debug("done")

    def _update_view_data(self, values: dict, timestamp: datetime) -> None:
        """
        Display data from device on view.
        :param values: The data to display.
        :param timestamp: When the data was received.
        :return: None.
        """
        print("Implement drt_controller._update_view_data(). values, timestamp:", values, timestamp)

    def _update_view_config(self, msg: dict) -> None:
        """
        Send device config updates to the view.
        :param msg: The current device settings.
        :return: None.
        """
        self._logger.debug("running")
        self._updating_config = True
        for key in msg:
            self._set_view_val(key, msg[key])
        self._updating_config = False
        self._logger.debug("done")

    def _set_view_val(self, var: str, val: int) -> None:
        """
        Set the value for the config field in the view.
        :param var: The config field.
        :param val: The new value.
        :return: None.
        """
        self._logger.debug("running")
        if var == "stimDur":
            self._model.set_current_vals(duration=val)
            self.view.set_stim_dur(val)
            self.view.set_stim_dur_err(False)
        elif var == "intensity":
            self._model.set_current_vals(intensity=val)
            self.view.set_stim_intens(self._model.calc_val_to_percent(val))
        elif var == "upperISI":
            self._model.set_current_vals(upper_isi=val)
            self.view.set_upper_isi(val)
            self.view.set_upper_isi_err(False)
        elif var == "lowerISI":
            self._model.set_current_vals(lower_isi=val)
            self.view.set_lower_isi(val)
            self.view.set_lower_isi_err(False)
        self._logger.debug("done")

    def _stim_dur_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in stim duration.
        :return: None.
        """
        self._logger.debug("running")
        if not self._updating_config:
            self.view.set_stim_dur_err(self._model.check_stim_dur_entry(self.view.get_stim_dur()))
            self._check_for_upload()
        self._logger.debug("done")

    def _stim_int_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in stim intensity.
        :return: None.
        """
        self._logger.debug("running")
        if not self._updating_config:
            self._model.check_stim_int_entry(self.view.get_stim_intens())
            self.view.update_stim_intens_val_tooltip()
            self._check_for_upload()
        self._logger.debug("done")

    def _isi_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in upper or lower isi.
        :return: None.
        """
        self._logger.debug("running")
        if not self._updating_config:
            upper = self.view.get_upper_isi
            lower = self.view.get_lower_isi
            err_upper = self._model.check_upper_isi_entry(upper, lower)
            err_lower = self._model.check_lower_isi_entry(upper, lower)
            self.view.set_upper_isi_err(err_upper)
            self.view.set_lower_isi_err(err_lower)
            self._check_for_upload()
        self._logger.debug("done")

    def _check_for_upload(self) -> None:
        """
        Set view upload button depending on if upload is possible.
        :return: None.
        """
        self._logger.debug("running")
        if self._model.valid_entries():
            self.view.set_upload_button(True)
        else:
            self.view.set_upload_button(False)
        self._logger.debug("done")

    def _iso(self) -> None:
        """
        Set the values of the device to iso standard.
        :return: None.
        """
        self._logger.debug("running")
        self.view.set_config_val(strings.iso_label)
        self._model.send_stim_dur("1000")
        self._model.send_stim_intensity(100)
        self._model.send_upper_isi("5000")
        self._model.send_lower_isi("3000")
        self.view.set_upload_button(False)
        self._logger.debug("done")
