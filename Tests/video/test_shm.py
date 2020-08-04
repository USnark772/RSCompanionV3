import numpy as np
from time import sleep, time, mktime
from datetime import datetime
from RSCompanionAsync.Model.app_helpers import format_current_time
from RSCompanionAsync.Devices.Camera.Model.cam_defs import cap_temp_codec, cap_codec
from Debugging_Profiling.profile_defs import profile_outdir
from multiprocessing import Process, Array, Semaphore, Value
from PIL import Image, ImageDraw, ImageFont
from cv2 import VideoCapture, CAP_DSHOW, imshow, waitKey, CAP_PROP_FOURCC, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from ctypes import c_char
from collections import deque
from textwrap import fill, shorten
from threading import Thread
import cProfile

IMG_SIZE = (640, 480)
# IMG_SIZE = (1920, 1080)

SHORT_OVL = "Exp Name, Timestamp, Block, KeyFlag, FPS:"

cond_name = "This is a test condition name that I like."
extra_cond_name = "that is so long that it likely goes off the edge of the image which is not really good so we have" \
                  " to add textwrap so it fits more properly but hopefully it wraps nicely and looks ok."

NL_SEP = "\n"
CM_SEP = ","
# OVL1 = "Condition name: This is a test condition name " + extra_cond_name + SEP
OVL1 = "Condition name: This is a test condition name." + NL_SEP
OVL2 = NL_SEP + "Block: 2" + NL_SEP + \
       "Keyflag: f" + NL_SEP
STR_ENCODING = 'utf-8'
DTYPE = np.uint8
FNT_SIZE = 18
NAME_WIDTH = 30
OVL1 = fill(OVL1, NAME_WIDTH) + NL_SEP
EDIT_HEIGHT = 22
OVL_FNT = ImageFont.truetype("simsun.ttc", FNT_SIZE)
r = 211
g = 250
b = 10
OVL_CLR = (b, g, r)
OVL_POS = (6, 3)

NUM_CAM_PROCS = 1
NUM_CAMS = 3
RUN_TIME = 300


BYTESTR_SIZE = 512


class FPSTracker:
    def __init__(self):
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


def add_overlay(image: np.ndarray, line: str):
    image_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(image_pil)
    draw.text(OVL_POS, text=line, font=OVL_FNT, fill=OVL_CLR)
    return np.asarray(image_pil)


def image_processor(index: int, shared_array: Array, shared_dim: tuple, sem1: Semaphore, sem2: Semaphore, line: Array, running: Value):
    shm_size = EDIT_HEIGHT * shared_dim[1] * shared_dim[2]
    np_arr = np.frombuffer(shared_array.get_obj(), count=int(shm_size), dtype=DTYPE).reshape(
        (EDIT_HEIGHT, shared_dim[1], shared_dim[2]))
    out_name = profile_outdir + "test_shm_proc_" + str(index) + "_image_processor" + ".prof"
    pflr = cProfile.Profile()
    pflr.enable()
    while running.value != 0:
        sem1.acquire()
        np.copyto(np_arr, add_overlay(np_arr, line.value.decode(STR_ENCODING)))
        sem2.release()
    pflr.disable()
    pflr.dump_stats(out_name)


