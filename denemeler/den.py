import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets


class myWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		view = QtWebEngineWidgets.QWebEngineView()
		file = os.path.join(
			os.path.dirname(os.path.realpath(__file__)), 
			"den.html"
		)
		view.load(QtCore.QUrl.fromLocalFile(file))
		self.setCentralWidget(view)
		self.resize(640, 480)

if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	mw = myWindow()
	mw.show()
	sys.exit(app.exec_())