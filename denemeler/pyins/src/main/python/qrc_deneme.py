try:
	import sys
	import time
	from denn import *

	class MyWindow(QtWidgets.QMainWindow):
		def __init__(self):
			super().__init__()
			self.ui = Ui_Form()
			self.ui.setupUi(self)
except Exception as e:
	print(e)
	time.sleep(10)

if __name__ == '__main__':
	try:
		app = QtWidgets.QApplication([])
		win = MyWindow()
		win.show()
		sys.exit(app.exec())
	except Exception as e:
		print(e)
		time.sleep(10)