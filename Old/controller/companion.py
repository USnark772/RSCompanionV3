from PySide2.QtWidgets import QApplication
from Old.view.mainwin import MainWindow
from asyncqt import QEventLoop
from Old.devices.template import cameras

from Old.model import com_connect

from multiprocessing import Value, Process, Pipe

import sys
import asyncio

# TODO: Separate these defs into device folders.
RS_Devices = {"DRT": {"vid": 9114, "pid": 32798},
              "wDRT": {"vid": 23123, "pid": 32421},
              "VOG": {"vid": 5824, "pid": 1155},
              "wVOG": {"vid": 61525, "pid": 38912}
              }


# TODO: Implement device manager.
# TODO: Implement camera manager.


class MainController:
    def __init__(self):
        # QT
        app = QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)
        self.running = True
        # com
        self.com_plug_event = asyncio.Event()
        self.com = com_connect.Comports(RS_Devices, self.com_plug_event)
        asyncio.create_task(self.comport_cb())

        # processes
        self.stop_flag = Value('i', 0)
        self.par_p, self.chi_p = Pipe()
        c = Process(target=cameras.Cameras, args=(self.chi_p, self.stop_flag, 0, 1))
        c.start()

        # loops
        self.duration = 4
        self.value = 0

        self.close_event = asyncio.Event()
        self.mw = MainWindow(self.close_event)
        self.mw.show()
        asyncio.create_task(self.handle_close_event())

        # --tasks
        asyncio.create_task(self.handle_frames())
        # asyncio.create_task(self.send_stop())

        # loops here...
        with loop:
            sys.exit(loop.run_forever())

    async def comport_cb(self):
        while self.running:
            await self.com_plug_event.wait()
            self.com_plug_event.clear()
            print(self.com.attached)

    async def handle_close_event(self):
        while self.running:
            await self.close_event.wait()
            self.par_p.send("msg")
            self.running = False
            self.com.cleanup()
            await self.pipe_reader()
            await self.cleanup()

    async def pipe_reader(self):
        while not self.par_p.poll():
            await asyncio.sleep(0.1)
        msg = self.par_p.recv()
        while self.par_p.poll() and not type(msg) == str():
            print("Not string, getting next msg from pipe.")
            msg = self.par_p.recv()
        print(type(msg))
        return msg == "done closing"

    @staticmethod
    async def cleanup():
        loop = asyncio.get_event_loop()
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.gather(*tasks)
        loop.stop()

    async def scale_video_win(self):
        while self.running:
            print(self)
            await asyncio.sleep(.01)

    async def handle_frames(self):
        while self.running:
            if self.par_p.poll():
                image = self.par_p.recv()
                self.mw.mdi_win.display(image)
            await asyncio.sleep(.01)

    def new_experiment(self):
        print("Starting new experiment")
