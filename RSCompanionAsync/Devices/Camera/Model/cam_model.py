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

# import cProfile
# from Debugging_Profiling.profile_defs import profile_outdir

from time import time, sleep, mktime
from ctypes import c_char
from threading import Lock, Thread
from PIL import ImageFont, ImageDraw, Image
from numpy import frombuffer, copyto, asarray, uint8
from collections import deque
from textwrap import shorten
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from asyncio import create_task, Event, sleep as asyncsleep, set_event_loop, new_event_loop, get_event_loop
from multiprocessing.connection import Connection
from multiprocessing import Array, Semaphore
from cv2 import resize, INTER_AREA
from queue import SimpleQueue
from RSCompanionAsync.Model.app_helpers import format_current_time
from RSCompanionAsync.Devices.Camera.Model import cam_defs as defs
from RSCompanionAsync.Devices.Camera.Model.cam_stream_reader import StreamReader
from RSCompanionAsync.Devices.Camera.Model.cam_stream_writer import StreamWriter
from RSCompanionAsync.Devices.Camera.Model.cam_size_getter import SizeGetter
from RSCompanionAsync.Devices.Camera.Resources.cam_strings import LangEnum, strings, StringsEnum


ENCODE_CODE = "utf-8"
CM_SEP = ","
DTYPE = uint8
COND_NAME_WIDTH = 30
BYTESTR_SIZE = 64
OVL_POS = (6, 3)
OVL_FONT = ImageFont.truetype("simsun.ttc", 18)
EDIT_HEIGHT = 22
r = 211
g = 250
b = 10
OVL_CLR = (b, g, r)


class FPSTracker:
    def __init__(self):
        self._lock = Lock()
        self._fps = 0
        self._times = deque()
        self._num_to_keep = 60
        self._sum_times = 0
        self._prev_time = time()

    def update_fps(self, timestamp):
        now = mktime(timestamp.timetuple()) + timestamp.microsecond / 1E6
        diff = now - self._prev_time
        self._times.append(diff)
        self._sum_times += diff
        while len(self._times) > self._num_to_keep:
            self._sum_times -= self._times.popleft()
        self._prev_time = now
        self._fps = round(self._num_to_keep / self._sum_times)

    def get_fps(self) -> int:
        ret = self._fps
        return ret


