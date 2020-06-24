import pyaudio
import wave
import time
import sys

# plays a file given from the command line
# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)
#
# wf = wave.open(sys.argv[1], 'rb')
#
# # instantiate PyAudio (1)
# p = pyaudio.PyAudio()
#
# print("done with 1")
#
#
# # define callback (2)
# def callback(in_data, frame_count, time_info, status):
#     data = wf.readframes(frame_count)
#     return (data, pyaudio.paContinue)
#
#
# print("done with 2")
#
# # open stream using callback (3)
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True,
#                 stream_callback=callback)
#
# print("done with 3")
#
# # start the stream (4)
# stream.start_stream()
#
# print("done with 4")
#
# # wait for stream to finish (5)
# while stream.is_active():
#     time.sleep(0.1)
#
# print("done with 5")
#
# # stop stream (6)
# stream.stop_stream()
# stream.close()
# wf.close()
#
# print("done with 6")
#
# # close PyAudio (7)
# p.terminate()
#
# print("done with 7")

# records audio, and saves it to FILENAME
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
# this is a specific path.
# change if running on a different machine.
FILENAME = "W:\\stuff\\file.wav"

p = pyaudio.PyAudio()

# start recording
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("recording")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("finished recording")

# stop recording
stream.stop_stream()
stream.close()
p.terminate()

waveFile = wave.open(FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(p.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
