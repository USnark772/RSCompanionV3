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
from aioserial import AioSerial
from Devices.AbstractDevice.Model.abstract_model import AbstractModel
from Devices.DRT.Model import drt_defs as defs


class DRTModel(AbstractModel):
    def __init__(self, port: AioSerial, save_dir: str, ch: StreamHandler):
        self._logger = getLogger(__name__)
        self._logger.addHandler(ch)
        self._logger.debug("Initializing")
        super().__init__()
        self._current_vals = [0, 0, 0, 0]
        self._errs = [False, False, False, False]
        self._logger.debug("Initialized")

    def set_current_vals(self, duration, intensity, upper_isi, lower_isi):
        self._current_vals = [duration, intensity, upper_isi, lower_isi]

    def _check_stim_dur_entry(self, entry: str) -> bool:
        self._logger.debug("running")
        if entry.isdigit():
            val = int(entry)
            if defs.duration_max >= val >= defs.duration_min:
                self._logger.debug("done with true")
                return True
        self._logger.debug("done with false")
        return False

    def _check_stim_int_entry(self, entry: str) -> bool:
        self._logger.debug("running")
        self._logger.debug("running")
        if entry.isdigit():
            val = int(entry)
            if defs.intensity_max >= val >= defs.intensity_min:
                self._logger.debug("done with true")
                return True
        self._logger.debug("done with false")
        return False

    def _check_upper_isi_entry(self, upper_entry: str, lower_entry: str) -> (bool, bool):
        self._logger.debug("running")
        if upper_entry.isdigit() and lower_entry.isdigit():
            upper_val = int(upper_entry)
            lower_val = int(lower_entry)
            if defs.ISI_max >= upper_val >= lower_val:
                self._errs[2] = False
                self._changed[2] = upper_val != self._current_vals[2]
        self.tab.set_upper_isi_val_error(self._errs[1])
        if not self._errs[2] and self._errs[3]:
            self._check_lower_isi_val()
        elif self._errs[2] and not self._errs[3]:
            self._check_lower_isi_val()
        self._logger.debug("done")

    def _check_lower_isi_entry(self):
        self._logger.debug("running")
        self._logger.debug("done")
