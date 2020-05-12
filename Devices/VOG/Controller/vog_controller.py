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

from logging import getLogger, StreamHandler
from datetime import datetime
from asyncio import create_task
from aioserial import AioSerial
from Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from Devices.AbstractDevice.View.graph_frame import GraphFrame
from Devices.VOG.View.vog_view import VOGView
from Devices.VOG.View.vog_graph import VOGGraph
from Devices.VOG.Model.vog_model import VOGModel
from Devices.VOG.Model import vog_defs as defs
from Devices.VOG.Resources.vog_strings import strings, StringsEnum, LangEnum


class Controller(AbstractController):
    def __init__(self, conn: AioSerial, lang: LangEnum, log_handlers: [StreamHandler]):
        self._logger = getLogger(__name__)
        for h in log_handlers:
            self._logger.addHandler(h)
        self._logger.debug("Initializing")
        device_name = "VOG_" + conn.port.strip("COM")
        view = VOGView(device_name, log_handlers)
        super().__init__(view)
        # self._model = VOGModel(device_name, conn, log_handlers)
        self._graph = VOGGraph(view, log_handlers)
        self.view.add_graph(GraphFrame(view, self._graph, log_handlers))
        self._exp_created = False
        self._exp_running = False
        self._updating_config = False
        # self._setup_handlers()
        # self._init_values()
        self._msg_handler_task = create_task(self.msg_handler())
        self._strings = dict()
        self.set_lang(lang)
        self._logger.debug("Initialized")

    def cleanup(self) -> None:
        """
        Cleanup this code for removal or app closure.
        :return: None.
        """
        self._logger.debug("running")
        if self._exp_created:
            self.end_exp()
        if self._exp_running:
            self.stop_exp()
        self._msg_handler_task.cancel()
        # self._model.cleanup()
        self._logger.debug("done")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this device's view language.
        :param lang: The enum for the language.
        :return: None.
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        # self._model.set_lang(lang)
        self.view.set_lang(lang)
        self._graph.set_lang(lang)
        self._logger.debug("done")

    def get_conn(self) -> AioSerial:
        """
        :return: The AioSerial connection passed in at creation.
        """
        return self._model.get_conn()

    async def msg_handler(self) -> None:
        """
        Handle messages sent from device.
        :return: None.
        """
        self._logger.debug("running")
        while True:
            msg, timestamp = await self._model.get_msg()
            msg_type = msg['type']
            # TODO: handle message on message type

    def create_exp(self, path: str) -> None:
        """
        Set this device's save dir.
        :param path: The save dir.
        :return None:
        """
        self._logger.debug("running")
        self._graph.clear_graph()
        self._model.update_save_info(path)
        self._model.add_save_hdr()
        self._model.send_create()
        self._logger.debug("done")

    def end_exp(self) -> None:
        """
        Notify this device of experiment end
        :return None:
        """
        self._logger.debug("running")
        self._model.send_end()
        self._logger.debug("done")

    def start_exp(self) -> None:
        """
        Notify this device of experiment start.
        :return None:
        """
        self._logger.debug("running")
        self._model.send_start()
        self._logger.debug("done")

    def stop_exp(self) -> None:
        """
        Notify this device of experiment stop.
        :return: None.
        """
        self._logger.debug("running")
        self._model.send_stop()
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        self._logger.debug("running")
        self._logger.debug("done")

    def _init_values(self) -> None:
        """
        Send for device config.
        :return: None.
        """
        self._logger.debug("running")
        self._model.query_config()
        self._logger.debug("done")
