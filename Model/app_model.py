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

from logging import StreamHandler, getLogger
from asyncio import get_event_loop, all_tasks, current_task, gather
from queue import Queue
from asyncio import Event, create_task
from aioserial import AioSerial
from Model.rs_device_com_scanner import RSDeviceCommScanner
from Devices.DRT.Controller.drt_controller import DRTController
from Devices.DRT.Model.drt_defs import profile as drt_profile


def get_profiles():
    profs = [drt_profile]
    ret = dict()
    for prof in profs:
        for key in prof.keys():
            ret[key] = prof[key]
    return ret


class AppModel:
    def __init__(self, new_dev_flag: Event, dev_conn_err_flag: Event, close_flag: Event, view_parent, ch: StreamHandler):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        self._ch = ch
        self._new_dev_q = Queue()
        self._dev_scanner = RSDeviceCommScanner(get_profiles(), new_dev_flag, dev_conn_err_flag, self._new_dev_q)
        self._devs = dict()
        self._dev_inits = dict()
        self._dev_inits['DRT'] = self._make_drt
        self._logger.debug("Initialized")

    def add_new_device(self) -> None:
        """
        Get new device info from new device queue and
        :return:
        """
        self._logger.debug("running")
        dev_type, connection = self._new_dev_q.get()
        self._make_device(dev_type, connection)
        self._logger.debug("done")

    def _make_device(self, dev_type: str, conn: AioSerial):
        self._logger.debug("running")
        if dev_type not in self._dev_inits.keys():
            self._logger.warning("Could not recognize device type")
            return
        controller = self._dev_inits[dev_type](conn)
        if not controller:
            self._logger.warning("Failed making controller for type: " + dev_type)
            return
        self._logger.debug("done")

    def _make_drt(self, conn: AioSerial) -> bool:
        self._logger.debug("running")
        ret = True
        try:
            self._devs[conn.port] = DRTController(conn, self._ch)
        except Exception as e:
            self._logger.exception("Problem making controller")
            ret = False
        self._logger.debug("done")
        return ret

    def start(self):
        self._logger.debug("running")
        self._dev_scanner.start()
        self._logger.debug("done")

    def cleanup(self):
        self._logger.debug("running")
        self._dev_scanner.cleanup()
        for dev in self._devs.values():
            dev.cleanup()
        create_task(self._end_tasks())
        self._logger.debug("done")

    @staticmethod
    async def _end_tasks():
        tasks = [t for t in all_tasks() if t is not current_task()]
        [task.cancel() for task in tasks]
        await gather(*tasks)
        get_event_loop().stop()
