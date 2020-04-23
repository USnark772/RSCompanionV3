""" Licensed under GNU GPL-3.0-or-later """

"""
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
"""

# Author: Joel Cooper
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import asyncio
import aioserial
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException
import time


class Comports:
    def __init__(self, device_ids, event_callback: asyncio.Event):
        self.event_callback = event_callback
        self.attached = {}

        ports = comports()
        self._ports_count = len(ports)
        self._device_ids = device_ids
        self._update_attached_devices(ports)

        self.running = True
        self.loop = asyncio.get_running_loop()
        self.loop.run_in_executor(None, self._scan_for_change)

    def cleanup(self):
        self.running = False
        for val in self.attached.values():
            val['conn'].close()

    def _scan_for_change(self):
        while self.running:
            ports = comports()
            ports_count = len(ports)
            if ports_count != self._ports_count:
                if ports_count < self._ports_count:
                    self.loop.call_soon_threadsafe(self._remove_event, ports)
                elif ports_count > self._ports_count:
                    self.loop.call_soon_threadsafe(self._plug_event, ports)
            self._ports_count = ports_count
            time.sleep(.1)

    def _plug_event(self, ports):
        self._update_attached_devices(ports)

    def _remove_event(self, ports):
        to_remove = []
        for key in self.attached.keys():
            if key not in ports:
                to_remove.append(key)

        for key in to_remove:
            self.attached[key]['conn'].close()
            del self.attached[key]

        self.event_callback.set()

    def _update_attached_devices(self, ports):
        for port in ports:
            if port.device not in self.attached.keys():
                for device in self._device_ids:
                    if self.__verify_port(port, self._device_ids[device]):
                        ret_val, connection = self.__try_open_port(port)
                        if ret_val:
                            self.attached.update({port.device: {'type': device, 'conn': connection}})
                            self.event_callback.set()
                        else:
                            pass  # TODO: Alert user of connection issue
                        break

    @staticmethod
    def __verify_port(port: ListPortInfo, profile):
        return port.vid == profile['vid'] and port.pid == profile['pid']

    @staticmethod
    def __try_open_port(port):
        new_connection = aioserial.AioSerial()
        new_connection.port = port.device
        i = 0
        while not new_connection.is_open and i < 5:  # Make multiple attempts in case device is busy
            i += 1
            try:
                new_connection.open()
            except SerialException as e:
                time.sleep(1)
        if not new_connection.is_open:  # Failed to connect
            return False, None
        return True, new_connection