class CamModel:
    def __init__(self, msg_pipe: Connection, img_pipe: Connection, cam_index: int = 0):
        # cProfile.runctx('self.sec_init(msg_pipe, img_pipe, cam_index)', globals(), locals(),
        #                 profile_outdir + "Cam_%d.prof" % cam_index)
    #
    # def sec_init(self, msg_pipe: Connection, img_pipe: Connection, cam_index: int = 0):
        set_event_loop(new_event_loop())
        self._msg_pipe = msg_pipe
        self._img_pipe = img_pipe
        self._cam_index = cam_index
        self._cam_reader = StreamReader(cam_index)
        self._size_gtr = SizeGetter(self._cam_reader)
        self._stop_event = Event()
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter()
        self._tasks = []
        self._switcher = {defs.ModelEnum.STOP: self._stop_writing,
                          defs.ModelEnum.START: self._start_writing,
                          defs.ModelEnum.SET_USE_CAM: self._use_cam,
                          defs.ModelEnum.SET_USE_FEED: self._use_feed,
                          defs.ModelEnum.CLEANUP: self.cleanup,
                          defs.ModelEnum.INITIALIZE: self.init_cam,
                          defs.ModelEnum.GET_FPS: self._get_fps,
                          defs.ModelEnum.SET_FPS: self._set_fps,
                          defs.ModelEnum.GET_RES: self._get_res,
                          defs.ModelEnum.SET_RES: self._set_res,
                          defs.ModelEnum.COND_NAME: self._update_cond_name,
                          defs.ModelEnum.BLOCK_NUM: self._update_block_num,
                          defs.ModelEnum.KEYFLAG: self._update_keyflag,
                          defs.ModelEnum.EXP_STATUS: self._update_exp_status,
                          defs.ModelEnum.LANGUAGE: self.set_lang,
                          }
        self._running = True
        self._process_imgs = False
        self._writing = False
        self._show_feed = False
        self._frame_size = self._cam_reader.get_resolution()
        self._handle_frames = Event()
        self._loop = get_event_loop()

        self._strings = strings[LangEnum.ENG]
        self._max_fps = 30
        self._fps = self._max_fps
        self._cam_name = "CAM_" + str(self._cam_index)
        self._cond_name = str()
        self._exp_status = self._strings[StringsEnum.EXP_STATUS_STOP]
        self._exp_running = False
        self._block_num = 0
        self._keyflag = str()
        self.set_lang()
        self._fps_tracker = FPSTracker()

        self._num_img_workers = 1
        self._img_workers = list()
        self._sems1 = list()
        self._sems2 = list()
        self._sems3 = list()
        self._shm_ovl_arrs = list()
        self._shm_img_arrs = list()
        self._np_img_arrs = list()
        self._proc_thread = Thread(target=None, args=())
        cur_res = self._cam_reader.get_resolution()
        self._cur_arr_shape = (int(cur_res[1]), int(cur_res[0]), 3)
        self._cur_arr_size = self._cur_arr_shape[0] * self._cur_arr_shape[1] * self._cur_arr_shape[2]
        self._executor = ThreadPoolExecutor()
        self._loop.run_until_complete(self._start_loop())

    async def _handle_pipe(self) -> None:
        """
        Handle msgs from model.
        :return None:
        """
        try:
            while self._running:
                if self._msg_pipe.poll():
                    msg = self._msg_pipe.recv()
                    if msg[0] in self._switcher.keys():
                        if msg[1] is not None:
                            self._switcher[msg[0]](msg[1])
                        else:
                            self._switcher[msg[0]]()
                await asyncsleep(.02)
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass
        except Exception as e:
            raise e

    def cleanup(self, discard: bool) -> None:
        """
        Cleanup this code and prep for app closure.
        :param discard: Quit without saving.
        :return None:
        """
        create_task(self._cleanup(discard))

    def init_cam(self) -> None:
        """
        Begin initializing camera.
        :return None:
        """
        create_task(self._run_tests())

    def set_lang(self, lang: LangEnum = LangEnum.ENG) -> None:
        """
        Set this camera's language.
        :param lang: The new language enum.
        :return None:
        """
        self._strings = strings[lang]
        self._set_texts()

    async def _run_tests(self) -> None:
        """
        Run each camera test in order.
        :return None:
        """
        prog_tracker = create_task(self._monitor_init_progress())
        sizes = await self._size_gtr.get_sizes()
        if len(sizes) < 1:
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))
            prog_tracker.cancel()
            return
        max_fps = await self._cam_reader.calc_max_fps(max(sizes))
        if max_fps < 0:
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))
            prog_tracker.cancel()
            return
        self._max_fps = max_fps
        self._fps = max_fps
        self._msg_pipe.send((defs.ModelEnum.START, (max_fps, sizes)))
        prog_tracker.cancel()
        self._proc_thread = Thread(target=self._start_frame_processing, args=())
        self._proc_thread.start()

    async def _monitor_init_progress(self) -> None:
        """
        Periodically update controller on init progress.
        :return None:
        """
        while True:
            status = (self._cam_reader.get_fps_status() / 2) + (self._size_gtr.status / 2)
            if status >= 100:
                break
            self._msg_pipe.send((defs.ModelEnum.STAT_UPD, status))
            await asyncsleep(.5)

    async def _await_reader_err(self) -> None:
        """
        Handle if reader fails.
        :return None:
        """
        while self._running:
            await self._cam_reader.await_err()
            self._msg_pipe.send((defs.ModelEnum.FAILURE, None))

    async def _cleanup(self, discard: bool) -> None:
        self._running = False
        self._size_gtr.stop()
        self._stop()
        self._cam_reader.cleanup()
        self._cam_writer.cleanup(discard)
        self._msg_pipe.send((defs.ModelEnum.CLEANUP, None))

    def _refresh_np_arrs(self) -> None:
        self._np_img_arrs = list()
        for j in range(self._num_img_workers):
            self._np_img_arrs.append(frombuffer(self._shm_img_arrs[j].get_obj(), count=self._cur_arr_size,
                                                dtype=DTYPE).reshape(self._cur_arr_shape))

    def _update_block_num(self, num: int) -> None:
        """
        Update the block num shown on camera details.
        :param num: The new num to show.
        :return None:
        """
        self._block_num = num

    def _update_cond_name(self, name: str) -> None:
        """
        Update the condition name shown on camera details.
        :param name: The new name to show.
        :return None:
        """
        self._cond_name = name

    def _update_keyflag(self, flag: str) -> None:
        """
        Update the key flag shown on camera details.
        :param flag: The new key flag to show.
        :return None:
        """
        self._keyflag = flag

    def _update_exp_status(self, status: bool) -> None:
        """
        Update the experiment status shown on the camera details.
        :param status: The new status to show.
        :return None:
        """
        self._exp_running = status
        if status:
            self._exp_status = self._strings[StringsEnum.EXP_STATUS_RUN]
        else:
            self._exp_status = self._strings[StringsEnum.EXP_STATUS_STOP]

    def _get_res(self) -> None:
        """
        Send the current resolution of this camera.
        :return None:
        """
        self._msg_pipe.send((defs.ModelEnum.CUR_RES, self._cam_reader.get_resolution()))

    def _set_res(self, new_res: (float, float)) -> None:
        """
        Change the resolution on this camera.
        :param new_res: The new resolution to use.
        :return None:
        """
        if new_res == self._cam_reader.get_resolution():
            print("Same res dummy!")
            return
        self._show_feed = False
        self._cam_reader.stop()
        self._stop_frame_processing()
        self._cam_reader.set_resolution(new_res)
        self._times = deque()
        cur_res = self._cam_reader.get_resolution()
        self._cur_arr_shape = (int(cur_res[1]), int(cur_res[0]), 3)
        self._cur_arr_size = self._cur_arr_shape[0] * self._cur_arr_shape[1] * self._cur_arr_shape[2]
        self._proc_thread = Thread(target=self._start_frame_processing, args=())
        self._cam_reader.start()
        self._proc_thread.start()
        self._show_feed = True

    def _use_cam(self, is_active: bool) -> None:
        """
        Toggle whether this cam is being used.
        :param is_active: Whether this cam is being used.
        :return None:
        """
        if is_active:
            self._cam_reader.start()
            self._handle_frames.set()
        else:
            self._cam_reader.stop()
            self._handle_frames.clear()

    def _use_feed(self, is_active: bool) -> None:
        """
        Toggle whether this cam feed is being passed to the view.
        :param is_active: Whether this cam feed is being passed to the view.
        :return None:
        """
        self._show_feed = is_active

    def _start_writing(self, path: str) -> None:
        """
        Create new writer and set boolean to start putting frames in write queue.
        :return None:
        """
        filename = path + "CAM_" + str(self._cam_index) + "_" + format_current_time(datetime.now(), save=True) + ".avi"
        self._frame_size = self._cam_reader.get_resolution()
        self._frame_size = (int(self._frame_size[0]), int(self._frame_size[1]))
        self._write_q = SimpleQueue()
        self._cam_writer = StreamWriter()
        self._cam_writer.start(filename, int(self._fps), self._frame_size, self._write_q)
        self._writing = True

    def _stop_writing(self) -> None:
        """
        Destroy writer and set boolean to stop putting frames in write queue.
        :return None:
        """
        self._cam_writer.cleanup()
        self._writing = False

    async def signal_done_writing(self) -> None:
        """
        Signal when writer is done writing to file.
        :return None:
        """
        while self._running:
            await self._cam_writer.await_done_writing()
            self._msg_pipe.send((defs.ModelEnum.STOP, None))

    async def _start_loop(self) -> None:
        """
        Run all async tasks in this model and wait for stop signal. (This method is the main loop for this process)
        :return None:
        """
        # TODO: Consider putting these in threads like in cam_controller.
        self._tasks.append(create_task(self._handle_pipe()))
        self._tasks.append(create_task(self._await_reader_err()))
        # self._tasks.append(create_task(self.signal_done_writing()))
        await self._stop_event.wait()

    def _start_frame_processing(self) -> None:
        """
        Create image processing threads and wait for stop signal.
        :return None:
        """
        self._process_imgs = True
        max_res = defs.common_resolutions[-1]
        max_img_arr_shape = (int(max_res[1]), int(max_res[0]), 3)
        max_img_arr_size = max_img_arr_shape[0] * max_img_arr_shape[1] * max_img_arr_shape[2]
        self._img_workers = list()
        self._sems1 = list()
        self._sems2 = list()
        self._sems3 = list()
        self._shm_ovl_arrs = list()
        self._shm_img_arrs = list()
        self._np_img_arrs = list()
        for i in range(self._num_img_workers):
            self._sems1.append(Semaphore(0))
            self._sems2.append(Semaphore(0))
            self._sems3.append(Semaphore(1))
            self._shm_ovl_arrs.append(Array(c_char, BYTESTR_SIZE))
            self._shm_img_arrs.append(Array('Q', max_img_arr_size))
            worker_args = (self._shm_img_arrs[i], self._sems1[i], self._sems2[i], self._shm_ovl_arrs[i])
            # TODO: Figure out why this wont work.
            # self._img_workers.append(self._loop.run_in_executor(self._executor, self._img_processor, worker_args))
            self._img_workers.append(Thread(target=self._img_processor, args=worker_args, daemon=True))
            self._img_workers[i].start()
        self._refresh_np_arrs()
        self._img_workers.append(Thread(target=self._distribute_frames, args=(), daemon=True))
        self._img_workers[-1].start()
        self._img_workers.append(Thread(target=self._handle_processed_frames, args=(), daemon=True))
        self._img_workers[-1].start()
        while self._process_imgs:
            sleep(1)

    def _stop_frame_processing(self) -> None:
        """
        Stop proc_thread and join it.
        :return None:
        """
        self._process_imgs = False
        self._proc_thread.join()

    def _stop(self) -> None:
        """
        Stop all async tasks.
        :return None:
        """
        for task in self._tasks:
            task.cancel()
        self._process_imgs = False
        self._proc_thread.join()
        self._stop_event.set()

    def _get_fps(self) -> None:
        """
        Send the current fps of this camera.
        :return None:
        """
        self._msg_pipe.send((defs.ModelEnum.CUR_FPS, self._cam_reader.get_fps()))

    def _set_fps(self, new_fps: float) -> None:
        """
        Set new fps and reset fps tracking.
        :param new_fps: The new fps to use.
        :return None:
        """
        self._times = deque()
        self._cam_reader.set_fps(new_fps)
        if new_fps == float("inf"):
            self._fps = self._max_fps
        else:
            self._fps = new_fps

    def _distribute_frames(self) -> None:
        """
        Distribute frames in proper order to image_worker processes.
        :return None:
        """
        i = 0
        while self._process_imgs:
            ret, (frame, timestamp) = self._cam_reader.get_next_new_frame()
            if ret:
                self._fps_tracker.update_fps(timestamp)
                overlay = shorten(self._cond_name, COND_NAME_WIDTH) + CM_SEP + \
                          format_current_time(timestamp, time=True, mil=True) + CM_SEP + self._exp_status + CM_SEP + \
                          str(self._block_num) + CM_SEP + str(self._keyflag) + CM_SEP + str(self._fps_tracker.get_fps())
                self._sems3[i].acquire()
                copyto(self._np_img_arrs[i], frame)
                self._shm_ovl_arrs[i].value = (overlay.encode(ENCODE_CODE))
                self._sems1[i].release()
                i = (i + 1) % self._num_img_workers
            else:
                sleep(.001)

    def _img_processor(self, sh_img_arr: Array, sem1: Semaphore, sem2: Semaphore, ovl_arr: Array) -> None:
        """
        Process images as needed.
        :param sh_img_arr:
        :param sem1:
        :param sem2:
        :param ovl_arr:
        :return:
        """
        img_dim = (EDIT_HEIGHT, self._cur_arr_shape[1], self._cur_arr_shape[2])
        img_size = int(EDIT_HEIGHT * img_dim[1] * img_dim[2])
        img_arr = frombuffer(sh_img_arr.get_obj(), count=img_size, dtype=DTYPE).reshape(img_dim)
        while self._process_imgs:
            sem1.acquire()
            img_pil = Image.fromarray(img_arr)
            draw = ImageDraw.Draw(img_pil)
            draw.text(OVL_POS, text=ovl_arr.value.decode(ENCODE_CODE), font=OVL_FONT, fill=OVL_CLR)
            processed_img = asarray(img_pil)
            copyto(img_arr, processed_img)
            sem2.release()

    def _handle_processed_frames(self) -> None:
        """
        Handle processed frames in proper order from ImgWorker processes.
        :return None:
        """
        i = 0
        while self._process_imgs:
            self._sems2[i].acquire()
            frame = self._np_img_arrs[i]
            if self._writing:
                self._write_q.put(frame)
            if self._show_feed:
                to_send = self.image_resize(frame, width=640)
                self._img_pipe.send(to_send)
            self._sems3[i].release()
            i = (i + 1) % self._num_img_workers

    def _set_texts(self) -> None:
        """
        Set the initial texts for this camera.
        :return None:
        """
        if self._exp_running:
            self._exp_status = self._strings[StringsEnum.EXP_STATUS_RUN]
        else:
            self._exp_status = self._strings[StringsEnum.EXP_STATUS_STOP]

    # from https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
    @staticmethod
    def image_resize(image, width=None, height=None, inter=INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = resize(image, dim, interpolation=inter)

        # return the resized image
        return resized
