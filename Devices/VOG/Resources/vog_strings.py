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

from Model.app_defs import LangEnum
from enum import Enum, auto


# Define enum like this.
class StringsEnum(Enum):
    CUSTOM_LABEL = auto()
    NHTSA_LABEL = auto()
    EBLIND_LABEL = auto()
    DCON_LABEL = auto()
    INF_LABEL = auto()
    CONFIG_TAB_LABEL = auto()
    CONFIG_LABEL = auto()
    UPLOAD_BUTTON_LABEL = auto()
    OPEN_DURATION_LABEL = auto()
    CLOSE_DURATION_LABEL = auto()
    DEBOUNCE_LABEL = auto()
    BUTTON_MODE_LABEL = auto()
    HOLD_VAL_LABEL = auto()
    CLICK_VAL_LABEL = auto()
    TOGGLE_LABEL = auto()
    CONFIG_LABEL_TOOLTIP = auto()
    UPLOAD_BUTTON_TOOLTIP = auto()
    OPEN_DURATION_TOOLTIP = auto()
    CLOSE_DURATION_TOOLTIP = auto()
    DEBOUNCE_TOOLTIP = auto()
    BUTTON_MODE_TOOLTIP = auto()
    HOLD_VAL_TOOLTIP = auto()
    CLICK_VAL_TOOLTIP = auto()
    TOGGLE_TOOLTIP = auto()
    SAVE_HDR = auto()
    PLOT_NAME_OPEN_CLOSE = auto()
    GRAPH_TS = auto()


# Define languages like this.
english = {StringsEnum.CUSTOM_LABEL: "Custom",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "eBlindfold",
           StringsEnum.DCON_LABEL: "Direct Control",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.CONFIG_LABEL: "Current Configuration:",
           StringsEnum.UPLOAD_BUTTON_LABEL: "Upload Settings",
           StringsEnum.OPEN_DURATION_LABEL: "Open Duration",
           StringsEnum.CLOSE_DURATION_LABEL: "Close Duration",
           StringsEnum.DEBOUNCE_LABEL: "Debounce Time",
           StringsEnum.BUTTON_MODE_LABEL: "Button Mode",
           StringsEnum.HOLD_VAL_LABEL: "Hold",
           StringsEnum.CLICK_VAL_LABEL: "Click",
           StringsEnum.TOGGLE_LABEL: "Toggle Lens",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
           StringsEnum.OPEN_DURATION_TOOLTIP: "Set lens open duration.",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "Set lens close duration.",
           StringsEnum.DEBOUNCE_TOOLTIP: "Set Debounce time.",
           StringsEnum.BUTTON_MODE_TOOLTIP: "Set button mode to Click or Hold.",
           StringsEnum.HOLD_VAL_TOOLTIP: "Hold button to toggle lens.",
           StringsEnum.CLICK_VAL_TOOLTIP: "Click button to toggle lens.",
           StringsEnum.TOGGLE_TOOLTIP: "Manually open/close lens.",
           StringsEnum.SAVE_HDR: "timestamp, trial, open, close, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "Time Open/Close",
           StringsEnum.GRAPH_TS: "Timestamp",
           }

# TODO: translate languages
french = {StringsEnum.CUSTOM_LABEL: "Custom",
          StringsEnum.NHTSA_LABEL: "NHTSA",
          StringsEnum.EBLIND_LABEL: "eBlindfold",
          StringsEnum.DCON_LABEL: "Direct Control",
          StringsEnum.INF_LABEL: "INF",
          StringsEnum.CONFIG_TAB_LABEL: "Configuration",
          StringsEnum.CONFIG_LABEL: "Current Configuration",
          StringsEnum.UPLOAD_BUTTON_LABEL: "Upload Settings",
          StringsEnum.OPEN_DURATION_LABEL: "Open Duration",
          StringsEnum.CLOSE_DURATION_LABEL: "Close Duration",
          StringsEnum.DEBOUNCE_LABEL: "Debounce Time",
          StringsEnum.BUTTON_MODE_LABEL: "Button Mode",
          StringsEnum.HOLD_VAL_LABEL: "Hold",
          StringsEnum.CLICK_VAL_LABEL: "Click",
          StringsEnum.TOGGLE_LABEL: "Toggle Lens",
          StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
          StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
          StringsEnum.OPEN_DURATION_TOOLTIP: "Set lens open duration.",
          StringsEnum.CLOSE_DURATION_TOOLTIP: "Set lens close duration.",
          StringsEnum.DEBOUNCE_TOOLTIP: "Set Debounce time.",
          StringsEnum.BUTTON_MODE_TOOLTIP: "Set button mode to Click or Hold.",
          StringsEnum.HOLD_VAL_TOOLTIP: "Hold button to toggle lens.",
          StringsEnum.CLICK_VAL_TOOLTIP: "Click button to toggle lens.",
          StringsEnum.TOGGLE_TOOLTIP: "Manually open/close lens.",
          StringsEnum.SAVE_HDR: "timestamp, trial, open, close, ",
          StringsEnum.PLOT_NAME_OPEN_CLOSE: "Time Open/Close",
          StringsEnum.GRAPH_TS: "Timestamp",
          }

