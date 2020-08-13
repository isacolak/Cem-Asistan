import sys
from PyQt5 import *
from PyQt5 import QtWidgets, QtGui, QtCore
from pyqtgraph import PlotWidget
from threading import Thread
import pyqtgraph
import numpy as np
import sv_listener
import socket
import time
import os

"""
host = socket.gethostname()
port = 1555

s = socket.socket()
s.bind((host,port))

def s_accept():
    global con
    s.listen(1)
    con,addr = s.accept()

def s_send():
    if con:
        con.send(str("ss").encode())

def sv_start():
    os.system("python sv.py")
    s.close()
"""

class myWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #self.b = QtWidgets.QPushButton("off",self)
        #self.b.move(100,10)
        #self.b.clicked.connect(s_send)
        #self.frame = QtWidgets.QFrame(self)
        #self.frame.setGeometry(0,0,400,200)

        #self.vbox = QtWidgets.QVBoxLayout(self.frame)

        self.setGeometry(500,200,411,111)

        self.p_w = PlotWidget(self)
        self.p_w.setGeometry(QtCore.QRect(0, 0, 411, 111))
        self.p_w.setObjectName("p_w")

        #self.vbox.addWidget(self.p_w)

        self.p_w.plotItem.showGrid(False, False,0.7)
        self.p_w.plotItem.hideAxis("left")
        self.p_w.plotItem.hideAxis("bottom")

        self.maxP = 0

        self.ear = sv_listener.listener(rate=44100,updatesPerSecond=20)
        self.ear.stream_start()

        self.update()


    def update(self):
        if not self.ear.data is None:
            pMax=np.max(np.abs(self.ear.data))
            if pMax>self.maxP:
                self.maxP=pMax
                self.p_w.plotItem.setRange(yRange=[-pMax,pMax])
            pen=pyqtgraph.mkPen(color='b')
            self.p_w.plot(self.ear.datax,self.ear.data,pen=pen,clear=True)
        QtCore.QTimer.singleShot(1,self.update)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = myWin()
    win.show()
    """ 
    th = Thread(target=s_accept)
    th2 = Thread(target=sv_start)
    th.daemon = True
    th2.daemon = True
    th.start()
    th2.start()
    """
    sys.exit(app.exec())