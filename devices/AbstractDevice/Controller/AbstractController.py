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
from Model.app_helpers import NotDefinedException


class ABCDeviceController(ABC):
    def __init__(self):
        self.active = True

    @abstractmethod
    def cleanup(self):
        pass

    def get_name(self):
        raise NotDefinedException("Device controller must implement get_name()")

    def create_new_save_file(self, new_filename):
        pass

    def start_exp(self):
        pass

    def end_exp(self):
        pass

    def start_block(self):
        pass

    def end_block(self):
        pass

    # TODO: Figure out if can pass instead of return ''
    @staticmethod
    def get_save_file_hdr():
        return ''

    # TODO: Figure out if can pass instead of return ''
    @staticmethod
    def get_note_spacer():
        return ''
