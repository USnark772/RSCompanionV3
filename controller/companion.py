from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QPixmap, QImage
from view.mainwin import MainWindow
from asyncqt import QEventLoop
from devices.template import cameras

from model import com_connect

from multiprocessing import Value, Process, Pool, Pipe

import concurrent.futures
import sys
import asyncio


import cv2

import time

import numpy as np

RS_Devices = {"wVOG" : {"vid": 61525, "pid": 38912},
              "DRT" : {"vid": 9114, "pid": 32798},
              "VOG": {"vid": 5824, "pid": 1155},
              "wDRT": {"vid": 23123, "pid": 32421}
              }


class MainController:
    def __init__(self):

        # QT
        app = QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        # com
        self.com_plug_event = asyncio.Event()
        self.com = com_connect.Comports(RS_Devices, self.com_plug_event)
        asyncio.create_task(self.com.run())
        asyncio.create_task(self.comport_cb())

        # processes
        self.stop_flag = Value('i', 0)
        self.par_p, self.chi_p = Pipe()
        c = Process(target=cameras.cameras,
                    args=(self.chi_p, self.stop_flag, 0, 1))
        c.start()

        # loops
        self.duration = 4
        self.value = 0

        self.mw = MainWindow()
        self.mw.show()

        # --tasks
        asyncio.create_task(self.handle_frames())

        asyncio.create_task(self.send_stop())


        # loops here...
        with loop:
            sys.exit(loop.run_forever())

    async def comport_cb(self):
        while True:
            await self.com_plug_event.wait()
            self.com_plug_event.clear()

            print(self.com.attached)

    async def send_stop(self):
        await asyncio.sleep(5500)
        self.stop_flag.value = 1

    async def scale_video_win(self):
        while True:
            print(self)

            await asyncio.sleep(.01)

    async def handle_frames(self):
        while True:
            if self.par_p.poll():
                image = self.par_p.recv()

                self.mw.mdi_win.display(image)

            await asyncio.sleep(.01)

    def new_experiment(self):
        print("Starting new experiment")
