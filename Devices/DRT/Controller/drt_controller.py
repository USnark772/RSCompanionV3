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
from aioserial import AioSerial
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Devices.AbstractDevice.View.graph_frame import GraphFrame
from Devices.DRT.View.drt_view import DRTView
from Devices.DRT.View.drt_graph import DRTGraph
from Devices.DRT.Model.drt_model import DRTModel
from Devices.DRT.Model import drt_defs as defs
from Devices.DRT.Resources.drt_strings import strings, StringsEnum, LangEnum


class Controller(AbstractController):
    def __init__(self, conn: AioSerial = AioSerial(), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        try:
            device_name = "DRT_" + conn.port.strip("COM")
        except:
            device_name = "DRT_NONE"
        view = DRTView(device_name, log_handlers)
        super().__init__(view)
        self._model = DRTModel(device_name, conn, log_handlers)
        self._graph = DRTGraph(view, log_handlers)
        self.view.add_graph(GraphFrame(view, self._graph, log_handlers))
        self._exp = False
        self._updating_config = False
        self._setup_handlers()
        self._init_values()
        self._msg_handler_task = create_task(self.msg_handler())
        self._strings = dict()
        self.set_lang(lang)
        self._logger.debug("Initialized")

    async def cleanup(self, discard: bool = False) -> None:
        """
        Cleanup this code for removal or app closure.
        :param discard: Quit without saving.
        :return: None.
        """
        self._logger.debug("running")
        if self._exp:
            self.stop_exp()
        self._msg_handler_task.cancel()
        self._model.cleanup()
        self.view.save_window_state()
        self._logger.debug("done")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this device's view language.
        :param lang: The enum for the language.
        :return: None.
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._model.set_lang(lang)
        # self.view.set_lang(lang)
        self.view.language = lang
        self._graph.set_lang(lang)
        self._logger.debug("done")

    def get_conn(self) -> AioSerial:
        """
        :return: The AioSerial connection passed in at creation.
        """
        return self._model.get_conn()

    async def msg_handler(self) -> None:
        """
        Handle messages sent from device.
        :return: None.
        """
        self._logger.debug("running")
        while True:
            msg, timestamp = await self._model.get_msg()
            msg_type = msg['type']
            if msg_type == "data":
                self._update_view_data(msg['values'], timestamp)
                self._model.save_data(msg['values'], timestamp)
            elif msg_type == "settings":
                self._update_view_config(msg['values'])

    def create_exp(self, path: str, cond_name: str) -> None:
        """
        Set this device's save dir.
        :param path: The save dir.
        :param cond_name: The optional condition name for this experiment.
        :return None:
        """
        self._logger.debug("running")
        self._graph.clear_graph()
        self._model.update_save_info(path)
        self._model.add_save_hdr()
        self._logger.debug("done")

    def start_exp(self, block_num: int) -> None:
        """
        Start this device.
        :param block_num: The block number for this exp block.
        :return: None.
        """
        self._logger.debug("running")
        self._model.send_start()
        self._graph.add_empty_point(datetime.now())
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
            self._model.send_stim_dur(self.view.stim_duration)
            changed = True
        if self._model.int_changed():
            self._model.send_stim_intensity(self.view.stim_intensity)
            changed = True
        if self._model.upper_changed():
            self._model.send_upper_isi(self.view.upper_isi)
            changed = True
        if self._model.lower_changed():
            self._model.send_lower_isi(self.view.lower_isi)
            changed = True
        if changed:
            self.view.config_text = self._strings[StringsEnum.CUSTOM_LABEL]
        self._model.reset_changed()
        self._check_for_upload()
        self._logger.debug("done")

    def _update_view_data(self, values: dict, timestamp: datetime) -> None:
        """
        Display data from device on view.
        :param values: The data to display.
        :param timestamp: When the data was received.
        :return: None.
        """
        self._logger.debug("running")
        data1 = [self._strings[StringsEnum.PLOT_NAME_RT], timestamp, values[defs.output_fields[3]]]
        data2 = [self._strings[StringsEnum.PLOT_NAME_CLICKS], timestamp, values[defs.output_fields[2]]]
        self._graph.add_data([data1, data2])
        self._logger.debug("done")

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
            self.view.stim_duration = val
            self.view.set_stim_dur_err(False)
        elif var == "intensity":
            self._model.set_current_vals(intensity=val)
            self.view.stim_intensity = self._model.calc_val_to_percent(val)
        elif var == "upperISI":
            self._model.set_current_vals(upper_isi=val)
            self.view.upper_isi = val
            self.view.set_upper_isi_err(False)
        elif var == "lowerISI":
            self._model.set_current_vals(lower_isi=val)
            self.view.lower_isi = val
            self.view.set_lower_isi_err(False)
        self._logger.debug("done")

    def _stim_dur_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in stim duration.
        :return: None.
        """
        self._logger.debug("running")
        if not self._updating_config:
            self.view.set_stim_dur_err(not self._model.check_stim_dur_entry(self.view.stim_duration))
            self._check_for_upload()
        self._logger.debug("done")

    def _stim_int_entry_changed_handler(self) -> None:
        """
        Handle when the user changes the value in stim intensity.
        :return: None.
        """
        self._logger.debug("running")
        if not self._updating_config:
            self._model.check_stim_int_entry(self.view.stim_intensity)
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
            upper = self.view.upper_isi
            lower = self.view.lower_isi
            err_upper = not self._model.check_upper_isi_entry(upper, lower)
            err_lower = not self._model.check_lower_isi_entry(upper, lower)
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
        self.view.set_upload_button(self._model.check_current_input())
        self._logger.debug("done")

    def _iso(self) -> None:
        """
        Set the values of the device to iso standard.
        :return: None.
        """
        self._logger.debug("running")
        self.view.config_text = self._strings[StringsEnum.ISO_LABEL]
        self._model.send_iso()
        self.view.set_upload_button(False)
        self._logger.debug("done")
