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

import os
import tempfile
from io import TextIOWrapper
from logging import getLogger, StreamHandler
from operator import itemgetter
from pathlib import Path
from shutil import move
from RSCompanionAsync.Resources.Strings.file_saver_strings import strings, StringsEnum, LangEnum

"""
Take two directories, manipulate all data inside first directory as needed, then move to second directory.
"""


app_data_names = ["flags", "notes", "events"]
data_ft = ".csv"
unsc_sep = "_"
comma_sep = ", "
new_line = "\n"


class RSSaver:
    def __init__(self, lang: LangEnum, log_handlers: [StreamHandler] = None):
        self._logger = getLogger(__name__)
        if log_handlers:
            for h in log_handlers:
                self._logger.addHandler(h)
        self._logger.debug("Initializing")
        self._to_dir = str()
        self._from_dir = None
        self._exp_name = str()
        self._strings = strings[lang]
        self._logger.debug("Initialized")

    def start(self, to_dir: str) -> str:
        """
        Take a directory path, give back a temp directory path.
        :param to_dir: The desired output path.
        :return str: The temporary directory to save data to before calling stop().
        """
        self._logger.debug("running")
        self._to_dir = to_dir
        self._from_dir = tempfile.TemporaryDirectory()
        self._exp_name = to_dir[to_dir.rindex("/") + 1:]
        self._logger.debug("done")
        return self._from_dir.name + "/"

    def stop(self) -> bool:
        """
        Save data saved in temp directory into desired output path.
        :return bool: Whether saving was successful.
        """
        self._logger.debug("running")
        if self._from_dir is None:
            self._logger.debug("done with False")
            return False
        self._finalize_data_output()
        self._move_non_csv_to_out_dir()
        self._from_dir.cleanup()
        self._logger.debug("done with True")
        return True

    def set_lang(self, lang: LangEnum):
        """
        Set the language for output from this module.
        :param lang: The new language to use.
        :return None:
        """
        self._logger.debug("running")
        self._strings = strings[lang]
        self._logger.debug("done")

    def _move_non_csv_to_out_dir(self) -> None:
        """
        Move data from self._from_dir into self._to_dir.
        :return None:
        """
        self._logger.debug("running")
        Path(self._to_dir).mkdir(parents=True, exist_ok=True)
        # with zipfile.ZipFile(self._save_path, "w") as zipper:
        #     for file in os.listdir(self._temp_folder.name):
        #         zipper.write(self._temp_folder.name + "/" + file, file)
        if not os.path.isdir(self._to_dir):
            os.mkdir(self._to_dir)
        prev_dir = os.getcwd()
        os.chdir(self._from_dir.name)
        for file in os.listdir():
            if not file.endswith(data_ft):
                move(file, self._to_dir)
        os.chdir(prev_dir)
        self._logger.debug("done")

    def _finalize_data_output(self) -> None:
        """
        Alter data as desired.
        :return None:
        """
        self._logger.debug("running")
        data: dict = self._parse_experiment()
        self._make_master_files(data)
        self._logger.debug("done")

    def _make_master_files(self, data: dict) -> None:
        """
        Create master output files for each device, add in all flags, notes and events in order of timestamp.
        :param data: The parsed output data from each device and other .csv output files.
        :return None:
        """
        self._logger.debug("running")
        flag = str()
        blk_num = str()
        cond_name = str()
        Path(self._to_dir).mkdir(parents=True, exist_ok=True)
        prev_dir = os.getcwd()
        os.chdir(self._to_dir)
        self._open_master_output_files(data)
        while len(data[app_data_names[2]][1]) > 0:
            next_key = self._calc_next_item(data)
            hdr = data[next_key][0]
            row = data[next_key][1].pop(0)
            if next_key == app_data_names[0]:  # Flag
                flag = row[-1]
                line1 = comma_sep.join([self._strings[StringsEnum.FLAG], cond_name,
                                        row[hdr[self._strings[StringsEnum.TSTAMP_HDR]]], blk_num])
                line2 = comma_sep.join([comma_sep.join(row[hdr[self._strings[StringsEnum.TSTAMP_HDR]] + 1:]), ""])
                self._write_to_all_dev_files(data, line1, line2)
            elif next_key == app_data_names[1]:  # Note
                line1 = comma_sep.join([self._strings[StringsEnum.NOTE], cond_name,
                                        row[hdr[self._strings[StringsEnum.TSTAMP_HDR]]], blk_num])
                line2 = comma_sep.join([flag, comma_sep.join(row[hdr[self._strings[StringsEnum.TSTAMP_HDR]] + 1:])])
                self._write_to_all_dev_files(data, line1, line2)
            elif next_key == app_data_names[2]:  # Event
                cond_name = row[2]
                blk_num = row[3]
                line1 = comma_sep.join([self._strings[StringsEnum.EVENT], cond_name,
                                        row[hdr[self._strings[StringsEnum.TSTAMP_HDR]]], blk_num])
                line2 = comma_sep.join([flag, row[1]])
                self._write_to_all_dev_files(data, line1, line2)
            else:
                line = comma_sep.join([row[0], cond_name, row[hdr[self._strings[StringsEnum.TSTAMP_HDR]]], blk_num,
                                       comma_sep.join(row[hdr[self._strings[StringsEnum.TSTAMP_HDR]] + 1:]), flag, ""])
                data[next_key][3].write(line + new_line)
        self._close_master_output_files(data)
        os.chdir(prev_dir)
        self._logger.debug("done")

    def _open_master_output_files(self, data: dict) -> None:
        """
        Open data_ft type output files for each data type.
        :param data: The dict containing all data types that will contain open output files for each data type.
        :return None:
        """
        for key in data.keys():
            if key not in app_data_names:
                data[key].append(open(key + unsc_sep + self._exp_name + data_ft, "w"))
                hdr_list = list()
                for dkey, dval in data[key][0].items():
                    hdr_list.append((dkey, dval))
                hdr_list = sorted(hdr_list, key=itemgetter(1))
                hdr_list = hdr_list[2:]
                hdr_list = [x[0] for x in hdr_list]
                hdr = comma_sep.join([self._strings[StringsEnum.HDR_1], comma_sep.join(hdr_list),
                                      self._strings[StringsEnum.HDR_2]])
                data[key][-1].write(hdr + new_line)

    @staticmethod
    def _close_master_output_files(data: dict) -> None:
        """
        Close all master output files in data dictionary.
        :param data: The data dict containing open output files.
        :return None:
        """
        for key in data.keys():
            if key not in app_data_names:
                file: TextIOWrapper = data[key][3]
                file.close()

    @staticmethod
    def _write_to_all_dev_files(data: dict, line1: str, line2: str) -> None:
        """
        Concat line1, appropriate comma sep, and line2 and write to each device master output file.
        :param data: refernece to each device output file and appropriate comma sep stored in dictionary.
        :param line1: first line to concat.
        :param line2: second line to concat.
        :return None:
        """
        for key in data.keys():
            if key not in app_data_names:
                data[key][3].write(line1 + comma_sep * data[key][2] + line2 + new_line)

    def _calc_next_item(self, data: dict) -> str:
        """
        Look through and find earliest timestamp using app events file as metric.
        :param data: App and data .csv files as dictionary.
        :return str: The key of the next csv file data to use.
        """
        best = app_data_names[2]
        for key in data.keys():
            # Compare timestamp of best to timestamp of key
            best_ts_index = data[best][0][self._strings[StringsEnum.TSTAMP_HDR]]
            best_array = data[best][1]
            key_ts_index = data[key][0][self._strings[StringsEnum.TSTAMP_HDR]]
            key_array = data[key][1]
            if len(key_array) > 0:
                if best_array[0][best_ts_index] > key_array[0][key_ts_index]:
                    best = key
        return best

    def _parse_experiment(self) -> dict:
        """
        Take all files of type data_ft and parse into dictionary with keys for each type of output and values tuples
        containing string rows from each respective output type.
        :return dict: The parsed data.
        """
        self._logger.debug("running")
        data = dict()
        num_devices = dict()
        prev_dir = os.getcwd()
        os.chdir(self._from_dir.name)
        for file in os.listdir():
            if file.endswith(data_ft):
                info = os.path.splitext(file)[0]
                if unsc_sep in file:
                    info = info.split(unsc_sep)
                else:
                    info = [info, ""]
                if info[0] in app_data_names:  # Type: app output data.
                    hdr, vals, num_col = self._parse_csv_file(file)
                    data[info[0]] = [hdr, vals, num_col]
                else:  # Type: device output data.
                    if info[0] not in num_devices.keys():  # Have not seen this device type yet.
                        num_devices[info[0]] = 0
                    num_devices[info[0]] += 1
                    hdr, vals, num_col = self._parse_csv_file(file, info[0] + unsc_sep + info[1])
                    if info[0] not in data.keys():
                        data[info[0]] = [hdr, [], num_col]
                        for item in vals:
                            data[info[0]][1].append(item)
                    else:
                        for item in vals:
                            data[info[0]][1].append(item)
        os.chdir(prev_dir)
        for data_type in data:
            if data_type in app_data_names:
                continue
            if num_devices[data_type] > 1:
                data[data_type][1] = sorted([row for row in data[data_type][1]],
                                            key=itemgetter(data[data_type][0][self._strings[StringsEnum.TSTAMP_HDR]]))
        self._logger.debug("done")
        return data

    def _parse_csv_file(self, filename: str, dev_id: str = None) -> (dict, list, int):
        """
        Parse rs_companion device output files of type data_ft.
        :param filename: The file to open and parse.
        :param dev_id: Optional device id if the file is a device output file.
        :return tuple: dictionary of hdr:index, list of rows in index order, number of comma_sep required for this
        output file.
        """
        hdr_dict = dict()
        rows = list()
        dev_num_col = 0
        dev = False
        with open(filename) as f:
            hdr = f.readline()
            if dev_id is not None:
                hdr_values = [self._strings[StringsEnum.ID_HDR]]
                more_vals = hdr.rstrip(new_line).split(comma_sep)
                dev_num_col = len(more_vals)
                for x in more_vals:
                    hdr_values.append(x)
                dev = True
            else:
                hdr_values = hdr.rstrip(new_line).split(comma_sep)
            for i in range(len(hdr_values)):
                hdr_dict[hdr_values[i]] = i
            for line in f:
                row = line.rstrip(new_line).split(comma_sep)
                if dev:
                    temp = [dev_id]
                    for item in row:
                        temp.append(item)
                    row = temp
                rows.append(row)
        return hdr_dict, rows, dev_num_col


def main():
    pass
    # exp_dir = "C:/Users/phill/Companion Save Files/experiment_2020-07-20-17-37-51"
    # to_dir = "C:/Users/phill/Companion Save Files/test_exp_edit_out"
    # saver = RSSaver(LangEnum.ENG)
    # saver.start(to_dir)
    # saver._from_dir = exp_dir
    # saver._exp_name = exp_dir[exp_dir.rindex("/") + 1:]
    # saver.stop()


if __name__ == '__main__':
    main()
