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

from Model.app_defs import LangEnum
from enum import Enum, auto


class StringsEnum(Enum):
    COMPANY_NAME = auto()
    APP_NAME = auto()
    PROG_OUT_HDR = auto()
    LOG_VER_ID = auto()
    ABOUT_COMPANY = auto()
    ABOUT_APP = auto()
    UPDATE_AVAILABLE = auto()
    NO_UPDATE = auto()
    ERR_UPDATE_CHECK = auto()
    DEV_CON_ERR = auto()
    LOG_OUT_NAME = auto()


company_name = "Red Scientific"
app_name = "RS Companion"
log_out_filename = "companion_app_log.txt"


english = {StringsEnum.COMPANY_NAME: company_name,
           StringsEnum.APP_NAME: app_name,
           StringsEnum.LOG_OUT_NAME: log_out_filename,
           StringsEnum.LOG_VER_ID: company_name + " app version: ",
           StringsEnum.PROG_OUT_HDR: "Timestamp, Author, Location, Message\n",
           StringsEnum.ABOUT_COMPANY: "Red Scientific Inc was founded in 2015 by Joel Cooper PhD\n\n"
                                      " Contact Information:\n"
                                      " joel@redscientific.com\n"
                                      " 1-801-520-5408",
           StringsEnum.ABOUT_APP: "- Most things in this app have tooltips. Mouse over different parts to see"
                                  " respective tooltips for more information\n\n"
                                  " Along the top of the app you will find a control bar containing the following:\n"
                                  " - Create/End button: Create or end an experiment. Choose a location folder for the"
                                  " app to save device data.\n"
                                  " - Play/Pause button: Begin/resume or pause an experiment in progress.\n"
                                  " - Optional condition name: An optional name that will be associated with the newly"
                                  " created experiment.\n\n"
                                  " - Key Flag: Press a letter key at any time to make a quick reference key that will"
                                  " be associated with the data coming in from the Devices during an experiment.\n\n"
                                  " - Note: Enter a note into the box and press Post to apply that note to all device"
                                  " data files within the current experiment.\n\n"
                                  " - Information: Displays information in regards to the current experiment.\n\n"
                                  " - Drive Info: Displays information in regards to the current volume where data is"
                                  " being saved to.",
           StringsEnum.UPDATE_AVAILABLE: "An update is available.",
           StringsEnum.NO_UPDATE: "Your program is up to date.",
           StringsEnum.ERR_UPDATE_CHECK: "There was an unexpected error connecting to the repository. Please check"
                                         " https://redscientific.com/downloads.html manually or contact Red Scientific"
                                         " directly.",
           StringsEnum.DEV_CON_ERR: "There was a problem connecting the device, please retry connection.",
           }

french = english

strings = {LangEnum.ENG: english,
           LangEnum.FRE: french}