def cam_reader(index: int, shared_arrays: [Array], shared_dim: tuple, sems1_list: [Semaphore], sems3_list: [Semaphore],
               ovl_arrs: [Array], running: Value):
    fps_tracker = FPSTracker()
    cap = VideoCapture(index, CAP_DSHOW)
    cap.set(CAP_PROP_FOURCC, cap_temp_codec)
    cap.set(CAP_PROP_FOURCC, cap_codec)
    cap.set(CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
    cap.set(CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
    ret, frame = cap.read()
    shm_size = shared_dim[0] * shared_dim[1] * shared_dim[2]
    np_arrs = list()
    for j in range(NUM_CAM_PROCS):
        np_arrs.append(np.frombuffer(shared_arrays[j].get_obj(), count=shm_size, dtype=DTYPE).reshape(shared_dim))
    k = 0
    out_name = profile_outdir + "test_shm_proc_" + str(index) + "_reader" + ".prof"
    pflr = cProfile.Profile()
    pflr.enable()
    while running.value != 0:
        ret, frame = cap.read()
        timestamp = datetime.now()
        fps_tracker.update_fps(timestamp)
        sems3_list[k].acquire()
        if ret and frame is not None:
            np.copyto(np_arrs[k], frame)
            fps = str(fps_tracker.get_fps())
            # line = OVL1 + "Timestamp: " + format_current_time(timestamp, True, True, True) + OVL2 + "FPS: " + fps
            line = shorten(cond_name, NAME_WIDTH) + CM_SEP + format_current_time(timestamp, time=True, mil=True) + CM_SEP + "2" + CM_SEP + "k" + CM_SEP + fps
            ovl_arrs[k].value = line.encode(STR_ENCODING)
        sems1_list[k].release()
        k = (k + 1) % NUM_CAM_PROCS
    pflr.disable()
    pflr.dump_stats(out_name)


def vid_disp(index: int, shared_arrays: [Array], shared_dim: tuple, sems2_list: [Semaphore], sems3_list: [Semaphore], running: Value):
    shm_size = shared_dim[0] * shared_dim[1] * shared_dim[2]
    np_arrs = list()
    for j in range(NUM_CAM_PROCS):
        np_arrs.append(np.frombuffer(shared_arrays[j].get_obj(), count=shm_size, dtype=DTYPE).reshape(shared_dim))
    k = 0
    name = "Camera: " + str(index)
    out_name = profile_outdir + "test_shm_proc_" + str(index) + "_display" + ".prof"
    pflr = cProfile.Profile()
    pflr.enable()
    while running.value != 0:
        sems2_list[k].acquire()
        imshow(name, np_arrs[k])
        waitKey(1)
        sems3_list[k].release()
        k = (k + 1) % NUM_CAM_PROCS
    pflr.disable()
    pflr.dump_stats(out_name)


def prog_proc(cam_index: int, running: Value):
    shm_arr_dim = (1080, 1920, 3)
    image_dim = (IMG_SIZE[1], IMG_SIZE[0], 3)
    image_processors = list()
    sems1 = list()
    sems2 = list()
    sems3 = list()
    shm_arrs = list()
    shm_ovl_arrs = list()
    out_name = profile_outdir + "test_shm_proc_" + str(cam_index) + ".prof"
    pflr = cProfile.Profile()
    pflr.enable()
    for i in range(NUM_CAM_PROCS):
        sems1.append(Semaphore(0))
        sems2.append(Semaphore(0))
        sems3.append(Semaphore(1))
        shm_ovl_arrs.append(Array(c_char, BYTESTR_SIZE))
        shm_arrs.append(Array('i', shm_arr_dim[0] * shm_arr_dim[1] * shm_arr_dim[2]))
        image_processors.append(Thread(target=image_processor, daemon=True, args=(cam_index, shm_arrs[i], image_dim, sems1[i],
                                                                                  sems2[i], shm_ovl_arrs[i], running,)))
        image_processors[i].start()
    cam = Thread(target=cam_reader, daemon=True, args=(cam_index, shm_arrs, image_dim, sems1, sems3, shm_ovl_arrs, running,))
    cam.start()
    disp = Thread(target=vid_disp, daemon=True, args=(cam_index, shm_arrs, image_dim, sems2, sems3, running,))
    disp.start()
    while running.value != 0:
        sleep(1)
    sleep(5)
    pflr.disable()
    pflr.dump_stats(out_name)


def main():
    procs = list()
    stop_bool = Value('i', 1)
    for p in range(NUM_CAMS):
        procs.append(Process(target=prog_proc, args=(p, stop_bool)))
        procs[p].start()
    sleep(RUN_TIME)
    stop_bool.value = 0
    for p in procs:
        p.join()


if __name__ == '__main__':
    # cProfile.run('main()', out_name)
    main()
