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
import asyncio
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt


async def test_coroutine(to_test, args):
    test = to_test(*args)
    await asyncio.sleep(2)
    test.cleanup()
    return 0


def test_companion_class(to_test, *args):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(test_coroutine(to_test, args))


# To run test in a particular module, add this code to given file and modify to suit.
# class to test must have cleanup function.
# if __name__ == '__main__':
    # from Tests.test_companion_module import test_companion_class
    # test_companion_class(class_to_test, any_args_required)
