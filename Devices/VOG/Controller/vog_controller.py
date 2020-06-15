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
Author: Nathan Rogers
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
from Devices.VOG.View.vog_view import VOGView
from Devices.VOG.View.vog_graph import VOGGraph
from Devices.VOG.Model.vog_model import VOGModel
from Devices.VOG.Model import vog_defs as defs
from Devices.VOG.Resources.vog_strings import strings, StringsEnum, LangEnum


class Controller(AbstractController):
    def __init__(self, conn: AioSerial = AioSerial(), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        try:
            device_name = "VOG_" + conn.port.strip("COM")
        except:
            device_name = "VOG_NONE"
        view = VOGView(device_name, log_handlers)
        super().__init__(view)
        self._model = VOGModel(device_name, conn, log_handlers)
        self._graph = VOGGraph(view, log_handlers)
        self.view.add_graph(GraphFrame(view, self._graph, log_handlers))
        self._exp_created = False
        self._exp_running = False
        self._updating_config = False
        self._prev_vals = ["0", "0"]  # open_dur, close_dur
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
        if self._exp_running:
            self.stop_exp()
        if self._exp_created:
            self.end_exp()
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
            if 'type' in msg.keys():
                msg_type = msg['type']
                if msg_type == "data":
                    self._update_view_data(msg['values'], timestamp)
                    self._model.save_data(msg['values'], timestamp)
                elif msg_type == "settings":
                    self._update_view_config(msg['values'])
                elif msg_type == "action":
                    pass  # TODO: handle action message?

    def create_exp(self, path: str, cond_name: str) -> None:
        """
        Set this device's save dir.
        :param path: The save dir.
        :param cond_name: The condition name for this experiment.
        :return None:
        """
        self._logger.debug("running")
        self._graph.clear_graph()
        self._model.update_save_info(path)
        self._model.add_save_hdr()
        self._model.send_create()
        self._logger.debug("done")

    def end_exp(self) -> None:
        """
        Notify this device of experiment end
        :return None:
        """
        self._logger.debug("running")
        self._model.send_end()
        self._logger.debug("done")

    def start_exp(self, block_num: int) -> None:
        """
        Notify this device of experiment start.
        :param block_num: The block number for this exp block.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_start()
        self._logger.debug("done")

    def stop_exp(self) -> None:
        """
        Notify this device of experiment stop.
        :return: None.
        """
        self._logger.debug("running")
        self._model.send_stop()
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        self._logger.debug("running")
        self.view.set_config_val_line_edit_handler(self._config_name_handler)
        self.view.set_nhtsa_button_handler(self._nhtsa_handler)
        self.view.set_eblindfold_button_handler(self._eblind_handler)
        self.view.set_direct_control_button_handler(self._direct_control_handler)
        self.view.set_open_dur_line_edit_handler(self._open_dur_handler)
        self.view.set_close_dur_line_edit_handler(self._close_dur_handler)
        self.view.set_open_inf_check_box_handler(self._open_inf_handler)
        self.view.set_close_inf_check_box_handler(self._close_inf_handler)
        self.view.set_debounce_time_line_edit_handler(self._debounce_handler)
        self.view.set_button_mode_selector_handler(self._button_mode_handler)
        self.view.set_control_mode_selector_handler(self._control_mode_handler)
        self.view.set_upload_settings_button_handler(self._update_device)
        self.view.set_manual_control_open_button_handler(self._manual_open_handler)
        self.view.set_manual_control_close_button_handler(self._manual_close_handler)
        self._logger.debug("done")

    def _init_values(self) -> None:
        """
        Send for device config.
        :return: None.
        """
        self._logger.debug("running")
        self._model.query_config()
        self._logger.debug("done")

    def _config_name_handler(self) -> None:
        """
        Handle user changing config name.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            self._model.check_config_entry(self.view.config_text)
            self._check_for_upload()
        self._logger.debug("done")

    def _open_dur_handler(self) -> None:
        """
        Handle user changing open duration value.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            self.view.set_open_dur_err(not self._model.check_open_entry(self.view.open_duration))
            self._check_for_upload()
        self._logger.debug("done")

    def _close_dur_handler(self) -> None:
        """
        Handle user changing close duration value.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            self.view.set_close_dur_err(not self._model.check_close_entry(self.view.close_duration))
            self._check_for_upload()
        self._logger.debug("done")

    def _open_inf_handler(self, state: int) -> None:
        """
        Handle user changing open inf val.
        :param state: Whether inf is checked or not.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            if state == 2:
                self._prev_vals[0] = self.view.open_duration
                self.view.open_duration = str(defs.max_open_close)
            elif state == 0:
                self.view.open_duration = self._prev_vals[0]
            self.view.set_open_dur_err(not self._model.check_open_entry(self.view.open_duration))
            self._check_for_upload()
        self._logger.debug("done")

    def _close_inf_handler(self, state: int) -> None:
        """
        Handle user changing close inf val.
        :param state: Whether inf is checked or not.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            if state == 2:
                self._prev_vals[1] = self.view.close_duration
                self.view.close_duration = str(defs.max_open_close)
            elif state == 0:
                self.view.close_duration = self._prev_vals[1]
            self.view.set_close_dur_err(not self._model.check_close_entry(self.view.close_duration))
            self._check_for_upload()
        self._logger.debug("done")

    def _debounce_handler(self) -> None:
        """
        Handle user changing debounce time value.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            self.view.set_debounce_err(not self._model.check_debounce_entry(self.view.debounce_val))
            self._check_for_upload()
        self._logger.debug("done")

    def _button_mode_handler(self) -> None:
        """
        Handle user changing button mode.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            self._model.check_button_mode_entry(self.view.button_mode)
            self._check_for_upload()
        self._logger.debug("done")

    def _control_mode_handler(self) -> None:
        """
        Handle user changing control mode.
        :return None:
        """
        self._logger.debug("running")
        if not self._updating_config:
            self._model.check_control_mode_entry(self.view.control_mode)
            self._check_for_upload()
        self._logger.debug("done")

    def _update_device(self) -> None:
        """
        Handle user clicking upload button.
        :return None:
        """
        self._logger.debug("running")
        if self._model.name_changed():
            self._model.send_name(self.view.config_text)
        if self._model.open_changed():
            self._model.send_open(self.view.open_duration)
        if self._model.close_changed():
            self._model.send_close(self.view.close_duration)
        if self._model.debounce_changed():
            self._model.send_debounce(self.view.debounce_val)
        if self._model.button_mode_changed():
            self._model.send_button_control(self.view.button_mode)
        if self._model.control_mode_changed():
            self._model.send_click(self.view.control_mode)
        self._model.reset_changed()
        self._check_for_upload()
        self._logger.debug("done")

    def _manual_open_handler(self) -> None:
        """
        Handle user clicking open lens button.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_lens_open()
        self._logger.debug("done")

    def _manual_close_handler(self) -> None:
        """
        Handle user clicking close lens button.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_lens_close()
        self._logger.debug("done")

    def _nhtsa_handler(self) -> None:
        """
        Handle user click on NHTSA button.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_nhtsa()
        self._model.reset_changed()
        self._check_for_upload()
        self._logger.debug("done")

    def _eblind_handler(self) -> None:
        """
        Handle user click on eBlindfold button.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_eblind()
        self._model.reset_changed()
        self._check_for_upload()
        self._logger.debug("done")

    def _direct_control_handler(self) -> None:
        """
        Handle user click on direct control button.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_direct_control()
        self._model.reset_changed()
        self._check_for_upload()
        self._logger.debug("done")

    def _update_view_config(self, msg: dict) -> None:
        """
        Send device config updates to the view.
        :param msg: The current device settings.
        :return: None.
        """
        self._logger.debug("running")
        self._updating_config = True
        try:
            for key in msg:
                self._set_view_val(key, msg[key])
        finally:
            self._updating_config = False
            self._model.reset_changed()
            self._check_for_upload()
        self._logger.debug("done")

    def _set_view_val(self, var: str, val: str) -> None:
        """
        Set the value for the config field in the view.
        :param var: The config field.
        :param val: The new value.
        :return: None.
        """
        self._logger.debug("running")
        if var == "Name":
            self._model.set_current_vals(name=val)
            self.view.config_text = val
        elif var == "MaxOpen":
            int_val = int(val)
            if int_val == defs.max_open_close:
                self.view.open_inf_check_box = True
            else:
                self.view.open_inf_check_box = False
            self._model.set_current_vals(max_open=int_val)
            self.view.open_duration = val
            self._prev_vals[0] = val  # TODO: Does this overwrite after we hit upload?
            self.view.set_open_dur_err(False)
        elif var == "MaxClose":
            int_val = int(val)
            if int_val == defs.max_open_close:
                self.view.close_inf_check_box = True
            else:
                self.view.close_inf_check_box = False
            self._model.set_current_vals(max_close=int_val)
            self.view.close_duration = val
            self._prev_vals[1] = val  # TODO: Does this overwrite after we hit upload?
            self.view.set_close_dur_err(False)
        elif var == "Debounce":
            int_val = int(val)
            self._model.set_current_vals(debounce=int_val)
            self.view.debounce_val = val
            self.view.set_debounce_err(False)
        elif var == "ClickMode":
            int_val = int(val)
            self._model.set_current_vals(button_mode=int_val)
            self.view.button_mode = int_val
        elif var == "buttonControl":
            int_val = int(val)
            self._model.set_current_vals(control_mode=int_val)
            self.view.control_mode = int_val
        self._logger.debug("done")

    def _check_for_upload(self) -> None:
        """
        Set view upload button depending on if upload is possible.
        :return: None.
        """
        self._logger.debug("running")
        self.view.set_upload_button(self._model.check_current_input())
        self._logger.debug("done")

    def _update_view_data(self, values: dict, timestamp: datetime) -> None:
        """
        Display data from device on view.
        :param values: The data to display.
        :param timestamp: When the data was received.
        :return: None.
        """
        self._logger.debug("running")
        data = [timestamp, int(values[defs.output_field[1]]), int(values[defs.output_field[2]])]
        self._graph.add_data(data)
        self._logger.debug("done")
