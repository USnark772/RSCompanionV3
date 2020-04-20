import cv2
import time
import queue
import asyncio
from multiprocessing import Value, Pipe


class cameras:
    def __init__(self, pipe, stop_flag, cam_n, frame_skip):
        self.pipe = pipe
        self.stop_flag = stop_flag

        # Vid cap
        self.cap = cv2.VideoCapture(cam_n, cv2.CAP_DSHOW)
        self.frame_num = 0
        self.frame_skip = frame_skip

        # Vid Saver
        path = 'output.avi'
        self.fps = 30.0 / self.frame_skip
        dims = int(self.cap.get(3)), int(self.cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(path, fourcc, self.fps, dims)
        self.q = queue.SimpleQueue()

        # Async loops
        asyncio.run(self.run_async_tasks())

    async def run_async_tasks(self):
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, self.read_frames)
        asyncio.create_task(self.frame_write_send())
        await self.killer()

    async def frame_write_send(self):
        while not self.stop_flag.value:
            if not self.q.empty():
                frame = self.q.get()
                self.frame_num += 1
                if self.frame_num % self.frame_skip == 0:
                    self.pipe.send(frame)
                    self.out.write(frame)
            await asyncio.sleep(0.005)

    def read_frames(self):
        while not self.stop_flag.value:
            f, frame = self.cap.read()
            self.q.put(frame)
            time.sleep(.001)

    async def killer(self):
        while not self.stop_flag.value:
            await asyncio.sleep(.1)
        await asyncio.sleep(self.fps/1000 * 3)
        self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
