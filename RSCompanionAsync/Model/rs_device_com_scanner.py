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
Author: Joel Cooper
Date: 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

from logging import getLogger, StreamHandler
from asyncio import Event, get_running_loop, create_task, futures, sleep
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from aioserial import AioSerial
from RSCompanionAsync.Model.app_helpers import await_event


class RSDeviceCommScanner:
    def __init__(self, device_ids: dict = None, log_handlers: [StreamHandler] = None):
        """
        Initialize scanner and prep for run.
        :param device_ids: The list of devices to look for.
        """
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        if device_ids:
            self._device_ids = device_ids
        else:
            self._device_ids = dict()
        self._connect_event = Event()
        self._disconnect_event = Event()
        self._connect_err_event = Event()
        self._new_coms = []
        self._lost_coms = []
        self._known_ports = []
        self._serials = {}
        self._tasks = []
        self._loop = get_running_loop()
        self._running = True
        self._logger.debug("Initialized")

    def start(self) -> None:
        """
        Begin working.
        :return None:
        """
        self._logger.debug("running")
        self._tasks.append(create_task(self._scan_ports()))
        self._logger.debug("done")

    async def cleanup(self) -> None:
        """
        Cleanup this object and prep for app closure.
        :return None:
        """
        self._logger.debug("running")
        self._running = False
        for task in self._tasks:
            task.cancel()
        self._logger.debug("done")

    def get_next_new_com(self) -> (bool, AioSerial):
        """
        Return the next new view if there is one.
        :return bool, AioSerial: If there is an element to return, The next element to return.
        """
        self._logger.debug("running")
        ret = False, None
        if len(self._new_coms) > 0:
            ret = (True, self._new_coms.pop(0))
        self._logger.debug("done with: " + str(ret[0]) + " " + str(ret[1]))
        return ret

    def get_next_lost_com(self) -> (bool, AioSerial):
        """
        Return the next new view if there is one.
        :return bool, AioSerial: If there is an element to return, The next element to return.
        """
        self._logger.debug("running")
        ret = False, None
        if len(self._lost_coms) > 0:
            self._logger.debug("done with true")
            ret = (True, self._lost_coms.pop(0))
        self._logger.debug("done with: " + str(ret[0]) + " " + str(ret[1]))
        return ret

    def await_connect(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._connect_event)

    def await_disconnect(self) -> futures:
        """
        Signal when there is a disconnect event.
        :return futures: If the flag is set.
        """
        return await_event(self._disconnect_event)

    def await_err(self) -> futures:
        """
        Signal when there is an error with device connection.
        :return futures: If the flag is set.
        """
        return await_event(self._connect_err_event)

    async def _scan_ports(self) -> None:
        """
        Check number of ports being used. If different than last checked, check for plug or unplug events.
        :return None:
        """
        self._logger.debug("running")
        while self._running:
            ports = await self._loop.run_in_executor(None, comports)
            if len(ports) > len(self._known_ports):
                create_task(self._check_for_new_devices(ports))
            elif len(ports) < len(self._known_ports):
                create_task(self._check_for_disconnects(ports))
            await sleep(1)

    async def _check_for_new_devices(self, ports: [ListPortInfo]) -> None:
        """
        Check plug events for supported Devices.
        :param ports: The list of ports to check.
        :return None:
        """
        self._logger.debug("running")
        for port in ports:
            if port not in self._known_ports:
                self._known_ports.append(port)
                for device_type in self._device_ids:
                    if self._verify_port(port, self._device_ids[device_type]):
                        ret_val, connection = await create_task(self._try_open_port(port))
                        if ret_val:
                            self._new_coms.append((device_type, connection))
                            self._connect_event.set()
                        else:
                            self._connect_err_event.set()
                        break
        self._logger.debug("done")

    async def _check_for_disconnects(self, ports: [ListPortInfo]) -> None:
        """
        Check the list of ports against list of known ports for any ports that are no longer in use
        and disconnect them.
        :param ports: List of ports to check
        :return None:
        """
        self._logger.debug("running")
        for known_port in self._known_ports:
            if known_port not in ports:
                self._known_ports.remove(known_port)
                for device_type in self._device_ids:
                    if self._verify_port(known_port, self._device_ids[device_type]):
                        self._lost_coms.append(known_port)
                        self._disconnect_event.set()
                        break
        self._logger.debug("done")

    @staticmethod
    def _verify_port(port: ListPortInfo, profile: dict) -> bool:
        """
        Check the port against the profile to tell if this is a supported device.
        :param port: The incoming port to check.
        :param profile: The device profile to match the port to.
        :return: Whether or not the port matches the profile.
        """
        return port.vid == profile['vid'] and port.pid == profile['pid']

    @staticmethod
    async def _try_open_port(port) -> (bool, AioSerial):
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
                await sleep(1)
        if not new_connection.is_open:  # Failed to connect
            return False, None
        return True, new_connection
