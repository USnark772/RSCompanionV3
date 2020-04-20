import asyncio
from asyncio import Event
import aioserial
from serial.tools.list_ports import comports
import time

RS_Devices = {"wVOG" : {"vid": 61525, "pid": 38912},
              "DRT" : {"vid": 9114, "pid": 32798},
              "VOG": {"vid": 5824, "pid": 1155},
              "wDRT": {"vid": 23123, "pid": 32421}
              }

class Comports:
    def __init__(self, device_ids):

        self.ports_count = len(comports())

        self.plug_event = Event()
        self.remove_event = Event()

        self.device_ids = device_ids
        self.devices_attached = {}
        self.com_all_attached = []

        self.updated_attached_devices()

        self.loop = asyncio.get_event_loop()
        self.loop.run_in_executor(None, self.scan_for_change)
        self.loop.run_forever()

    def scan_for_change(self):
        while True:
            ports_count = len(comports())
            if ports_count < self.ports_count:
                self.loop.call_soon_threadsafe(self.handle_remove_event)
            elif ports_count > self.ports_count:
                self.loop.call_soon_threadsafe(self.handle_plug_event)
            self.ports_count = ports_count
            time.sleep(.1)

    def handle_plug_event(self):
        self.updated_attached_devices()

    def handle_remove_event(self):
        ports = comports()

        attached = []
        for com in ports:
            attached.append(com.device)

        to_remove = []
        for port in self.devices_attached:
            if port not in attached:
                to_remove.append(port)

        for port in to_remove:
            self.devices_attached.pop(port)

        print(self.devices_attached)

    def updated_attached_devices(self):
        for com in comports():
            for device in self.device_ids:
                if com.vid == self.device_ids[device]['vid'] and com.pid == self.device_ids[device]['pid']:
                    self.devices_attached.update({com.device: {'type': device}})
                    break

        print(self.devices_attached)


Comports(RS_Devices)
