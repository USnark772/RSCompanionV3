import os
import cv2
import time

dir_name = "C:/Users/phill/Companion Save Files/experiment_2020-08-01-11-47-21/"


def get_frms_fps(file: str):
    reader = cv2.VideoCapture(file)
    num_frames = 0
    fps = 0
    runtime = 0
    try:
        num_frames = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = reader.get(cv2.CAP_PROP_FPS)
        runtime = num_frames/fps
        return num_frames, fps, runtime
    except Exception as e:
        print("Failed to get num frames the short way: ", e)
        print("Getting num frames the long way...")
        while True:
            ret, frame = reader.read()
            if not ret:
                break
            num_frames += 1
    finally:
        reader.release()
        return num_frames, fps, runtime


def main():
    vid_infos = dict()
    num_frms_key = "Num frames"
    fps_key = "FPS"
    runtime_key = "Runtime"
    vid_infos[num_frms_key] = list()
    vid_infos[fps_key] = list()
    vid_infos[runtime_key] = list()
    cur_dir = os.getcwd()
    print("os.chdir(" + dir_name + ")")
    os.chdir(dir_name)
    for file in os.listdir():
        if file.endswith('.avi'):
            print("get_frms_fps(" + file + ")...")
            num_frames, fps, runtime = get_frms_fps(file)
            vid_infos[num_frms_key].append(num_frames)
            vid_infos[fps_key].append(fps)
            vid_infos[runtime_key].append(runtime)
            print("\tNum frames: " + str(num_frames) + ", fps: " + str(fps) + ", runtime: " + str(time.strftime('%H:%M:%S', time.gmtime(runtime))))
    print("Runtime range: " + str(max(vid_infos[runtime_key]) - min(vid_infos[runtime_key])))
    print("os.chdir(" + cur_dir + ")")
    os.chdir(cur_dir)


if __name__ == '__main__':
    main()
