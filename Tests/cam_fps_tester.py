import cv2
from statistics import median
from time import time
from Devices.Camera.Model.cam_defs import cap_backend, cap_temp_codec, cap_codec


def test_type_read_times(cap, cam_index, num_frames, show_values):
    times = []
    prev = time()
    for i in range(num_frames):
        cap.read()
        now = time()
        times.append((now - prev))
        prev = now

    times.sort()
    to_print = "Test type: read time" \
               "Camera: " + str(cam_index) + \
               "\n- Mean time to read frame: " + str(sum(times) / len(times)) + \
               "\n- Median time to read frames: " + str(median(times)) + \
               "\n- Range of times to read frames: " + str(min(times)) + " to " + str(max(times))
    print(to_print)

    intervals = dict()
    i = 0
    while i <= times[-1]:
        i += .01
        intervals[round(i, 3)] = list()

    next_time = .01
    next_time = round(next_time, 3)
    for t in times:
        while t > next_time:
            next_time += .01
            next_time = round(next_time, 3)
        intervals[next_time].append(t)

    prev_key = 0
    for key in intervals:
        if len(intervals[key]) > 0:
            print("- Number of values between", "{:.2f}".format(prev_key), "and", "{:.2f}".format(key), ":",
                  len(intervals[key]))
            if show_values:
                print(intervals[key])
        prev_key = key
    print("\n")


def test_type_fps(cap, cam_index, num_frames):
    # Get time taken to read camera num_frames times with no other operations.
    s = time()
    for i in range(num_frames):
        cap.read()
    elapsed = time() - s

    # Print results.
    print("Test type: fps"
          "Camera:", cam_index,
          "\n- Num_frames:", num_frames,
          "\n- Time_taken:", elapsed,
          "\n- fps:", num_frames / elapsed)
    print("\n")


def test_cam(backend_to_use, cam_index: int = 0, info_level: bool = False) -> None:
    # Open camera
    cap = cv2.VideoCapture(cam_index, backend_to_use)

    # Test if camera was opened successfully.
    if not cap.isOpened():
        print("Cam failed to open")
        return

    # Test if camera can be read successfully.
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Cam failed to read.")
        return

    # Set required codec.
    cap.set(cv2.CAP_PROP_FOURCC, cap_temp_codec)
    cap.set(cv2.CAP_PROP_FOURCC, cap_codec)

    # Set max frame size.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Set number of frames to read.
    num_frames = 310
    # Run tests.
    test_type_fps(cap, cam_index, num_frames)
    test_type_read_times(cap, cam_index, num_frames, info_level)


def main():
    detailed = False  # Change to true to see more detailed output.
    for cam_index in range(1, 3):
        test_cam(cap_backend, cam_index, detailed)


if __name__ == '__main__':
    main()
