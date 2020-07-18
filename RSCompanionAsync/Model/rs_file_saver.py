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

import os
import tempfile
from collections import defaultdict
from operator import itemgetter
from pathlib import Path
from shutil import move

"""
Take two directories, manipulate all data inside first directory as needed, then move to second directory.
"""


app_data_names = ["flags", "notes", "times"]
data_filetype = ".csv"
underscore_sep = "_"
comma_sep = ","
new_line = "\n"
ts_hdr_name = 'timestamp'
dev_id_hdr = "device id"


class RSSaver:
    def __init__(self):
        self._to_dir = str()
        self._from_dir = None

    def start(self, to_dir: str) -> str:
        """
        Take a directory path
        :param to_dir: The desired output path.
        :return str: The temporary directory to save data to before calling stop().
        """
        self._to_dir = to_dir
        self._from_dir = tempfile.TemporaryDirectory()
        return self._from_dir.name + "/"

    def stop(self) -> None:
        """
        Save data saved in temporary directory into desired output path.
        :return bool: Whether saving was successful.
        """
        self._finalize_data_output()
        self._move_data_to_output_dir()

    def _move_data_to_output_dir(self) -> None:
        """
        Move data from self._from_dir into self._to_dir.
        :return None:
        """
        Path(self._to_dir).mkdir(parents=True, exist_ok=True)
        # with zipfile.ZipFile(self._save_path, "w") as zipper:
        #     for file in os.listdir(self._temp_folder.name):
        #         zipper.write(self._temp_folder.name + "/" + file, file)
        if not os.path.isdir(self._to_dir):
            os.mkdir(self._to_dir)
        prev_dir = os.getcwd()
        os.chdir(self._from_dir.name)
        for file in os.listdir():
            move(file, self._to_dir)
        os.chdir(prev_dir)

    def _finalize_data_output(self) -> None:
        """
        Alter data as desired.
        :return None:
        """
        data: dict = self._parse_experiment()
        for key in data.keys():
            print("looking at data type: " + key + ".")
            if key in app_data_names:
                print("It's an app data type")
            else:
                print("It's a device.")

    def _parse_experiment(self) -> dict:
        data = dict()
        num_devices = dict()
        prev_dir = os.getcwd()
        os.chdir(self._from_dir)  # TODO: Change this to self._from_dir.name when running with tempfile.
        # os.chdir(self._from_dir.name)
        for file in os.listdir():
            if file.endswith(data_filetype):
                info = file.rstrip(data_filetype).split(underscore_sep)
                if info[0] in app_data_names:
                    hdr, vals = self._parse_csv_file(file)
                    data[info[0]] = [hdr, vals]
                else:
                    if info[0] not in num_devices.keys():
                        num_devices[info[0]] = 0
                    num_devices[info[0]] += 1
                    hdr, vals = self._parse_csv_file(file, info[0] + underscore_sep + info[1])
                    if info[0] not in data.keys():
                        data[info[0]] = [hdr, []]
                        data[info[0]][1].append(vals)
                    else:
                        data[info[0]][1].append(vals)
        os.chdir(prev_dir)
        for data_type in data:
            if data_type in app_data_names:
                continue
            if num_devices[data_type] > 1:
                data[data_type][1] = sorted([row for sublist in data[data_type][1] for row in sublist],
                                            key=itemgetter(data[data_type][0][ts_hdr_name]))
        return data

    @staticmethod
    def _parse_csv_file(filename: str, dev_id: str = None) -> (dict, list):
        hdr_dict = dict()
        rows = list()
        dev = False
        with open(filename) as f:
            hdr = f.readline()
            if dev_id is not None:
                hdr_values = [dev_id_hdr]
                more_vals = hdr.rstrip(new_line).split(comma_sep)
                for x in more_vals:
                    hdr_values.append(x)
                dev = True
            else:
                hdr_values = hdr.rstrip(new_line).split(comma_sep)
            print(hdr_values)
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
        return hdr_dict, rows


def main():
    exp_dir = "C:/Users/phill/Companion Save Files/experiment_2020-07-18-14-06-12"
    saver = RSSaver()
    saver._from_dir = exp_dir
    saver._finalize_data_output()
    # hdr = {app_timestamp_hdr_name: 0, 'data': 1}
    # values = [[(5, 1), (4, 5), (2, 1)], [(3, 2), (2, 1), (8, 4)], [(1, 8), (2, 6), (3, 0)]]
    # the_dictionary = {'DRT': [hdr, values]}
    # print(the_dictionary)
    # for key in the_dictionary:
    #     the_dictionary[key][1] = sorted([row for sublist in the_dictionary[key][1] for row in sublist],
    #                                     key=itemgetter(the_dictionary[key][0][app_timestamp_hdr_name]))
    # print(the_dictionary)


if __name__ == '__main__':
    main()
