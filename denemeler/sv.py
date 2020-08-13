from PyQt5 import *
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg

import struct
import pyaudio
from scipy.fftpack import fft
import numpy as np

import sys
import time

import socket

from threading import Thread

host = socket.gethostname()
port = 1555

s = socket.socket()

class AudioStream(object):
    def __init__(self):
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Spectrum Analyzer')
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(505, 300, 350, 150)

        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (127, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        self.waveform = self.win.addPlot(
            row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )
        self.waveform.hideAxis("bottom")
        self.waveform.hideAxis("left")
        self.waveform.setMouseEnabled(x=False,y=False)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

        self.x = np.arange(0, 2 * self.CHUNK, 2)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0.1)
                self.waveform.setXRange(0, 1 * self.CHUNK, padding=0.005)

    def update(self):
        wf_data = self.stream.read(self.CHUNK)
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data,)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(1)
        self.start()

    def s_connect(self):
        s.connect((host,port))
        data = s.recv(1024).decode()
        self.close_sv()

    def close_sv(self):
        QtCore.QCoreApplication.instance().quit()



if __name__ == '__main__':
    audio_app = AudioStream()
    th = Thread(target=audio_app.s_connect)
    th.start()
    audio_app.animation()
        