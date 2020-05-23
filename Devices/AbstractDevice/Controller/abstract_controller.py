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

from abc import ABC, abstractmethod
from Model.app_defs import LangEnum
from aioserial import AioSerial
from Devices.AbstractDevice.View.abstract_view import AbstractView


class AbstractController(ABC):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def get_view(self) -> AbstractView:
        """
        :return AbstractView: This device's view object.
        """
        return self.view

    # TODO: Change this to async? Could await all cleanup calls in app_model in this case.
    @abstractmethod
    async def cleanup(self) -> None:
        """
        Handle cleanup and shut down of this code.
        :return: None.
        """
        pass

    def get_conn(self) -> AioSerial:
        """
        Return this device's com port if it exists.
        :return: This device's com port.
        """
        pass

    @abstractmethod
    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this device's language.
        :param lang: The enum for the language.
        :return: None.
        """
        pass

    def create_exp(self, path: str) -> None:
        """
        Set the current experiment save directory for this device if this device needs to save data to file.
        Logic for if this device needs to know about when an experiment is created.
        :return: None.
        """
        pass

    def end_exp(self) -> None:
        """
        Logic for if this device needs to know about when an experiment is ended.
        :return: None.
        """
        pass

    def start_exp(self) -> None:
        """
        Logic for if this device needs to know about when an experiment is running.
        :return: None.
        """
        pass

    def stop_exp(self) -> None:
        """
        Logic for if this device needs to know about when an experiment is stopped.
        :return: None.
        """
        pass
