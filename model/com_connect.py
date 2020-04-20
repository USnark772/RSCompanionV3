import asyncio
import aioserial
from serial.tools.list_ports import comports
import time


class Comports:
    def __init__(self, device_ids, event_callback: asyncio.Event):
        self.event_callback = event_callback
        self.attached = {}

        self._ports_count = len(comports())
        self._device_ids = device_ids
        self._update_attached_devices()

        self.loop = asyncio.get_running_loop()

    async def run(self):
        self.loop.run_in_executor(None, self._scan_for_change)
        self.loop.create_task(self.read_ports())

    async def read_ports(self):
        for ports in self.attached:
            if not self.attached[ports]['reply']:
                self.attached[ports]['reply'] = self.loop.create_task(self.attached[ports]['conn'].read_async())
                print(self.attached[ports]['reply'])

    def _scan_for_change(self):
        while True:
            ports_count = len(comports())
            if ports_count != self._ports_count:
                if ports_count < self._ports_count:
                    self.loop.call_soon_threadsafe(self._remove_event)
                elif ports_count > self._ports_count:
                    self.loop.call_soon_threadsafe(self._plug_event)
            self._ports_count = ports_count

            time.sleep(.1)

    def _plug_event(self):
        self._update_attached_devices()
        self.event_callback.set()

    def _remove_event(self):
        ports = comports()

        attached = []
        for com in ports:
            attached.append(com.device)

        to_remove = []
        for port in self.attached:
            if port not in attached:
                to_remove.append(port)

        for port in to_remove:
            self.attached[port]['conn'].close()
            self.attached.pop(port)

        self.event_callback.set()

    def _update_attached_devices(self):
        for com in comports():
            if com.device not in self.attached.keys():
                for device in self._device_ids:
                    if com.vid == self._device_ids[device]['vid'] and com.pid == self._device_ids[device]['pid']:
                        connection = aioserial.AioSerial(com.device)
                        self.attached.update({com.device: {'type': device, 'conn': connection}})
                        break
