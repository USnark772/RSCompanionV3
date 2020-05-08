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
Date: 2019 - 2020
Project: Companion App
Company: Red Scientific
https://redscientific.com/index.html
"""


from logging import getLogger, StreamHandler
from urllib3 import PoolManager
from Model.app_defs import version_url, current_version


class VersionChecker:
    """
    Checks version number against latest version from the site
    """

    def __init__(self, log_handlers: [StreamHandler]):
        """
        Initialize the version checker
        :return None:
        """
        self.logger = getLogger(__name__)
        for h in log_handlers:
            self.logger.addHandler(h)
        self.logger.debug("Initializing")
        self.latest_version = self.get_latest_version()
        self.logger.debug("Initialized")

    def check_version(self) -> int:
        """
        Compare version numbers.
        :return int:
            return -1 if unable to get the latest version
            return 1 if the latest version is newer than the app current version
            return 0 otherwise
        """
        self.logger.debug("running")
        if self.latest_version < 0:
            self.logger.debug("done")
            return -1
        elif self.latest_version > current_version:
            self.logger.debug("done")
            return 1
        self.logger.debug("done")
        return 0

    # TODO: Figure out if urllib3 is blocking. Check out https://docs.aiohttp.org/en/stable/ for ideas.
    #  This is probably overkill since this function is only called once at app startup.
    def get_latest_version(self) -> float:
        """
        Connect to site at version_url and retrieve latest version number.
        :return float:
            return -1.0 if unable to get version
            return version number otherwise
        """
        self.logger.debug("running")
        mgr = PoolManager()
        try:
            r = mgr.request("GET", version_url)
        except Exception:
            self.logger.exception("failed, could not connect to url")
            return -1.0
        data = str(r.data)
        if "Companion App Version:" in data:
            latest_version = data[data.index(":") + 1:].rstrip("\\n'")
            self.logger.debug("done, found version")
            return float(latest_version)
        self.logger.debug("done, didn't find version")
        return -1.0
