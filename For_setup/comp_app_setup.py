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
Date: 2019 - 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""

import sys
import os
from pathlib import Path
from shutil import rmtree
from cx_Freeze import setup, Executable

# ************************************************* EDIT AS NEEDED *****************************************************
root_dir = 'C:/RSDev/'  # Point to parent dir of project dir.
builds_dir = root_dir + 'Builds/'
# **********************************************************************************************************************


def check_path(path: str, check_for: str = None, check_as_dir: bool = True) -> None:
    """
    Check if path is a directory and check if check_for is in that directory.
    Raise exceptions if tests do not pass.
    :param path: The directory to check and search in.
    :param check_for: The item to search for.
    :param check_as_dir: Check check_for as a directory.
    :return None:
    """
    if not os.path.isdir(path):
        raise Exception(path + " is not a valid directory")
    if check_for is not None:
        if check_for not in os.listdir(path):
            raise Exception(check_for + " not found in:" + path)
        if check_as_dir:
            if not os.path.isdir(path + check_for):
                raise Exception(path + " is not a valid directory")


# Check if root_dir exists.
check_path(root_dir)

# Check if project dir exists.
proj_name = 'asyncCompanion'
check_path(root_dir, proj_name)
proj_dir = root_dir + proj_name + '/'

# Get access to app version number.
sys.path.append(proj_dir)  # Set to your asyncCompanion folder.
from RSCompanionAsync.Model.app_defs import version_number

# App info.
app_name = 'RS Companion'
exe_name = 'RSCompanion.exe'
app_description = app_name

# Check if vc redist exists.
redist = 'redist'
check_path(root_dir, redist)
redist_dir = root_dir + redist + '/'
redist_filename = 'VC_redist.x64.exe'
check_path(redist_dir, redist_filename, False)

# Check if readme dir exists.
readme_dir = proj_dir + 'readme/'

# Initialize rest of paths required for building.
proj_packages_dir = proj_dir + 'RSCompanionAsync/'
main_path = proj_packages_dir + 'main.py'
images_dir = proj_packages_dir + 'Resources/Images/'
icon_path = images_dir + 'rs_icon.ico'

# Version number.
app_v_num = str(version_number)

# Output path.
app_v_maj, app_v_min = app_v_num.split('.')
out_path = builds_dir + 'Version ' + app_v_maj + '/Build ' + app_v_maj + '.' + app_v_min + '/RSCompanion/'

# Ensure output path exists.
if Path(out_path).exists():
    rmtree(out_path)
tries = 0
while tries < 30:
    try:
        Path(out_path).mkdir(parents=True)
        break
    except PermissionError as pe:
        tries += 1
        pass

# Ensure path has project path to allow cx_freeze to add specified app packages.
sys.path.append(proj_dir)

# Explicitly list required packages/files for cx_freeze to add/ignore and set output path.
build_exe_options = {'packages': ['os',
                                  'requests',
                                  'queue',
                                  'idna.idnadata',
                                  'urllib3',
                                  'numpy',
                                  'matplotlib',
                                  'mpl_toolkits',  # Requires __init__.py in mpl_toolkits folder to import this package.
                                  'PySide2',
                                  'aioserial',
                                  'asyncqt',
                                  'certifi',
                                  'chardet',
                                  'cycler',
                                  'kiwisolver',
                                  'cv2',
                                  'pyparsing',
                                  'serial',
                                  'shiboken2',
                                  'six',
                                  'RSCompanionAsync',
                                  ],
                     'excludes': ['tkinter',
                                  'PyQt5',
                                  ],
                     'include_files': [redist_dir+redist_filename,
                                       images_dir,
                                       readme_dir],
                     'build_exe': out_path}

# Add required .dll files. if needed.
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1.dll'),
                 os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1.dll')]

# Set base platform (OS) and include required files.
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    for file in include_files:
        build_exe_options['include_files'].append(file)

# Run setup.
setup(name=app_name,
      version=app_v_num,
      description=app_description,
      options={'build_exe': build_exe_options},
      executables=[Executable(main_path, targetName=exe_name, base=base, icon=icon_path)])
