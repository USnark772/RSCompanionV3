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

Author: Nathan Rogers
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from logging import getLogger, StreamHandler
from asyncio import create_task, get_running_loop
from aioserial import AioSerial, SerialException
from datetime import datetime
import adafruit_gps
from RSCompanionAsync.Model.app_helpers import write_line_to_file, format_current_time
from RSCompanionAsync.Devices.GPS.Model import gps_defs as defs
from RSCompanionAsync.Devices.GPS.Resources.gps_strings import strings, StringsEnum, LangEnum


class GPSModel:
    def __init__(self, dev_name: str = "GPS_NONE", conn: AioSerial = AioSerial(), log_handlers: [StreamHandler] = None):
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
        self._loop = get_running_loop()
        self.gps = adafruit_gps.GPS(self._conn, debug=False)
        self._send_msg("PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        self._logger.debug("Initialized")

    def get_conn(self) -> AioSerial:
        """
        :return AioSerial: The AioSerial connection passed in at creation
        """
        return self._conn

    def update_hz(self, hz: int) -> None:
        """
        Update GPS hertz
        :param hz: new hertz value to set the gps
        """
        self._logger.debug("running")
        self._send_msg("PMTK220," + str(hz * 1000))
        self._logger.debug("done")

    def update_save_info(self, path: str) -> None:
        """
        Set this device's output path to given path.
        :param path: The output path to use.
        :return None:
        """
        self._logger.debug("running")
        self._save_dir = path
        # self._save_filename = self._dev_name + "_" + format_current_time(datetime.now(), save=True) + ".csv"
        self._save_filename = self._dev_name + ".csv"
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
        :param lang: the language enumerator to use.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._logger.debug("done")

    async def get_msg(self) -> (dict, datetime):
        """
        Get next message from device.
        :return (dict, datetime): (The next message from device, time message was received.)
        """
        self._logger.debug("running")
        msg = await self._loop.run_in_executor(None, self.readline_threaded)
        self._logger.debug("done")
        return msg

    def readline_threaded(self) -> (dict, datetime):
        """
        :return (dict, datetime): (message from device, time message was received)
        """
        self._logger.debug("running")
        line = self._conn.readline()
        timestamp = datetime.now()
        msg = self._parse_msg(line.decode("utf-8"))
        self._logger.debug("done")
        return msg, timestamp

    def cleanup(self) -> None:
        """
        Cleanup this code for code removal or app closure.
        :return None:
        """
        self._logger.debug("running")
        self._conn.close()
        self._logger.debug("done")

    def save_data(self, data: dict, timestamp: datetime) -> None:
        """
        Save data to output file.
        :return None:
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
                self.gps.send_command(msg.encode())
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
        :return None:
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
        print("msg_string:", msg_string)

    @staticmethod
    def _prepare_msg(cmd: str, arg: str = None) -> str:
        """
        Create string using gps syntax
        :param cmd: the command to send.
        :param arg: the option parameter of the command.
        :return str: the message in the correct syntax.
        """
        if arg:
            msg_to_send = cmd + " " + arg + "\n"
        else:
            msg_to_send = cmd + "\n"
        return msg_to_send

    @staticmethod
    def _format_save_data(values: dict, timestamp: datetime) -> str:
        """
        Format values from device into readable ouput for saving
        :param values: The values from the device.
        :param timestamp: The timestamp from when the values were recieved.
        :return str: The formatted output.
        """
        # line = format_current_time(timestamp, date=True, time=True, micro=True)
        line = str(timestamp.timestamp())
        for i in defs.save_fields:
            line += ", " + str(values[i])
        line = line.rstrip("\r\n")
        return line
