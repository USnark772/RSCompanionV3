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
from asyncio import Event, create_task, futures, sleep, get_running_loop
from cv2 import VideoCapture
from RSCompanionAsync.Model.app_helpers import await_event
from RSCompanionAsync.Devices.Camera.Model.cam_defs import cap_backend


class CamCounter:
    def __init__(self, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self.known_indicies = list()
        self._logger.debug("Initialized")

    def reset(self) -> None:
        """
        Reset known camera indicies.
        :return:
        """
        self._logger.debug("running")
        self.known_indicies = list()
        self._logger.debug("done")

    def get_next_index(self) -> int:
        """
        Get the next unused camera index.
        :return int: The next unused camera index.
        """
        self._logger.debug("running")
        ret = 0
        if len(self.known_indicies) > 0:
            ret = self._find_missing()
        self._logger.debug("done with index:" + str(ret))
        return ret

    def _find_missing(self):
        """
        Find the first missing index in numerical order.
        :return:
        """
        self._logger.debug("running")
        ret = sorted(set(range(0, self.known_indicies[-1] + 2)) - set(self.known_indicies))[0]
        self._logger.debug("done with ret:" + str(ret))
        return ret

    def add_index(self, cam_index) -> None:
        """
        Add index to list.
        :param cam_index: The index to add.
        :return None:
        """
        self._logger.debug("running")
        self.known_indicies.append(cam_index)
        self.known_indicies.sort()
        self._logger.debug("done")

    def remove_index(self, cam_index) -> None:
        """
        Remove the given index from the list.
        :param cam_index: The index to remove.
        :return None:
        """
        self._logger.debug("running")
        if cam_index in self.known_indicies:
            self.known_indicies.remove(cam_index)
        self._logger.debug("done")


class CamScanner:
    def __init__(self, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._counter = CamCounter(log_handlers)
        self._connect_event = Event()
        self._disconnect_event = Event()
        self._connect_err_event = Event()
        self._tasks = list()
        self._unhandled_cams = list()
        self._connect_event.set()
        self._running = True
        self._loop = get_running_loop()
        self._logger.debug("Initialized")

    async def cleanup(self):
        """
        Cleanup this object and prep for app closure.
        :return None:
        """
        self._logger.debug("running")
        self._running = False
        for task in self._tasks:
            task.cancel()
        self._logger.debug("done")

    async def _scan_for_cams(self) -> None:
        """
        Scan for new cameras and flag if new camera found.
        :return None:
        """
        self._logger.debug("running")
        while self._running:
            ret = await self._loop.run_in_executor(None, self._check_for_cam, self._counter.get_next_index())
            # ret = self._check_for_cam(self._counter.get_next_index())
            if ret[0]:
                while ret[0]:
                    self._unhandled_cams.append(ret[1])
                    self._counter.add_index(ret[1])
                    ret = self._check_for_cam(self._counter.get_next_index())
                self._connect_event.set()
            else:
                await sleep(2)

    def _check_for_cam(self, cam_index) -> (bool, int):
        """
        Check the given index for an unused camera.
        :param cam_index: The given index
        :return None:
        """
        self._logger.debug("running")
        ret = (False, -1)
        cap = VideoCapture(cam_index, cap_backend)
        if cap and cap.isOpened():
            cap.release()
            ret = True, cam_index
        self._logger.debug("done with: " + str(ret[0]) + " " + str(ret[1]))
        return ret

    def get_next_new_cam(self) -> (bool, int):
        """
        Get next unhandled camera index and remove it from list.
        :return (bool, int): (If there is an unhandled camera, The next unhandled camera index).
        """
        self._logger.debug("running")
        ret = (False, -1)
        if len(self._unhandled_cams) > 0:
            ret = (True, self._unhandled_cams.pop(0))
        self._logger.debug("done with: " + str(ret[0]) + " " + str(ret[1]))
        return ret

    def await_connect(self) -> futures:
        """
        Signal when there is a connect event.
        :return futures: If the flag is set.
        """
        return await_event(self._connect_event)

    def await_err(self) -> futures:
        """
        Signal when there is an error with device connection.
        :return futures: If the flag is set.
        """
        return await_event(self._connect_err_event)

    def remove_cam_index(self, cam_index: int) -> None:
        """
        Remove index from list of known camera indices.
        :param cam_index: The index to remove.
        :return None:
        """
        self._logger.debug("running")
        self._counter.remove_index(cam_index)
        self._logger.debug("done")

    def activate(self) -> None:
        """
        Set this scanner to search for cameras.
        :return None:
        """
        self._logger.debug("running")
        self._running = True
        self._tasks.append(create_task(self._scan_for_cams()))
        self._logger.debug("done")

    def deactivate(self) -> None:
        """
        Set this scanner to do nothing.
        :return None:
        """
        self._logger.debug("running")
        self._running = False
        print(__name__, "Implement cam_scanner.deactivate().")
        self._logger.debug("done")
