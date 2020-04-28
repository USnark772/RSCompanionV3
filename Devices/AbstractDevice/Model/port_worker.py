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

from asyncio import get_running_loop
from threading import Event
from aioserial import AioSerial
from queue import Queue
from datetime import datetime


# TODO: See about running this from just create_task instead of run_in_executor.
class PortWorker:
    """
    This code is used to continually check an AioSerial port for incoming data, send alerts and pass on said data.
    Also used to send data through said port.
    """
    def __init__(self, conn: AioSerial, msg_q: Queue, new_msg_cb: Event, cleanup_cb: Event, err_cb: Event):
        self._conn = conn
        self._msg_q = msg_q
        self._new_msg_cb = new_msg_cb
        self._cleanup_cb = cleanup_cb
        self._err_cb = err_cb
        self._running = True
        self._loop = get_running_loop()

    def start(self) -> None:
        """
        Start running.
        :return: None.
        """
        self._loop.run_in_executor(None, self._run)

    def _run(self) -> None:
        """
        Run until signalled to stop.
        :return: None.
        """
        while self._running:
            self._check_for_msg()
        if self._err_cb.is_set():
            self.cleanup(self._err_cb.is_set())

    def _check_for_msg(self) -> None:
        """
        Check port for new message. If new message, put message and timestamp into queue and then set flag.
        If failure with port, stop and set error flag.
        :return: None.
        """
        try:
            if self._conn.in_waiting > 0:
                msg = self._conn.readline().decode("utf-8")
                print("port_worker: Got message from device:", msg)
                self._msg_q.put((msg, datetime.now()))
                self._new_msg_cb.set()
        except Exception as e:
            self._running = False
            self._err_cb.set()

    def send_msg(self, msg) -> None:
        """
        Send message through port if port is open.
        :param msg: The message to send.
        :return: None.
        """
        if self._conn.is_open:
            self._conn.write(str.encode(msg))

    def cleanup(self, err: bool = False) -> None:
        """
        Close port and signal loops to stop. Set cleanup flag.
        :return:
        """
        self._running = False
        self._conn.close()
        if not err:
            self._cleanup_cb.set()
