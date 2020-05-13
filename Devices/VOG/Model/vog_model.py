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
from asyncio import create_task
from aioserial import AioSerial
from math import trunc, ceil
from datetime import datetime
from Model.app_helpers import write_line_to_file, format_current_time
from Devices.VOG.Model import vog_defs as defs
from Devices.VOG.Resources.vog_strings import strings, StringsEnum, LangEnum


class VOGModel:
    def __init__(self, dev_name: str, conn: AioSerial, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._dev_name = dev_name
        self._conn = conn
        self._save_filename = str()
        self._save_dir = str()
        self._strings = dict()
        self._current_vals = ["", 0, 0, 0, 0]  # current config, open, close, debounce, mode
        self._errs = [False, False, False]  # open, close, debounce
        self._changed = [False, False, False, False, False] # current config, open, close, debounce, mode
        self._logger.debug("Initialized")

    def get_conn(self) -> AioSerial:
        """
        :return: The AioSerial connection passed in at creation.
        """
        return self._conn

    def update_save_info(self, path: str) -> None:
        """
        Set this device's output path to path.
        :param path: The output path to use.
        :return None:
        """
        self._save_dir = path
        self._save_filename = self._dev_name + "_" + format_current_time(datetime.now(), save=True) + ".csv"

    def set_current_vals(self, name: str = None, open: int = None, close: int = None, debounce: int = None) -> None:
        """
        Set the current values the device should have.
        :param name: The config name of the device.
        :param open: The max_open value.
        :param close: The max_close value.
        :param debounce: The debounce value.
        :return: None.
        """
        self._logger.debug("running")
        if name:
            self._current_vals[0] = name
        if open:
            self._current_vals[1] = open
        if close:
            self._current_vals[2] = close
        if debounce:
            self._current_vals[3] = debounce
        self._logger.debug("done")

    def reset_changed(self) -> None:
        """
        Reset all changed bools to false.
        :return: None.
        """
        for i in range(len(self._changed)):
            self._changed[i] = False

    def add_save_hdr(self) -> None:
        self._output_save_data(self._strings[StringsEnum.SAVE_HDR])

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this device's data output.
        :param lang: The lang enum to use.
        :return None:
        """
        self._strings = strings[lang]

    async def get_msg(self) -> (dict, datetime):
        """
        Get next message from device.
        :return (dict, datetime): (The next message from device, when the message was received.)
        """
        self._logger.debug("running")
        line = await self._conn.readline_async()
        msg = self._parse_msg(line.decode("utf-8"))
        timestamp = datetime.now()
        return msg, timestamp

    def cleanup(self) -> None:
        """
        Cleanup this code for code removal or app closure.
        :return: None.
        """
        self._logger.debug("running")
        self._conn.close()
        self._logger.debug("done")

    def check_current_input(self):
        pass

    def query_config(self) -> None:
        """
        Request current device settings.
        :return None:
        """
        self._logger.debug("running")
        self.query_name()
        self.query_open()
        self.query_close()
        self.query_debounce()
        self.query_click()
        self.query_button_control()
        self._logger.debug("done")

    def query_name(self) -> None:
        """
        Ask device for current name
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configName"))
        self._logger.debug("done")

    def query_open(self) -> None:
        """
        Ask device for current max open
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configMaxOpen"))
        self._logger.debug("done")

    def query_close(self) -> None:
        """
        Ask device for current max close
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configMaxClose"))
        self._logger.debug("done")

    def query_debounce(self) -> None:
        """
        Ask device for current debounce value
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configDebounce"))
        self._logger.debug("done")

    def query_click(self) -> None:
        """
        Ask device for current mode
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configClickMode"))
        self._logger.debug("done")

    def query_button_control(self) -> None:
        """
        Ask device for current config button type
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configButtonControl"))
        self._logger.debug("done")

    def send_name(self, val: str) -> None:
        """
        Ask device for current name
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configName", str(val)))
        self._logger.debug("done")

    def send_open(self, val: str) -> None:
        """
        Ask device for current max open
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configMaxOpen", str(val)))
        self._logger.debug("done")

    def send_close(self, val: str) -> None:
        """
        Ask device for current max close
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configMaxClose", str(val)))
        self._logger.debug("done")

    def send_debounce(self, val: str) -> None:
        """
        Ask device for current debounce value
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configDebounce", str(val)))
        self._logger.debug("done")

    def send_click(self, val: int) -> None:
        """
        Ask device for current mode
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configClickMode", str(val)))
        self._logger.debug("done")

    def send_button_control(self, val: str) -> None:
        """
        Ask device for current config button type
        :return None:
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_configButtonControl", str(val)))
        self._logger.debug("done")

    def save_data(self, data: dict, timestamp: datetime) -> None:
        """
        Save data to output file.
        :return: None
        """
        self._logger.debug("running")
        self._output_save_data(self._format_save_data(data, timestamp))
        self._logger.debug("done")

    def _output_save_data(self, line: str) -> None:
        """
        Write data to save file.
        :param line: The data to write.
        :return: None.
        """
        create_task(write_line_to_file(self._save_dir + self._save_filename, line))

    def _send_msg(self, msg) -> None:
        """
        encode and send a message over serial port
        :param msg: message to be sent
        :return None:
        """
        if self._conn.is_open:
            self._conn.write(str.encode(msg))

    def send_nhtsa(self):
        """
        Set device and display to nhtsa defaults.
        :return None:
        """
        self._logger.debug("running")
        # self.tab.set_open_inf(False)
        # self.tab.set_close_inf(False)
        self.send_name("NHTSA")
        self.send_open("1500")
        self.send_close("1500")
        self.send_debounce("20")
        self.send_click(1)
        self.send_button_control("0")
        # self._set_upload_button(False)
        self._logger.debug("done")

    def send_eblind(self):
        """
        Set device and display to eblind mode.
        :return None:
        """
        self._logger.debug("running")
        # self.tab.set_open_inf(True)
        # self.tab.set_close_inf(False)
        self.send_name("eBlindfold")
        self.send_open(defs.max_open_close)
        self.send_close("0")
        self.send_debounce("100")
        self.send_click(1)
        self.send_button_control("0")
        # self.__set_upload_button(False)
        self._logger.debug("done")

    def send_direct_control(self):
        """
        Set device and display to direct control mode.
        :return None:
        """
        self._logger.debug("running")
        # self.tab.set_open_inf(True)
        # self.tab.set_close_inf(True)
        self.send_name("DIRECT CONTROL")
        self.send_open(defs.max_open_close)
        self.send_close("0")
        self.send_debounce("100")
        self.send_click(0)
        self.send_button_control("1")
        # self.__set_upload_button(False)
        self._logger.debug("done")

    @staticmethod
    def _parse_msg(msg_string):
        ret = dict()
        ret['values'] = {}
        if msg_string[0:5] == "data|":
            ret['type'] = "data"
            val_ind_start = 5
            for i in range(len(defs.output_field)):
                val_ind_end = msg_string.find(',', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                ret['values'][defs.output_field[i]] = msg_string[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 1
        elif "config" in msg_string:
            ret['type'] = "settings"
            bar_ind = msg_string.find('|', 6)
            if msg_string[6:bar_ind] == "Name":
                ret['values']['Name'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "MaxOpen":
                ret['values']['MaxOpen'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "MaxClose":
                ret['values']['MaxClose'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "Debounce":
                ret['values']['Debounce'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "ClickMode":
                ret['values']['ClickMode'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
        elif "Click" in msg_string:
            ret['action'] = "Click"
        elif "buttonControl" in msg_string:
            ret['type'] = "settings"
            bar_ind = msg_string.find('|')
            ret['values'] = {}
            ret['values']['buttonControl'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
        elif "peek" in msg_string:
            ret['type'] = "settings"
            ret['values'] = {}
            ret['values']['lensState'] = msg_string.rstrip("\r\n")
        return ret

    @staticmethod
    def _prepare_msg(cmd, arg=None):
        """ Create string using vog syntax. """
        if arg:
            msg_to_send = ">" + cmd + "|" + arg + "<<\n"
        else:
            msg_to_send = ">" + cmd + "|" + "<<\n"
        return msg_to_send

    @staticmethod
    def _format_save_data(values: dict, timestamp: datetime) -> str:
        """
        Format values from device into readable output for saving.
        :param values: The values from the device.
        :param timestamp: The timestamp the values were received.
        :return: The formatted output.
        """
        line = format_current_time(timestamp, True, True, True) + ", "
        for i in defs.save_fields:
            line += str(values[i]) + ", "
        line = line.rstrip("\r\n")
        return line
