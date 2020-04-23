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

from asyncio import get_running_loop, Event
from aioserial import AioSerial
from queue import Queue
from datetime import datetime


class PortWorker:
    """
    This code is used to continually check an AioSerial port for incoming data, send alerts and pass on said data.
    Also used to send data through said port.
    """
    def __init__(self, name: str, port: AioSerial, msg_q: Queue, new_msg_cb: Event, cleanup_cb: Event, err_cb: Event):
        self.__device_name = name
        self.__port = port
        self.__msg_q = msg_q
        self.__new_msg_cb = new_msg_cb
        self.__cleanup_cb = cleanup_cb
        self.__err_cb = err_cb
        self.__running = True
        self.__loop = get_running_loop()

    def start(self) -> None:
        """
        Start running.
        :return: None.
        """
        self.__loop.run_in_executor(None, self.__run)

    async def __run(self) -> None:
        """
        Run until signalled to stop.
        :return: None.
        """
        while self.__running:
            self.__check_for_msg()
        self.cleanup(self.__err_cb.is_set())

    def __check_for_msg(self) -> None:
        """
        Check port for new message. If new message, put message and timestamp into queue and then set flag.
        If failure with port, stop and set error flag.
        :return: None.
        """
        try:
            if self.__port.in_waiting > 0:
                self.__msg_q.put((self.__port.readline().decode("utf-8"), datetime.now()))
                self.__new_msg_cb.set()
        except Exception as e:
            self.__running = False
            self.__err_cb.set()

    def send_msg(self, msg) -> None:
        """
        Send message through port if port is open.
        :param msg: The message to send.
        :return: None.
        """
        if self.__port.is_open:
            self.__port.write(str.encode(msg))

    def cleanup(self, err: bool = False) -> None:
        """
        Close port and signal loops to stop. Set cleanup flag.
        :return:
        """
        self.__running = False
        self.__port.close()
        if not err:
            self.__cleanup_cb.set()
