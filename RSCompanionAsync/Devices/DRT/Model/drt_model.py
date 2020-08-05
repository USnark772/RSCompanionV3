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
from asyncio import create_task, get_running_loop
from aioserial import AioSerial, SerialException
from math import trunc, ceil
from datetime import datetime
from RSCompanionAsync.Model.app_helpers import write_line_to_file, format_current_time
from RSCompanionAsync.Devices.DRT.Model import drt_defs as defs
from RSCompanionAsync.Devices.DRT.Resources.drt_strings import strings, StringsEnum, LangEnum


class DRTModel:
    def __init__(self, dev_name: str = "DRT_NONE", conn: AioSerial = AioSerial(), log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._dev_name = dev_name
        self._conn = conn
        self._save_filename = str()
        self._save_dir = str()
        self._strings = dict()
        self._current_vals = [0] * 4  # dur, int, upper, lower
        self._errs = [False] * 4  # dur, int, upper, lower
        self._changed = [False] * 4
        self._loop = get_running_loop()
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
        # self._save_filename = self._dev_name + "_" + format_current_time(datetime.now(), save=True) + ".csv"
        self._save_filename = self._dev_name + ".csv"

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
        if type(duration) == int:
            self._current_vals[0] = duration
        if type(intensity) == int:
            self._current_vals[1] = intensity
        if type(upper_isi) == int:
            self._current_vals[2] = upper_isi
        if type(lower_isi) == int:
            self._current_vals[3] = lower_isi
        self._logger.debug("done")

    def reset_changed(self) -> None:
        """
        Reset all changed bools to false.
        :return: None.
        """
        self._logger.debug("running")
        for i in range(len(self._changed)):
            self._changed[i] = False
        self._logger.debug("done")

    def add_save_hdr(self) -> None:
        """
        Add header line to save file.
        :return None:
        """
        self._logger.debug("running")
        self._output_save_data(self._strings[StringsEnum.SAVE_HDR])
        self._logger.debug("done")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set the language for this device's data output.
        :param lang: The lang enum to use.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._logger.debug("done")

    def send_iso(self) -> None:
        """
        Reset device to ISO standards
        :return None:
        """
        self._logger.debug("running")
        self.send_stim_dur(str(defs.iso_standards["stimDur"]))
        self.send_stim_intensity(100)
        self.send_upper_isi(str(defs.iso_standards["upperISI"]))
        self.send_lower_isi(str(defs.iso_standards["lowerISI"]))
        self._logger.debug("done")

    async def get_msg(self) -> (dict, datetime):
        """
        Get next message from device.
        :return: (The next message from device, when the message was received.)
        """
        self._logger.debug("running")
        msg = await self._loop.run_in_executor(None, self.readline_threaded)
        self._logger.debug("done")
        return msg

    def readline_threaded(self) -> (dict, datetime):
        self._logger.debug("running")
        line = self._conn.readline()
        timestamp = datetime.now()
        msg = self._parse_msg(line.decode("utf-8"))
        self._logger.debug("done")
        return msg, timestamp

    def cleanup(self) -> None:
        """
        Cleanup this code for code removal or app closure.
        :return: None.
        """
        self._logger.debug("running")
        self._conn.close()
        self._logger.debug("done")

    def dur_changed(self) -> bool:
        """
        :return: Whether or not there is an unsaved user change to this vaue.
        """
        return self._changed[0]

    def int_changed(self) -> bool:
        """
        :return: Whether or not there is an unsaved user change to this vaue.
        """
        return self._changed[1]

    def upper_changed(self) -> bool:
        """
        :return: Whether or not there is an unsaved user change to this vaue.
        """
        return self._changed[2]

    def lower_changed(self) -> bool:
        """
        :return: Whether or not there is an unsaved user change to this value.
        """
        return self._changed[3]

    def query_config(self) -> None:
        """
        Ask device for all current configurations.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_config"))
        self._logger.debug("done")

    def query_stim_dur(self) -> None:
        """
        Ask device for current stim duration value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_stimDur"))
        self._logger.debug("done")

    def send_stim_dur(self, val: str) -> None:
        """
        Send new value to device.
        :param val: The new value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("set_stimDur", str(val)))
        self._logger.debug("done")

    def query_stim_intesity(self) -> None:
        """
        Ask device for current stim intensity value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_intensity"))
        self._logger.debug("done")

    def send_stim_intensity(self, val: int) -> None:
        """
        Send new value to device.
        :param val: The new value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("set_intensity", str(self.calc_percent_to_val(val))))
        self._logger.debug("done")

    def query_upper_isi(self) -> None:
        """
        Ask device for current upper isi value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_upperISI"))
        self._logger.debug("done")

    def send_upper_isi(self, val: str) -> None:
        """
        Send new value to device.
        :param val: The new value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("set_upperISI", str(val)))
        self._logger.debug("done")

    def query_lower_isi(self) -> None:
        """
        Ask device for current lower isi value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("get_lowerISI"))
        self._logger.debug("done")

    def send_lower_isi(self, val: str) -> None:
        """
        Send new value to device.
        :param val: The new value.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("set_lowerISI", str(val)))
        self._logger.debug("done")

    def send_start(self) -> None:
        """
        Tell device to start running experiment.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("exp_start"))
        self._logger.debug("done")

    def send_stop(self) -> None:
        """
        Tel device to stop running experiment.
        :return: None.
        """
        self._logger.debug("running")
        self._send_msg(self._prepare_msg("exp_stop"))
        self._logger.debug("done")

    def check_stim_dur_entry(self, entry: str) -> bool:
        """
        Check user input for validity.
        :param entry: The user input.
        :return: validity.
        """
        self._logger.debug("running with entry: " + entry)
        ret = False
        if entry.isdigit():
            val = int(entry)
            if defs.duration_max >= val >= defs.duration_min:
                self._changed[0] = (val != self._current_vals[0])
                ret = True
        self._errs[0] = not ret
        self._logger.debug("done with: " + str(ret))
        return ret

    def check_stim_int_entry(self, entry: int) -> bool:
        """
        Check user input for validity.
        :param entry: The user input.
        :return: validity.
        """
        ret = False
        self._logger.debug("running with entry: " + str(entry))
        val = self.calc_percent_to_val(int(entry))
        if defs.intensity_max >= val >= defs.intensity_min:
            self._changed[1] = (val != self._current_vals[1])
            self._logger.debug("done with true")
            ret = True
        self._errs[1] = not ret
        self._logger.debug("done with: " + str(ret))
        return ret

    def check_upper_isi_entry(self, upper_entry: str, lower_entry: str) -> bool:
        """
        Check user input for validity.
        :param upper_entry: The user input.
        :param lower_entry: The current input for lower_isi.
        :return: validity.
        """
        self._logger.debug("running with upper: " + upper_entry + ", and lower: " + lower_entry)
        ret = False
        if upper_entry.isdigit() and lower_entry.isdigit():
            upper_val = int(upper_entry)
            lower_val = int(lower_entry)
            if defs.ISI_max >= upper_val >= lower_val:
                self._changed[2] = (upper_val != self._current_vals[2])
                ret = True
        self._errs[2] = not ret
        self._logger.debug("done with: " + str(ret))
        return ret

    def check_lower_isi_entry(self, upper_entry: str, lower_entry: str) -> bool:
        """
        Check user input for validity.
        :param upper_entry: The current input for upper_isi
        :param lower_entry: The user input.
        :return: validity.
        """
        self._logger.debug("running with upper: " + upper_entry + ", and lower: " + lower_entry)
        ret = False
        if upper_entry.isdigit() and lower_entry.isdigit():
            upper_val = int(upper_entry)
            lower_val = int(lower_entry)
            if upper_val >= lower_val >= defs.ISI_min:
                self._changed[3] = (lower_val != self._current_vals[3])
                ret = True
        self._errs[3] = not ret
        self._logger.debug("done with: " + str(ret))
        return ret

    def check_current_input(self) -> bool:
        """
        Check user input for validity.
        :return: Whether the user input values are valid or not.
        """
        ret = False
        for x in self._changed:  # Check for any changes first.
            if x:
                ret = True
        for y in self._errs:  # If any errors, can't send changes.
            if y:
                ret = False
        return ret

    def save_data(self, data: dict, timestamp: datetime) -> None:
        """
        Save data to output file.
        :return: None
        """
        self._logger.debug("running")
        self._output_save_data(self._format_save_data(data, timestamp))
        self._logger.debug("done")

    def _send_msg(self, msg) -> None:
        """
        Encode and send a message over serial port
        :param msg: message to be sent
        :return None:
        """
        try:
            if self._conn.is_open:
                self._conn.write(msg.encode())
        except PermissionError as pe:
            self._logger.exception("Device " + self._dev_name + " connection failed")
        except SerialException as se:
            self._logger.exception("Device " + self._dev_name + " connection failed")
        except Exception as ge:
            self._logger.exception("Device " + self._dev_name + " connection failed")

    def _output_save_data(self, line: str) -> None:
        """
        Write data to save file.
        :param line: The data to write.
        :return: None.
        """
        create_task(write_line_to_file(self._save_dir + self._save_filename, line))

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
        # line = format_current_time(timestamp, date=True, time=True, micro=True)
        line = str(timestamp.timestamp())
        for i in defs.save_fields:
            line += ", " + str(values[i])
        line = line.rstrip("\r\n")
        return line
