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


profile = {"DRT": {"vid": 9114, "pid": 32798}}

config_fields = ['lowerISI', 'upperISI', 'stimDur', 'intensity']
output_fields = ['startMillis', 'trial', 'clicks', 'rt']
save_fields = ['trial', 'clicks', 'startMillis', 'rt']
ui_fields = ['Mills from block start', 'probe #', 'clicks', 'response time']

iso_standards = {'upperISI': 5000, 'lowerISI': 3000, 'intensity': 255, 'stimDur': 1000}

# drt v1.0 uses uint16_t for drt value storage
max_val = 65535

# All the following drt values must be between 0 and drt_max_val
intensity_max = 255
intensity_min = 0

duration_max = max_val
duration_min = 0

ISI_max = max_val
ISI_min = 0
