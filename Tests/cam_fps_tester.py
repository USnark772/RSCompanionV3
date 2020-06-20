import cv2
from statistics import median
from time import time
from RSCompanionAsync.Devices.Camera.Model.cam_defs import cap_backend, cap_temp_codec, cap_codec


def test_type_read_times(cap: cv2.VideoCapture, cam_index: int, num_reads: int, show_values: bool):
    # Read camera num_frames times and capture time taken per read.
    times = []
    prev = time()
    for i in range(num_reads):
        cap.read()
        now = time()
        times.append(now - prev)
        prev = now

    # Sort times taken low to high.
    times.sort()

    # Show basic output.
    to_print = "Test type: read time" + \
               "\n- Camera: " + str(cam_index) + \
               "\n- Mean time to read frame: " + str(sum(times) / len(times)) + \
               "\n- Median time to read frames: " + str(median(times)) + \
               "\n- Range of times to read frames: " + str(min(times)) + " to " + str(max(times))
    print(to_print)

    # Create dictionary of intervals of 0.01 seconds.
    intervals = dict()
    i = 0
    while i <= times[-1]:
        i += .01
        intervals[round(i, 3)] = list()

    # Sort times taken into dictionary.
    next_time = .01
    next_time = round(next_time, 3)
    for t in times:
        while t > next_time:
            next_time += .01
            next_time = round(next_time, 3)
        intervals[next_time].append(t)

    # Output results.
    prev_key = 0
    for key in intervals:
        if len(intervals[key]) > 0:
            print("- Number of read times between", "{:.2f}".format(prev_key), "and", "{:.2f}".format(key), "seconds:",
                  len(intervals[key]))
            if show_values:
                print(intervals[key])
        prev_key = key
    print("\n")


def test_type_fps(cap: cv2.VideoCapture, cam_index: int, num_reads: int):
    # Get time taken to read camera num_frames times with no other operations.
    s = time()
    for i in range(num_reads):
        cap.read()
    elapsed = time() - s

    # Print results.
    print("Test type: fps"
          "\n- Camera:", cam_index,
          "\n- Num_frames:", num_reads,
          "\n- Time_taken:", elapsed,
          "\n- fps:", num_reads / elapsed)
    print("\n")


def test_cam(backend_to_use, cam_index: int = 0, num_reads: int = 300, info_level: bool = False) -> None:
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

    # Set frame size to desired max.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Run tests.
    test_type_fps(cap, cam_index, num_reads)
    test_type_read_times(cap, cam_index, num_reads, info_level)


def main():
    detailed = False     # Change to true to see more detailed output.
    cam_range_start = 2  # Change to index of first cam to test
    cam_range_end = 3    # Change to index of last cam to test + 1
    num_reads = 180      # Change to number of frames to capture per test.
    for cam_index in range(cam_range_start, cam_range_end):
        test_cam(cap_backend, cam_index, num_reads, detailed)


if __name__ == '__main__':
    main()
