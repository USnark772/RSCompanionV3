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

from tempfile import gettempdir
from Model.strings_english import program_output_hdr


class AppModel:
    def __init__(self):
        pass

    @staticmethod
    def setup_log_output_file(file_name: str) -> str:
        """
        Create program output file to save log.
        :param file_name: Name of the save log
        :return str: full directory to the save log, including the save log name
        """

        fname = gettempdir() + "\\" + file_name
        with open(fname, "w") as temp:
            temp.write(program_output_hdr)
        return fname
