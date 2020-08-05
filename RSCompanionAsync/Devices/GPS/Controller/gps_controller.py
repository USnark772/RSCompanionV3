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
from RSCompanionAsync.Devices.AbstractDevice.Controller.abstract_controller import AbstractController
from RSCompanionAsync.Devices.AbstractDevice.View.graph_frame import GraphFrame
from RSCompanionAsync.Devices.GPS.View.gps_view import GPSView
from RSCompanionAsync.Devices.GPS.View.gps_graph import GPSGraph
from RSCompanionAsync.Devices.GPS.Model.gps_model import GPSModel
from RSCompanionAsync.Devices.GPS.Model import gps_defs as defs
from RSCompanionAsync.Devices.GPS.Resources.gps_strings import strings, StringsEnum, LangEnum


class Controller(AbstractController):
    def __init__(self, conn: AioSerial = AioSerial(), lang: LangEnum = LangEnum.ENG,
                 log_handlers: [StreamHandler] = None):
        print("gps_controller")
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        try:
            device_name = "GPS_" + conn.port.strip("COM")
        except:
            device_name = "GPS_NONE"
        view = GPSView(device_name, log_handlers)
        super().__init__(view)
        print("here 1")
        self._model = GPSModel(device_name, conn, log_handlers)
        print("here 2")
        self._graph = GPSGraph(view, log_handlers)
        print("here 3")
        self.view.add_graph(GraphFrame(view, self._graph, log_handlers))
        print("here 4")
        self._exp = False
        self._updating_config = False
        print("here 5")
        self._setup_handlers()
        self._init_values()
        print("here 6")
        self._msg_handler_task = create_task(self.msg_handler())
        print("here 7")
        self._strings = dict()
        self.set_lang(lang)
        print("here 8")
        self._cont = True
        self._logger.debug("Initialized")

    async def cleanup(self, discard: bool = False) -> None:
        """
        Cleanup this code for removal or app closure
        :param discard: Quit without saving.
        :return None:
        """
        self._logger.debug("running")
        if self._exp:
            self.stop_exp()
        self._msg_handler_task.cancel()
        self._model.cleanup()
        self.view.save_window_state()
        self._logger.debug("done")

    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this device's view language.
        :param lang: The enum for the language.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._model.set_lang(lang)
        self.view.language = lang
        self._graph.set_lang(lang)
        self._logger.debug("done")

    def get_conn(self) -> AioSerial:
        """
        :return AioSerial: the AioSerial connection passed in at creation
        """
        return self._model.get_conn()

    async def msg_handler(self) -> None:
        """
        Handle messages sent from device.
        :return None:
        """
        self._logger.debug("running")
        while self._cont:
            self._model.gps.update()

            if not self._model.gps.has_fix:
                self.view.setTitle()
                print("waiting for fix...")
                continue
            print("=" * 150)
            print(self._model.gps.nmea_sentence)
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    self._model.gps.timestamp_utc.tm_mon,
                    self._model.gps.timestamp_utc.tm_mday,
                    self._model.gps.timestamp_utc.tm_year,
                    self._model.gps.timestamp_utc.tm_hour,
                    self._model.gps.timestamp_utc.tm_min,
                    self._model.gps.timestamp_utc.tm_sec,
                )
            )
            print("Latitude: {0:.6f} degrees".format(self._model.gps.latitude))
            print("Longitude: {0:.6f} degrees".format(self._model.gps.longitude))
            print("Fix quality: {}".format(self._model.gps.fix_quality))

            if self._model.gps.satellites is not None:
                print("# satellites: {}".format(self._model.gps.satellites))
            if self._model.gps.altitude_m is not None:
                print("Altitude: {} meters".format(self._model.gps.altitude_m))
            if self._model.gps.speed_knots is not None:
                print("Speed: {} knots".format(self._model.gps.speed_knots))
            if self._model.gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(self._model.gps.track_angle_deg))
            if self._model.gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(self._model.gps.horizontal_dilution))
            if self._model.gps.height_geoid is not None:
                print("Height geo ID: {} meters".format(self._model.gps.height_geoid))
        self._logger.debug("done")

    def create_exp(self, path: str, cond_name: str) -> None:
        """
        Set this device's save directory.
        :param path: The save directory.
        :param cond_name: The name for this part of the experiment.
        :return None:
        """
        self._logger.debug("running")
        self._graph.clear_graph()
        self._model.update_save_info(path)
        self._model.add_save_hdr()
        self._logger.debug("done")

    def end_exp(self) -> None:
        """
        Notify this device of experiment end
        :return None:
        """
        self._logger.debug("running")
        self._exp = False
        self._logger.debug("done")

    def _setup_handlers(self) -> None:
        """
        Attach handlers to view.
        :return None:
        """
        self._logger.debug("running")
        print("implement gps_controller.py _setup_handlers()")
        self._logger.debug("done")

    def _init_values(self) -> None:
        """
        Set up initial values
        :return None:
        """
        self._logger.debug("running")
        print("implement gps_controller.py _init_values()")
        self._logger.debug("done")