german = {StringsEnum.CUSTOM_LABEL: "Custom",
          StringsEnum.NHTSA_LABEL: "NHTSA",
          StringsEnum.EBLIND_LABEL: "eBlindfold",
          StringsEnum.DCON_LABEL: "Direct Control",
          StringsEnum.INF_LABEL: "INF",
          StringsEnum.CONFIG_TAB_LABEL: "Configuration",
          StringsEnum.CONFIG_LABEL: "Current Configuration",
          StringsEnum.UPLOAD_BUTTON_LABEL: "Upload Settings",
          StringsEnum.OPEN_DURATION_LABEL: "Open Duration",
          StringsEnum.CLOSE_DURATION_LABEL: "Close Duration",
          StringsEnum.DEBOUNCE_LABEL: "Debounce Time",
          StringsEnum.BUTTON_MODE_LABEL: "Button Mode",
          StringsEnum.HOLD_VAL_LABEL: "Hold",
          StringsEnum.CLICK_VAL_LABEL: "Click",
          StringsEnum.TOGGLE_LABEL: "Toggle Lens",
          StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
          StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
          StringsEnum.OPEN_DURATION_TOOLTIP: "Set lens open duration.",
          StringsEnum.CLOSE_DURATION_TOOLTIP: "Set lens close duration.",
          StringsEnum.DEBOUNCE_TOOLTIP: "Set Debounce time.",
          StringsEnum.BUTTON_MODE_TOOLTIP: "Set button mode to Click or Hold.",
          StringsEnum.HOLD_VAL_TOOLTIP: "Hold button to toggle lens.",
          StringsEnum.CLICK_VAL_TOOLTIP: "Click button to toggle lens.",
          StringsEnum.TOGGLE_TOOLTIP: "Manually open/close lens.",
          StringsEnum.SAVE_HDR: "timestamp, trial, open, close, ",
          StringsEnum.PLOT_NAME_OPEN_CLOSE: "Time Open/Close",
          StringsEnum.GRAPH_TS: "Timestamp",
          }

spanish = {StringsEnum.CUSTOM_LABEL: "Custom",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "eBlindfold",
           StringsEnum.DCON_LABEL: "Direct Control",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.CONFIG_LABEL: "Current Configuration",
           StringsEnum.UPLOAD_BUTTON_LABEL: "Upload Settings",
           StringsEnum.OPEN_DURATION_LABEL: "Open Duration",
           StringsEnum.CLOSE_DURATION_LABEL: "Close Duration",
           StringsEnum.DEBOUNCE_LABEL: "Debounce Time",
           StringsEnum.BUTTON_MODE_LABEL: "Button Mode",
           StringsEnum.HOLD_VAL_LABEL: "Hold",
           StringsEnum.CLICK_VAL_LABEL: "Click",
           StringsEnum.TOGGLE_LABEL: "Toggle Lens",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
           StringsEnum.OPEN_DURATION_TOOLTIP: "Set lens open duration.",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "Set lens close duration.",
           StringsEnum.DEBOUNCE_TOOLTIP: "Set Debounce time.",
           StringsEnum.BUTTON_MODE_TOOLTIP: "Set button mode to Click or Hold.",
           StringsEnum.HOLD_VAL_TOOLTIP: "Hold button to toggle lens.",
           StringsEnum.CLICK_VAL_TOOLTIP: "Click button to toggle lens.",
           StringsEnum.TOGGLE_TOOLTIP: "Manually open/close lens.",
           StringsEnum.SAVE_HDR: "timestamp, trial, open, close, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "Time Open/Close",
           StringsEnum.GRAPH_TS: "Timestamp",
           }

chinese = {StringsEnum.CUSTOM_LABEL: "Custom",
           StringsEnum.NHTSA_LABEL: "NHTSA",
           StringsEnum.EBLIND_LABEL: "eBlindfold",
           StringsEnum.DCON_LABEL: "Direct Control",
           StringsEnum.INF_LABEL: "INF",
           StringsEnum.CONFIG_TAB_LABEL: "Configuration",
           StringsEnum.CONFIG_LABEL: "Current Configuration",
           StringsEnum.UPLOAD_BUTTON_LABEL: "Upload Settings",
           StringsEnum.OPEN_DURATION_LABEL: "Open Duration",
           StringsEnum.CLOSE_DURATION_LABEL: "Close Duration",
           StringsEnum.DEBOUNCE_LABEL: "Debounce Time",
           StringsEnum.BUTTON_MODE_LABEL: "Button Mode",
           StringsEnum.HOLD_VAL_LABEL: "Hold",
           StringsEnum.CLICK_VAL_LABEL: "Click",
           StringsEnum.TOGGLE_LABEL: "Toggle Lens",
           StringsEnum.CONFIG_LABEL_TOOLTIP: "Current device configuration",
           StringsEnum.UPLOAD_BUTTON_TOOLTIP: "Upload current configuration to device",
           StringsEnum.OPEN_DURATION_TOOLTIP: "Set lens open duration.",
           StringsEnum.CLOSE_DURATION_TOOLTIP: "Set lens close duration.",
           StringsEnum.DEBOUNCE_TOOLTIP: "Set Debounce time.",
           StringsEnum.BUTTON_MODE_TOOLTIP: "Set button mode to Click or Hold.",
           StringsEnum.HOLD_VAL_TOOLTIP: "Hold button to toggle lens.",
           StringsEnum.CLICK_VAL_TOOLTIP: "Click button to toggle lens.",
           StringsEnum.TOGGLE_TOOLTIP: "Manually open/close lens.",
           StringsEnum.SAVE_HDR: "timestamp, trial, open, close, ",
           StringsEnum.PLOT_NAME_OPEN_CLOSE: "Time Open/Close",
           StringsEnum.GRAPH_TS: "Timestamp",
           }

# Add defined languages to strings dictionary.
strings = {LangEnum.ENG: english,
           LangEnum.FRE: french,
           LangEnum.GER: german,
           LangEnum.SPA: spanish,
           LangEnum.CHI: chinese}
