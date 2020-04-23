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

from asyncio import Event, get_running_loop
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from time import sleep
from aioserial import AioSerial
from queue import Queue
from PySide2.QtCore import QObject, Signal


class ScannerSig(QObject):
    new_device_sig = Signal(str, AioSerial)
    connection_failure_sig = Signal(str)


class RSDeviceCommScanner:
    def __init__(self, device_ids: dict, std_cb: Event, err_cb: Event, q: Queue):
        """
        Initialize scanner and run in thread.
        :param device_ids: The list of Devices to look for.
        :param std_cb: The callback for when a device is plugged in or unplugged.
        :param err_cb: The callback for when an error is encountered while trying to connect to a new device.
        """
        self.signals = ScannerSig()
        self.__device_ids = device_ids
        self.std_cb = std_cb
        self.err_cb = err_cb
        self.q = q
        self.__known_ports = []
        self.__running = True
        self.__loop = get_running_loop()
        self.__loop.run_in_executor(None, self.scan_ports)

    def cleanup(self):
        self.__running = False

    def scan_ports(self) -> None:
        """
        Check number of ports being used. If different than last checked, check for plug or unplug events.
        :return: None
        """
        while self.__running:
            ports = comports()
            if len(ports) > len(self.__known_ports):
                self.__check_for_new_devices(ports)
            elif len(ports) < len(self.__known_ports):
                self.__check_for_disconnects(ports)
            sleep(.1)

    def __check_for_new_devices(self, ports: [ListPortInfo]) -> None:
        """
        Check plug events for supported Devices.
        :param ports: The list of ports to check.
        :return: None
        """
        for port in ports:
            if port not in self.__known_ports:
                for device_type in self.__device_ids:
                    if self.__verify_port(port, self.__device_ids[device_type]):
                        ret_val, connection = self.__try_open_port(port)
                        if ret_val:
                            self.q.put(port)
                            self.std_cb.set()
                        else:
                            self.err_cb.set()
                        break
                self.__known_ports.append(port)

    def __check_for_disconnects(self, ports: [ListPortInfo]) -> None:
        """
        Check the list of ports against list of known ports for any ports that are no longer in use
        and disconnect them.
        :param ports: List of ports to check
        :return: None
        """
        for known_port in self.__known_ports:
            if known_port not in ports:
                self.__known_ports.remove(known_port)

    @staticmethod
    def __verify_port(port: ListPortInfo, profile: dict) -> bool:
        """
        Check the port against the profile to tell if this is a supported device.
        :param port: The incomming port to check.
        :param profile: The device profile to match the port to.
        :return: Whether or not the port matches the profile.
        """
        return port.vid == profile['vid'] and port.pid == profile['pid']

    @staticmethod
    def __try_open_port(port) -> (bool, AioSerial):
        """
        Try to connect to the given port.
        :param port: The port to connect to
        :return: (success value, connection)
        """
        new_connection = AioSerial()
        new_connection.port = port.device
        i = 0
        while not new_connection.is_open and i < 5:  # Make multiple attempts in case device is busy
            i += 1
            try:
                new_connection.open()
            except SerialException as e:
                sleep(1)
        if not new_connection.is_open:  # Failed to connect
            return False, None
        return True, new_connection
