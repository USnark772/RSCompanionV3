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
from queue import Queue
from aioserial import AioSerial
from asyncio import Event
from math import trunc, ceil
from datetime import datetime
from Devices.AbstractDevice.Model.abstract_model import AbstractModel
from Devices.AbstractDevice.Model.port_worker import PortWorker
from Devices.DRT.Model import drt_defs as defs


class DRTModel(AbstractModel):
    def __init__(self, port: AioSerial, save_dir: str, new_msg_cb: Event, cleanup_cb: Event, err_cb: Event,
                 ch: StreamHandler):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        super().__init__()
        self._msg_q = Queue()
        self._port_worker = PortWorker(port, self._msg_q, new_msg_cb, cleanup_cb, err_cb)
        self._save_dir = save_dir
        self._current_vals = [0, 0, 0, 0]
        self._errs = [False, False]
        self._logger.debug("Initialized")

    def set_current_vals(self, duration: int = None, intensity: int = None, upper_isi: int = None,
                         lower_isi: int = None) -> None:
        """
        Set the current values the device should have.
        :param duration: The stim duration value.
        :param intensity: The stim intensity value.
        :param upper_isi: The upper_isi value.
        :param lower_isi: The lower_isi value.
        :return: None.
        """
        self._logger.debug("running")
        if duration:
            self._current_vals[0] = duration
        if intensity:
            self._current_vals[1] = intensity
        if upper_isi:
            self._current_vals[2] = upper_isi
        if lower_isi:
            self._current_vals[3] = lower_isi
        self._logger.debug("done")

    def get_msg(self) -> (bool, dict):
        """
        Get next message from device.
        :return: (success, The next message from device)
        """
        self._logger.debug("running")
        if not self._msg_q.empty():
            self._logger.debug("done with msg")
            return True, self._parse_msg(self._msg_q.get())
        self._logger.debug("done with no msg")
        return False, ''

    def cleanup(self):
        self._logger.debug("running")
        self._port_worker.cleanup()
        self._logger.debug("done")

    def query_config(self):
        self._logger.debug("running")
        self._port_worker.send_msg(self._prepare_msg("get_config"))
        self._logger.debug("done")

    def send_start(self):
        self._logger.debug("running")
        self._port_worker.send_msg(self._prepare_msg("exp_start"))
        self._logger.debug("done")

    def send_stop(self):
        self._logger.debug("running")
        self._port_worker.send_msg(self._prepare_msg("exp_stop"))
        self._logger.debug("done")

    def check_stim_dur_entry(self, entry: str) -> bool:
        self._logger.debug("running with entry: " + entry)
        if entry.isdigit():
            val = int(entry)
            if defs.duration_max >= val >= defs.duration_min:
                self._logger.debug("done with true")
                return True
        self._logger.debug("done with false")
        return False

    def check_stim_int_entry(self, entry: str) -> bool:
        self._logger.debug("running with entry: " + entry)
        if entry.isdigit():
            val = int(entry)
            if defs.intensity_max >= val >= defs.intensity_min:
                self._logger.debug("done with true")
                return True
        self._logger.debug("done with false")
        return False

    def check_upper_isi_entry(self, upper_entry: str, lower_entry: str) -> bool:
        self._logger.debug("running with upper: " + upper_entry + ", and lower: " + lower_entry)
        if upper_entry.isdigit() and lower_entry.isdigit():
            upper_val = int(upper_entry)
            lower_val = int(lower_entry)
            if defs.ISI_max >= upper_val >= lower_val:
                self._logger.debug("done with true")
                return True
        self._logger.debug("done with false")
        return False

    def check_lower_isi_entry(self, upper_entry: str, lower_entry: str) -> bool:
        self._logger.debug("running with upper: " + upper_entry + ", and lower: " + lower_entry)
        if upper_entry.isdigit() and lower_entry.isdigit():
            upper_val = int(upper_entry)
            lower_val = int(lower_entry)
            if upper_val >= lower_val >= defs.ISI_min:
                self._logger.debug("done with true")
                return True
        self._logger.debug("done with false")
        return False

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
        print("Implement DRTModel._output_save_data()")

    @staticmethod
    def _parse_msg(msg_string: str) -> dict:
        """
        Parse message from device into useful keyval pairs.
        :param msg_string: The string to parse.
        :return: dictionary containing result of parsing.
        """
        ret = dict()
        ret['values'] = {}
        if msg_string[0:4] == "cfg>":
            ret['type'] = "settings"
            # Check if this is a response to get_config
            if len(msg_string) > 90:
                # Get relevant values from msg and insert into ret
                for i in defs.config_fields:
                    index = msg_string.find(i + ":")
                    index_len = len(i) + 1
                    val_len = msg_string.find(', ', index + index_len)
                    if val_len < 0:
                        val_len = None
                    ret['values'][msg_string[index:index+index_len-1]] = int(msg_string[index+index_len:val_len])
            else:
                # Single value update, find which value it is and insert into ret
                for i in defs.config_fields:
                    index = msg_string.find(i + ":")
                    if index > 0:
                        index_len = len(i)
                        val_ind = index + index_len + 1
                        ret['values'][msg_string[index:index + index_len]] = int(msg_string[val_ind:])
        elif msg_string[0:4] == "trl>":
            ret['type'] = "data"
            val_ind_start = 4
            for i in defs.output_fields:
                val_ind_end = msg_string.find(', ', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                ret['values'][i] = int(msg_string[val_ind_start:val_ind_end])
                if val_ind_end:
                    val_ind_start = val_ind_end + 2
        return ret

    @staticmethod
    def _prepare_msg(cmd: str, arg: str = None) -> str:
        """
        Create string using drt syntax.
        :param cmd: The cmd to send.
        :param arg: The option parameter of the command.
        :return str: The message in the correct syntax.
        """
        if arg:
            msg_to_send = cmd + " " + arg + "\n"
        else:
            msg_to_send = cmd + "\n"
        return msg_to_send

    @staticmethod
    def calc_val_to_percent(val: int) -> int:
        """
        Calculate the value of stim intensity from device.
        :param val: The value to be converted.
        :return int: The converted percentage.
        """
        return trunc(val / defs.intensity_max * 100)

    @staticmethod
    def calc_percent_to_val(val: int) -> int:
        """
        Calculate the value of stim intensity for device.
        :param val: The percentage to be converted.
        :return int: The converted value.
        """
        return ceil(val / 100 * defs.intensity_max)

    @staticmethod
    def _format_save_data(values: dict, timestamp: datetime) -> str:
        """
        Format values from device into readable output for saving.
        :param values: The values from the device.
        :param timestamp: The timestamp the values were received.
        :return: The formatted output.
        """
        line = ""
        for i in defs.save_fields:
            line += ", " + str(values[i])
        line = line.rstrip("\r\n")
        line = line + ", "
        return line

