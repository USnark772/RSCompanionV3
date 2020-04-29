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

# TODO: Change this to match drt_strings style.
#################################################################################################################
# general strings
#################################################################################################################

company_name = "Red Scientific"
app_name = "RS Companion"
closing_app_text = "Close RS Companion"
close_confirmation_text = "Are you sure? Any unsaved progress will be lost!"

program_output_hdr = "Timestamp, Author, Location, Message\n"

about_RS_text = "Red Scientific Inc was founded in 2015 by Joel Cooper PhD\n\n" \
                "Contact Information:\n" \
                "joel@redscientific.com\n" \
                "1-801-520-5408"

about_RS_app_text = "- Most things in this app have tooltips. Mouse over different parts to see respective tooltips" \
                    " for more information\n\n" \
                    "Along the top of the app you will find a detachable control bar containing the following:\n" \
                    "- Create button: Create an experiment and choose a location folder for the app to save device" \
                    " data.\n" \
                    "- Play/Pause button: Begin/resume or pause an experiment in progress.\n" \
                    "- Optional condition name: An optional name that will be associated with the newly created" \
                    " experiment.\n\n" \
                    "- Key Flag: Press a letter key at any time to make a quick reference key that will be associated" \
                    " with the data coming in from the Devices during an experiment.\n\n" \
                    "- Note: Enter a note into the box and press Post to apply that note to all device data files" \
                    " within the current experiment.\n\n" \
                    "- Information: Displays information in regards to the current experiment.\n\n" \
                    "The lower left section contains the Display area with the following features:\n" \
                    "- Displays data coming in from Devices associated with the latest experiment.\n" \
                    "- Clicking on the legend will show/hide device specific data in each graph.\n" \
                    "- Using the control bar under each graph you will be able manipulate the graphs.\n\n" \
                    "The lower right section contains the Device config area where each device will display a" \
                    " configuration menu. In each menu you can alter the settings of how the respective device acts" \
                    " during an experiment.\n"

update_available = "An update is available."

up_to_date = "Your program is up to date."

error_checking_for_update = "There was an unexpected error connecting to the repository. Please check" \
                            " https://redscientific.com/downloads.html manually or contact Red Scientific directly."

device_connection_error = "There was a problem connecting the device, please retry connection."

log_version_id = "RS Companion app version: "

#################################################################################################################
# Button box strings
#################################################################################################################

button_box_title = "Experiment"
button_box_create = "Create"
button_box_end = "End"
button_box_create_tooltip = "Create a new experiment"
button_box_end_tooltip = "End experiment"
button_box_start_tooltip = "Begin experiment"
button_box_resume_tooltip = "Resume experiment"
button_box_pause_tooltip = "Pause experiment"
button_box_text_entry_placeholder = "Optional condition name"
button_box_prog_bar_label = "Saving video..."

#################################################################################################################
# Logging strings
#################################################################################################################

log_out_filename = "companion_app_log.txt"
