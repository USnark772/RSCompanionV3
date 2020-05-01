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

from asyncio import Event
import asyncio
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from aioserial import AioSerial
from queue import Queue


# TODO: Figure out if can use something other than Queue for passing device info around.
class RSDeviceCommScanner:
    def __init__(self, device_ids: dict):
        """
        Initialize scanner and run in thread.
        :param device_ids: The list of Devices to look for.
        :param new_cb: The callback for when a device is plugged in or unplugged.
        :param err_cb: The callback for when an error is encountered while trying to connect to a new device.
        """
        self._device_ids = device_ids
        self.com_new_q = Queue()
        self.com_remove_q = Queue()
        self._known_ports = []
        self._running = True
        self._loop = asyncio.get_running_loop()

    def com_start(self) -> None:
        """
        Begin working.
        :return: None.
        """
        asyncio.create_task(self._scan_ports())

    def com_cleanup(self) -> None:
        """
        Cleanup this class and prep for app closure.
        :return: None.
        """
        self._running = False

    async def _scan_ports(self) -> None:
        """
        Check number of ports being used. If different than last checked, check for plug or unplug events.
        :return: None.
        """
        while self._running:
            ports = await self._loop.run_in_executor(None, comports)
            if len(ports) > len(self._known_ports):
                asyncio.create_task(self._check_for_new_devices(ports))
            elif len(ports) < len(self._known_ports):
                self._check_for_disconnects(ports)

    async def _check_for_new_devices(self, ports: [ListPortInfo]) -> None:
        """
        Check plug events for supported Devices.
        :param ports: The list of ports to check.
        :return: None.
        """
        for port in ports:
            if port not in self._known_ports:
                for device_type in self._device_ids:
                    if self._verify_port(port, self._device_ids[device_type]):
                        ret_val, connection = await asyncio.create_task(self._try_open_port(port))
                        if ret_val:
                            self.com_new_q.put((device_type, connection))
                            self.com_event_connect()
                        else:
                            self.com_event_error()
                        break
                self._known_ports.append(port)

    def _check_for_disconnects(self, ports: [ListPortInfo]) -> None:
        """
        Check the list of ports against list of known ports for any ports that are no longer in use
        and disconnect them.
        :param ports: List of ports to check
        :return: None.
        """
        for known_port in self._known_ports:
            if known_port not in ports:
                self._known_ports.remove(known_port)
                for device_type in self._device_ids:
                    if self._verify_port(known_port, self._device_ids[device_type]):
                        self.com_remove_q.put(known_port)
                        self.com_event_remove()
                        break

    def com_event_connect(self):
        """
        Called when a device is attached.
        """
        pass

    def com_event_remove(self):
        """
        Called when a device is removed.
        """
        pass

    def com_event_error(self):
        """
        Called an error is received.
        """
        pass

    @staticmethod
    def _verify_port(port: ListPortInfo, profile: dict) -> bool:
        """
        Check the port against the profile to tell if this is a supported device.
        :param port: The incoming port to check.
        :param profile: The device profile to match the port to.
        :return: Whether or not the port matches the profile.
        """
        return port.vid == profile['vid'] and port.pid == profile['pid']

    # TODO: Figure out why this sometimes throws error even when device is connected successfully. I can't get an error here no matter how hard I try. It opens every time for me on the first try.
    @staticmethod
    async def _try_open_port(port) -> (bool, AioSerial):
        """
        Try to connect to the given port.
        :param port: The port to connect to
        :return: (success value, connection)
        """

        new_connection = AioSerial()
        new_connection.port = port.device
        new_connection.open()

        i = 0
        while not new_connection.is_open and i < 5:  # Make multiple attempts in case device is busy
            i += 1
            try:
                new_connection.open()
            except SerialException as e:
                await asyncio.sleep(1)

        if not new_connection.is_open:  # Failed to connect
            return False, None
        return True, new_connection
