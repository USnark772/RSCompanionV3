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

profile = {"VOG": {"vid": 5824, "pid": 1155}}

config_fields = []
output_field = ['trialCounter', 'millis_openElapsed', 'millis_closeElapsed']
ui_fields = ['block #', 'Total millis open', 'Total millis closed']

max_val = 2147483647

max_open_close = max_val
min_open_close = 0

debounce_max = 100
debounce_min = 0

button_mode = 0
