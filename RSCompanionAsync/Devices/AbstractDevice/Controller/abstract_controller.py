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
from asyncio import Event, futures
from RSCompanionAsync.Model.app_defs import LangEnum
from aioserial import AioSerial
from RSCompanionAsync.Devices.AbstractDevice.View.abstract_view import AbstractView


class AbstractController(ABC):
    def __init__(self, view=None):
        super().__init__()
        self.view = view
        self.saved = Event()
        self.saved.set()

    def get_view(self) -> AbstractView:
        """
        :return AbstractView: This device's view object.
        """
        return self.view

    @abstractmethod
    async def cleanup(self, discard: bool = False) -> None:
        """
        Handle cleanup and shut down of this code.
        :param discard: Quit without saving.
        :return None:
        """
        pass

    def await_saved(self) -> futures:
        """
        Signal main app that this device data has been saved.
        :return futures: An asyncio awaitable.
        """
        self.saved.set()
        return self.saved.wait()

    def get_conn(self) -> AioSerial:
        """
        Return this device's com port if it exists.
        :return AioSerial: This device's com port.
        """
        pass

    @abstractmethod
    def set_lang(self, lang: LangEnum) -> None:
        """
        Set this device's language.
        :param lang: The enum for the language.
        :return None:
        """
        pass

    # TODO: Change these to async
    def create_exp(self, path: str, cond_name: str) -> None:
        """
        Set the current experiment save directory for this device if this device needs to save data to file.
        Logic for if this device needs to know about when an experiment is created.
        :param path: The path to be used for saving this device's data.
        :param cond_name: The optional condition name for this experiment.
        :return: None.
        """
        pass

    def end_exp(self) -> None:
        """
        Logic for if this device needs to know about when an experiment is ended.
        :return None:
        """
        pass

    def start_exp(self, block_num: int, cond_name: str) -> None:
        """
        Logic for if this device needs to know about when an experiment is running.
        :param block_num: The block number for this part of the experiment.
        :param cond_name: The optional condition name for this experiment.
        :return None:
        """
        pass

    def stop_exp(self) -> None:
        """
        Logic for if this device needs to know about when an experiment is stopped.
        :return None:
        """
        pass

    def update_keyflag(self, flag: str) -> None:
        """
        Logic for if this device needs to know about keflag updates.
        :param flag: The new flag.
        :return None:
        """
        pass

    def update_cond_name(self, name: str) -> None:
        """
        Logic for if this device needs to know about condition name updates.
        :param name: The new condition name.
        :return None:
        """
        pass
