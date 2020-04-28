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

# TODO implement methods called from self
class DRTView(AbstractView):
    def __init__(self, parent, name):
        super().__init__(parent, name)

    def set_stim_dur_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self.logger.debug("running")
        self.stim_dur_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def set_stim_intens_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self.logger.debug("running")
        self.stim_intens_slider.valueChanged.connect(func)
        self.logger.debug("done")

    def set_upper_isi_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self.logger.debug("running")
        self.upper_isi_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def set_lower_isi_entry_changed_handler(self, func: classmethod) -> None:
        """

        :param func:
        :return:
        """
        self.logger.debug("running")
        self.lower_isi_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def get_stim_dur(self):
        """

        :return:
        """
        return self.stim_dur_line_edit.text()

    def set_stim_dur(self, val) -> None:
        """
        Set display value of stim duration
        :param val:
        :return:
        """
        self.logger.debug("running")
        self.stim_dur_line_edit.setText(str(val))
        self.logger.debug("done")

    def set_stim_dur_err(self, is_error) -> None:
        """
        Set display of error in stim duration
        :param is_error:
        :return:
        """
        self.logger.debug("running")
        if is_error:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def get_stim_intens(self):
        """

        :return:
        """
        return self.stim_intens_slider.value()

    def set_stim_intens(self, val) -> None:
        """
        Set display value of stim intensity
        :param val:
        :return:
        """
        self.logger.debug("running")
        self.stim_intens_slider.setValue(int(val))
        self.set_stim_intens_val_label(val)
        self.logger.debug("done")

    def set_stim_intens_err(self) -> None:
        """

        :return:
        """

    def get_upper_isi(self):
        """

        :return:
        """
        return self.upper_isi_line_edit.text()

    def set_upper_isi(self, val) -> None:
        """
        Set display value of upper isi
        :param val:
        :return:
        """
        self.logger.debug("running")
        self.upper_isi_line_edit.setText(str(val))
        self.logger.debug("done")

    def set_upper_isi_err(self, is_error) -> None:
        """
        Set display of error in upper isi line edit
        :param is_error:
        :return:
        """
        self.logger.debug("running")
        if is_error:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def get_lower_isi(self):
        """

        :return:
        """
        return self.lower_isi_line_edit.text()

    def set_lower_isi(self, val) -> None:
        """
        Set display value of lower isi
        :param val:
        :return:
        """
        self.logger.debug("running")
        self.lower_isi_line_edit.setText(str(val))
        self.logger.debug("done")

    def set_lower_isi_err(self, is_error) -> None:
        """
        Set display of error in lower isi line edit
        :param is_error:
        :return:
        """
        self.logger.debug("running")
        if is_error:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def set_upload_button(self, is_active) -> None:
        """

        :return:
        """
        self.logger.debug("running")
        self.upload_settings_button.setEnabled(is_active)
        self.logger.debug("done")
