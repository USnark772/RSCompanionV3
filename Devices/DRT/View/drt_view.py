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

from Devices.AbstractDevice.View.abstract_view import AbstractView


class DRTView(AbstractView):
    def __init__(self, parent, name):
        super().__init__(parent, name)

    def set_stim_dur_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """

    def set_stim_int_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """

    def set_upper_isi_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """

    def set_lower_isi_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """

    def get_stim_dur(self):
        """

        :return:
        """

    def set_stim_dur(self) -> None:
        """

        :return:
        """

    def set_stim_dur_err(self) -> None:
        """

        :return:
        """

    def get_stim_intens(self):
        """

        :return:
        """

    def set_stim_intens(self) -> None:
        """

        :return:
        """

    def set_stim_intens_err(self) -> None:
        """

        :return:
        """

    def get_upper_isi(self):
        """

        :return:
        """

    def set_upper_isi(self) -> None:
        """

        :return:
        """

    def set_upper_isi_err(self) -> None:
        """

        :return:
        """

    def get_lower_isi(self):
        """

        :return:
        """

    def set_lower_isi(self) -> None:
        """

        :return:
        """

    def set_lower_isi_err(self) -> None:
        """

        :return:
        """

    def get_upload_button(self):
        """

        :return:
        """

    def set_upload_button(self) -> None:
        """

        :return:
        """
