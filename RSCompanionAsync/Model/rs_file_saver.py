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
from pathlib import Path
from shutil import move

"""
Take two directories, manipulate all data inside first directory as needed, then move to second directory.
"""


def print_csv_dict(name: str, to_print: dict):
    print(name + ":")
    for key in to_print:
        print(key)
        for item in to_print[key]:
            print("\t" + str(item))


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

    def stop(self) -> bool:
        """
        Save data saved in temporary directory into desired output path.
        :return bool: Whether saving was successful.
        """
        ret = False
        self._alter_data()
        self._move_data_to_output_dir()
        return ret

    def _alter_data(self) -> None:
        """
        Alter data as desired.
        :return None:
        """
        drts = dict()
        vogs = dict()
        flags = dict()
        notes = dict()
        events = dict()
        last_cond_name = str()
        last_block_num = str()
        last_flag = str()
        os.chdir("C:/Users/phill/Companion Save Files/experiment_2020-07-18-14-06-12")
        for file in os.listdir():
            if file.endswith(".csv"):
                print("Looking at file:", file)
                info = file.rstrip(".csv").split("_")
                if info[0] == "flags":
                    pass
                    flags = self._parse_csv_file(file)
                    # print_csv_dict("flags_dict", flags)
                elif info[0] == "notes":
                    pass
                    notes = self._parse_csv_file(file)
                    # print_csv_dict("notes_dict", notes)
                elif info[0] == "times":
                    pass
                    events = self._parse_csv_file(file)
                    # print_csv_dict("events_dict", events)
                elif info[0] == "DRT":
                    temp = self._parse_csv_file(file, info[0] + "_" + info[1])
                    self._merge_dicts(drts, temp)
                    # print_csv_dict("devs_dict", devs)
                elif info[0] == "VOG":
                    temp = self._parse_csv_file(file, info[0] + "_" + info[1])
                    self._merge_dicts(vogs, temp)
        # print_csv_dict("drts_dict", drts)
        # print_csv_dict("vogs_dict", vogs)
        # TODO: Sort arrays in devs based on timestamp array.

    @staticmethod
    def _parse_csv_file(filename: str, dev_id: str = None) -> dict:
        ret = dict()
        dev = False
        with open(filename) as f:
            hdr = f.readline()
            if dev_id is not None:
                hdr_values = ["Device ID"]
                more_vals = hdr.rstrip("\n").split(",")
                for x in more_vals:
                    hdr_values.append(x)
                dev = True
            else:
                hdr_values = hdr.rstrip("\n").split(",")
            print(hdr_values)
            for value in hdr_values:
                ret[value] = list()
            for line in f:
                line_values = line.rstrip("\n").split(",")
                for i in range(len(hdr_values)):
                    if dev and i == 0:
                        ret[hdr_values[i]].append(dev_id)
                    else:
                        ret[hdr_values[i]].append(line_values[i-1])
        return ret

    @staticmethod
    def _merge_dicts(a: dict, b: dict) -> dict:
        """
        Merge dict b into dict a. Assume both dictionaries have same structure or a is empty.
        :param a: The data to add to.
        :param b: The data to add.
        :return dict: The resulting merge.
        """
        ret = dict()
        print("a*********************************\n", a, "\n")
        print("b*********************************\n", b, "\n")
        for key in b:
            ret[key] = b[key]
        print("ret*******************************\n", ret, "\n")
        return ret

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
        cur_dur = os.getcwd()
        os.chdir(self._from_dir.name)
        for file in os.listdir(self._from_dir.name):
            move(file, self._to_dir)
        os.chdir(cur_dur)


def main():
    saver = RSSaver()
    saver._alter_data()


if __name__ == '__main__':
    main()
