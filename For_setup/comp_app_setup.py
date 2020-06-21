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

import pathlib
import sys
import os
from cx_Freeze import setup, Executable
# EDIT THESE VARIABLES AS NEEDED.
##########################################################################
builds_path = 'C:/RSDev/Builds/'  # Set to your Builds folder.
sys.path.append("C:/RSDev/asyncCompanion/")  # Set to your asyncCompanion folder.
##########################################################################
from RSCompanionAsync.Model.app_defs import current_version


# Version number.
app_version = str(current_version)
# Output path.
app_v_maj, app_v_min = app_version.split('.')
out_path = builds_path + 'Version ' + app_v_maj + '/Build ' + app_v_maj + '.' + app_v_min + '/RSCompanion/'
# Ensure output path exists.
pathlib.Path(out_path).mkdir(parents=True, exist_ok=True)
# App information.
app_name = 'RS Companion'
exe_name = 'RSCompanion.exe'
app_description = app_name
# Paths to different components of app required for building.
root_path = 'C:/RSDev/'
redist_path = root_path + 'redist/'
proj_path = root_path + 'asyncCompanion/'
package_path = proj_path + 'RSCompanionAsync/'
readme_path = proj_path + 'readme/'
images_path = package_path + 'Resources/Images/'
icon_path = images_path + 'rs_icon.ico'
main_path = package_path + 'main.py'

# Ensure path has project path to allow cx_freeze to add specified app packages.
sys.path.append(proj_path)

# Explicitly list required packages/files for cx_freeze to add/ignore and set output path.
build_exe_options = {'packages': ['os',
                                  'requests',
                                  'queue',
                                  'idna.idnadata',
                                  'urllib3',
                                  'numpy',
                                  'matplotlib',
                                  'Pyside2',
                                  'RSCompanionAsync',
                                  ],
                     'excludes': ['tkinter',
                                  'PyQt5',
                                  ],
                     'include_files': [redist_path,
                                       images_path,
                                       readme_path],
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
      version=app_version,
      description=app_description,
      options={'build_exe': build_exe_options},
      executables=[Executable(main_path, targetName=exe_name, base=base, icon=icon_path)])
