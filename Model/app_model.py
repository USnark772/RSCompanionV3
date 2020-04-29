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

import os
import glob
import importlib.util
from logging import StreamHandler, getLogger
from asyncio import get_event_loop, all_tasks, current_task, gather, Event, create_task
from queue import Queue
from aioserial import AioSerial
from PySide2.QtWidgets import QMdiArea
from Model.rs_device_com_scanner import RSDeviceCommScanner


# TODO: Figure out close_flag. How to remove views?
class AppModel:
    def __init__(self, new_dev_view_flag: Event, dev_conn_err_flag: Event, close_flag: Event, view_parent: QMdiArea,
                 ch: StreamHandler):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        self._ch = ch
        self._view_parent = view_parent
        self._new_dev_q = Queue()
        self._profiles = self.get_profiles()
        self._controllers = self.get_controllers()
        self._new_dev_view_flag = new_dev_view_flag
        self._new_dev_flag = Event()
        self._dev_scanner = RSDeviceCommScanner(self._profiles, self._new_dev_flag, dev_conn_err_flag, self._new_dev_q)
        self._devs = dict()
        self._dev_inits = dict()
        self._new_dev_views = []
        self._tasks = []
        self._logger.debug("Initialized")

    async def add_new_device(self) -> None:
        """
        Get new device info from new device queue and
        :return:
        """
        self._logger.debug("running")
        dev_type: str
        dev_port: AioSerial
        while True:
            await self._new_dev_flag.wait()
            dev_type, connection = self._new_dev_q.get()
            self._make_device(dev_type, connection)
            if self._new_dev_q.empty():
                self._new_dev_flag.clear()
                self._logger.debug("done")

    def get_next_view(self):
        if self.has_unhandled_views():
            return self._new_dev_views.pop(0)

    def has_unhandled_views(self):
        return len(self._new_dev_views) > 0

    def _make_device(self, dev_type: str, conn: AioSerial):
        self._logger.debug("running")
        if dev_type not in self._controllers.keys():
            self._logger.warning("Could not recognize device type")
            return
        ret = self._make_controller(conn, dev_type)
        if not ret:
            self._logger.warning("Failed making controller for type: " + dev_type)
            return
        self._logger.debug("done")

    def _make_controller(self, conn: AioSerial, dev_type) -> bool:
        self._logger.debug("running")
        ret = True
        try:
            controller = self._controllers[dev_type](conn, self._view_parent, self._ch)
            self._devs[conn.port] = controller
            self._new_dev_views.append(controller.get_view())
            self._new_dev_view_flag.set()
        except Exception as e:
            self._logger.exception("Problem making controller")
            ret = False
        self._logger.debug("done")
        return ret

    def start(self):
        self._logger.debug("running")
        self._tasks.append(create_task(self.add_new_device()))
        self._dev_scanner.start()
        self._logger.debug("done")

    def cleanup(self):
        self._logger.debug("running")
        self._dev_scanner.cleanup()
        for dev in self._devs.values():
            dev.cleanup()
        create_task(self.end_tasks())
        self._logger.debug("done")

    async def end_tasks(self):
        for task in self._tasks:
            task.cancel()
            await gather(self._tasks)

    # TODO add debugging
    @staticmethod
    def get_profiles():
        profs = {}
        for device in os.listdir('Devices'):
            if device != "AbstractDevice":
                fpath = glob.glob("Devices/" + device + "/Model/*defs.py")
                if fpath:
                    spec = importlib.util.spec_from_file_location("stuff", fpath[0])
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    profs.update(mod.profile)
        return profs

    # TODO add debugging
    @staticmethod
    def get_controllers():
        controllers = {}
        for device in os.listdir('Devices'):
            if device != "AbstractDevice":
                fpath = glob.glob("Devices/" + device + "/Controller/*controller.py")
                if fpath:
                    spec = importlib.util.spec_from_file_location(device, fpath[0])
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    controllers.update({device: mod.Controller})
        return controllers

    @staticmethod
    async def _end_tasks():
        tasks = [t for t in all_tasks() if t is not current_task()]
        [task.cancel() for task in tasks]
        await gather(*tasks)
        get_event_loop().stop()
