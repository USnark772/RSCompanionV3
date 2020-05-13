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


class VOGModel:
    def __init__(self, name: str, conn, log_handlers):
        pass

    def check_current_input(self):
        pass

    @staticmethod
    def __parse_msg(msg_string):
        ret = dict()
        ret['values'] = {}
        if msg_string[0:5] == "data|":
            ret['type'] = "data"
            val_ind_start = 5
            for i in range(len(vog_output_field)):
                val_ind_end = msg_string.find(',', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                ret['values'][vog_output_field[i]] = msg_string[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 1
        elif "config" in msg_string:
            ret['type'] = "settings"
            bar_ind = msg_string.find('|', 6)
            if msg_string[6:bar_ind] == "Name":
                ret['values']['Name'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "MaxOpen":
                ret['values']['MaxOpen'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "MaxClose":
                ret['values']['MaxClose'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "Debounce":
                ret['values']['Debounce'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "ClickMode":
                ret['values']['ClickMode'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
        elif "Click" in msg_string:
            ret['action'] = "Click"
        elif "buttonControl" in msg_string:
            ret['type'] = "settings"
            bar_ind = msg_string.find('|')
            ret['values'] = {}
            ret['values']['buttonControl'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
        elif "peek" in msg_string:
            ret['type'] = "settings"
            ret['values'] = {}
            ret['values']['lensState'] = msg_string.rstrip("\r\n")
        return ret

    @staticmethod
    def __prepare_msg(cmd, arg=None):
        """ Create string using vog syntax. """
        if arg:
            msg_to_send = ">" + cmd + "|" + arg + "<<\n"
        else:
            msg_to_send = ">" + cmd + "|" + "<<\n"
        return msg_to_send
