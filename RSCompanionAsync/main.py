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

from sys import argv, exit
from multiprocessing import freeze_support
from os import environ
environ['QT_API'] = 'PySide2'
from asyncio import set_event_loop, run
from asyncqt import QEventLoop
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from RSCompanionAsync.Controller.app_controller import AppController


async def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(argv)
    app_loop = QEventLoop(app)
    set_event_loop(app_loop)
    controller = AppController()  # Need reference else garbage collector has too much fun
    with app_loop:
        exit(app_loop.run_forever())


if __name__ == '__main__':
    freeze_support()
    profile = False  # True: Profile code. False: Run normally.
    if profile:
        import cProfile
        from pstats import Stats, SortKey
        filename = "C:/RSDev/profiler_output/companion_app_profile.stats"
        cProfile.run('run(main())', filename)
        stats = Stats(filename)

        # Pick sorting order for stat output.
        # stats.sort_stats(SortKey.CALLS)  # Sort by total calls to code.
        stats.sort_stats(SortKey.CUMULATIVE)  # Sort by time spent in code.

        # Pick print filter
        stats.print_stats("asyncCompanion")  # Only show project files.
        # stats.print_stats()  # Show all files.
    else:
        run(main())
