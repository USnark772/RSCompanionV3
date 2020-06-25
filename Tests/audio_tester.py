import pyaudio
import wave
import time
import sys
from PySide2.QtWidgets import *
from RSCompanionAsync.View.MainWindow.central_widget import CentralWidget
from RSCompanionAsync.Model.app_helpers import EasyFrame, ClickAnimationButton

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(300, 200)
        self.setCentralWidget(CentralWidget(self))
        self.myLayout = QHBoxLayout(self)

        # set this to desired file location and name
        self.file = "W:\\stuff\\file.wav"

        self.rec_button = ClickAnimationButton()
        self.rec_button.setText("record")
        self.rec_button.clicked.connect(self.record_audio)

        self.devs_button = ClickAnimationButton()
        self.devs_button.setText("input devices")
        self.devs_button.clicked.connect(self.input_devices)

        self.play_button = ClickAnimationButton()
        self.play_button.setText("play")
        self.play_button.clicked.connect(self.play_audio)

        self.myLayout.addWidget(self.rec_button)
        self.myLayout.addWidget(self.devs_button)
        self.myLayout.addWidget(self.play_button)

        self.centralWidget().layout().addLayout(self.myLayout)

    def play_file(self, file):
        # plays a file given from the command line
        print("Plays a wave file from: %s" % file)

        wf = wave.open(file, 'rb')

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()

        print("done with 1")

        # define callback (2)
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        print("done with 2")

        # open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        print("done with 3")

        # start the stream (4)
        stream.start_stream()

        print("done with 4")

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.1)

        print("done with 5")

        # stop stream (6)
        stream.stop_stream()
        stream.close()
        wf.close()

        print("done with 6")

        # close PyAudio (7)
        p.terminate()

        print("done with 7")

    def record_file(self, file):
        # records audio, and saves it to FILENAME
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 10
        # this is a specific path.
        # change if running on a different machine.
        FILENAME = file

        print("recording to:", FILENAME)

        p = pyaudio.PyAudio()

        # start recording
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        frames = []

        print(p.get_default_input_device_info())

        print("\nrecording\n")

        # saves audio to frames
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

    def input_devices(self):
        retVals = []
        p = pyaudio.PyAudio()

        # print out available mic devices
        for i in range(p.get_device_count()):
            device = p.get_device_info_by_index(i)
            input_ch = device.get('maxInputChannels', 0)
            if input_ch > 0:
                name = device.get('name')
                rate = device.get('defaultSampleRate')
                val = "index {i}: {name} (max channels {input_ch}, Default @ {rate} Hz)".format(i=i, name=name,
                                                                                                input_ch=input_ch,
                                                                                                rate=int(rate))
                print(val)
                retVals.append(val)
        return retVals

    def record_audio(self):
        self.record_file(self.file)

    def play_audio(self):
        self.play_file(self.file)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
