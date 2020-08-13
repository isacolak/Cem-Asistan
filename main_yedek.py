import os
import re
import sys
import time
from gui import *
from PyQt5 import QtMultimedia
from random import choice
from threading import Thread
from Modules import BaseModule

ses = BaseModule.ses()
hava = BaseModule.hava()
hatırlatıcı = BaseModule.hatırlatıcı()
mail = BaseModule.mail()
doviz = BaseModule.doviz()
db = BaseModule.data_base().db
info = BaseModule.info()
face_recognition = BaseModule.FaceRecognition()
web = BaseModule.web()

Saat = time.strftime("%H:%M")
Gün = time.strftime("%w")
Gün2 = time.strftime("%d")
Ay = time.strftime("%m")
Yıl = time.strftime("%Y")
Tarih = time.strftime("%d.%m.%Y")

haftaGün = {'1':'Pazartesi','2':'Salı','3':'Çarşamba','4':'Perşembe','5':'Cuma','6':'Cumartesi','7':'Pazar'}
yılAy = {'01':'Ocak','02':'Şubat','03':'Mart','04':'Nisan','05':'Mayıs','06':'Haziran','07':'Temmuz','08':'Ağustos','09':'Eylül','10':'Ekim','11':'Kasım','12':'Aralık'}


data = {}
data1 = db.child('/').get().val()

def database_c(db):
	global data
	global data1
	try:
		data2 = db.child("/").get().val()
		if data2 != data1:
			data1 = data2
				
	except Exception as e:
		print('Hata: ',e)

def update_data(data_s):
	for key, val in data_s.items():
		data[key] = val

def upload_data(data):
	db.set(data)

update_data(data1)


class mywindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		pixmap = QtGui.QPixmap("Datas/icons/logo.png")
		pixmap = pixmap.scaled(111, 141, QtCore.Qt.KeepAspectRatio)
		self.ui.logo.setPixmap(pixmap)

		self.ui.sideBar.hide()
		self.ui.logo.hide()
		self.ui.assistant.hide()
		self.ui.music_player.hide()

		self.ui.sideBar.itemClicked.connect(self.clicked)
		self.ui.sideBarB.clicked.connect(self.sidebar)
		self.ui.lampB.clicked.connect(self.lampF)
		self.ui.fanB.clicked.connect(self.fanF)
		self.ui.doorB.clicked.connect(self.doorF)
		self.ui.msg.returnPressed.connect(self.msg_a)

		self.up_key = QtWidgets.QShortcut(QtGui.QKeySequence("UP"), self)
		self.up_key.activated.connect(self.up)

		self.down_key = QtWidgets.QShortcut(QtGui.QKeySequence("DOWN"), self)
		self.down_key.activated.connect(self.down)

		self.on_stop = False

		self.player = QtMultimedia.QMediaPlayer()
		self.playList = QtMultimedia.QMediaPlaylist()
		self.userAction = -1			#0- stopped, 1- playing 2-paused
		self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.volumeChanged.connect(self.qmp_volumeChanged)
		self.playList.currentMediaChanged.connect(self.songChanged)
		self.player.setVolume(60)

		self.ui.playB.clicked.connect(self.play)
		self.ui.pauseB.clicked.connect(self.pause)
		self.ui.stopB.clicked.connect(self.stop)
		self.ui.v_DOWN.clicked.connect(self.vDown)
		self.ui.v_UP.clicked.connect(self.vUp)
		self.ui.prevSB.clicked.connect(self.playlistPrev)
		self.ui.nextSB.clicked.connect(self.playlistNext)
		self.ui.slider.sliderMoved.connect(self.seekPosition)

	def up(self):
		print("up")

	def down(self):
		print("DOWN")

	def sidebar(self):
		if self.ui.sideBar.isHidden():
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("Datas/icons/menu_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.sideBarB.setIcon(icon)
			self.ui.sideBar.show()
			self.ui.logo.show()
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("Datas/icons/menu_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.sideBarB.setIcon(icon)
			self.ui.sideBar.hide()
			self.ui.logo.hide()

	def clicked(self,item):
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("Datas/icons/menu_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.sideBarB.setIcon(icon)
		self.ui.title.setText(item.text())
		if item.text() == "Ana Menü":
			self.ui.sideBar.hide()
			self.ui.logo.hide()
			self.ui.assistant.hide()
			self.ui.music_player.hide()
			self.ui.main_menu.show()
		elif item.text() == "Asistan":
			self.ui.sideBar.hide()
			self.ui.logo.hide()
			self.ui.main_menu.hide()
			self.ui.music_player.hide()
			self.ui.assistant.show()
		elif item.text() == "Müzik Oynatıcı":
			self.ui.sideBar.hide()
			self.ui.logo.hide()
			self.ui.main_menu.hide()
			self.ui.assistant.hide()
			self.ui.music_player.show()
			self.playlistAdd()


	def msg_a(self):
		query = self.ui.msg.text()
		self.ui.msg.clear()

		self.assistant(query,"msg")

	def assistant(self,query,w=None):

		a_data = BaseModule.a_data()

		on = True

		if w:
			for i in a_data["user"]:
				if query.lower() in a_data["user"][i]:
					on = False
					if i == "geliştirici":
						self.return_a_w_msg(query, choice(a_data["assistant"][i]))
					elif i == "saat":
						self.return_a_w_msg(query, a_data["assistant"][i].format(Saat))
					elif i == "tarih":
						self.return_a_w_msg(query, a_data["assistant"][i].format(Gün2,yılAy[Ay],haftaGün[Gün]))
					elif i == "durum":
						self.return_a_w_msg(query, choice(a_data["assistant"][i]))
					elif i == "durumD":
						self.return_a_w_msg2(query)
					elif i == "iltifat":
						self.return_a_w_msg(query, choice(a_data["assistant"][i]))
					elif i == "yil":
						self.return_a_w_msg(query, a_data["assistant"][i].format(Yıl))
					elif i == "hava":
						havad = hava.havaD()
						self.return_a_w_msg(query, a_data["assistant"][i].format(hava.ilce if hava.ilce else hava.il,havad))
					elif i == "google_ac":
						self.return_a_w_msg(query, "Google açılıyor")
						web.open_google()
					elif i == "google_kapa":
						self.return_a_w_msg(query, "Google kapatılıyor")
						web.close()
					elif i == "youtube_ac":
						self.return_a_w_msg(query, "Youtube açılıyor")
						web.open_youtube()
					elif i == "youtube_kapa":
						self.return_a_w_msg(query, "Youtube kapatılıyor")
						web.close()
					

			for l in a_data["user"]["lamba_ac"]:
				if l in query.lower():
					if "ışığını" in l:
						lamp_re = re.search('(.+)ışığını',query)
						lamp = lamp_re.group(1)
					if "lambasını" in  l:
						lamp_re = re.search('(.+)lambasını',query)
						lamp = lamp_re.group(1)

					if "odasının" in lamp:
						lampL = lamp.split(" ")
						lampL[lampL.index("odasının")+1] = "odası"
						lampL[lampL.index("odasının")] = " "
						lamp2 = "".join(lampL)
					elif "mutfağın" in lamp:
						lamp2 = "mutfak"
					else:
						lamp2 = lamp.replace("un", "").replace("in", "")
					print(lamp)
					print(lamp2)
					self.return_a_w_msg(query, lamp+"ışığı açılıyor")
					on = False

			for l in a_data["user"]["lamba_kapat"]:
				if l in query.lower():
					if "ışığını" in l:
						lamp_re = re.search('(.+)ışığını',query)
						lamp = lamp_re.group(1)
					if "lambasını" in  l:
						lamp_re = re.search('(.+)lambasını',query)
						lamp = lamp_re.group(1)

					if "odasının" in lamp:
						lampL = lamp.split(" ")
						lampL[lampL.index("odasının")+1] = "odası"
						lampL[lampL.index("odasının")] = " "
						lamp2 = "".join(lampL)
					elif "mutfağın" in lamp:
						lamp2 = "mutfak"
					else:
						lamp2 = lamp.replace("un", "").replace("in", "")
					print(lamp)
					print(lamp2)
					self.return_a_w_msg(query, lamp+"ışığı kapatılıyor")
					on = False

			for l in a_data["user"]["kapi_kilit_ac"]:
				if l == query.lower():
					self.return_a_w_msg(query, "Kapı kilidi açılıyor")
					on = False

			for l in a_data["user"]["kapi_kilit_kapat"]:
				if l == query.lower():
					self.return_a_w_msg(query, "Kapı kilidi kapatılıyor")
					on = False

			for l in a_data["user"]["fan_ac"]:
				if l == query.lower():
					self.return_a_w_msg(query, "Fan açılıyor")
					on = False

			for l in a_data["user"]["fan_kapat"]:
				if l == query.lower():
					self.return_a_w_msg(query, "Fan kapatılıyor")
					on = False

			if on:
				self.return_a_w_msg(query, "Anlamadım")

		else:
			if query == "none":
					text = "Ses Tanıma Hatası"
					self.return_a(text)
			else:
				for i in a_data["user"]:
					if query in a_data["user"][i]:
						on = False
						if i == "geliştirici":
							self.return_a(choice(a_data["assistant"][i]))
						elif i == "saat":
							self.return_a(a_data["assistant"][i].format(Saat))
						elif i == "tarih":
							self.return_a(a_data["assistant"][i].format(Gün2,yılAy[Ay],haftaGün[Gün]))
						elif i == "durum":
							self.return_a(choice(a_data["assistant"][i]))
						elif i == "durumD":
							pass
						elif i == "iltifat":
							self.return_a(choice(a_data["assistant"][i]))
						elif i == "yil":
							self.return_a(a_data["assistant"][i].format(Yıl))
						elif i == "hava":
							havad = hava.havaD()
							self.return_a(a_data["assistant"][i].format(hava.ilce if hava.ilce else hava.il,havad))
						elif i == "google_ac":
							self.return_a("Google açılıyor")
							web.open_google()
						elif i == "google_kapa":
							self.return_a("Google kapatılıyor")
							web.close()
						elif i == "youtube_ac":
							self.return_a("Youtube açılıyor")
							web.open_youtube()
						elif i == "youtube_kapa":
							self.return_a("Youtube kapatılıyor")
							web.close()


				for l in a_data["user"]["lamba_ac"]:
					if l in query:
						if "ışığını" in l:
							lamp_re = re.search('(.+)ışığını',query)
							lamp = lamp_re.group(1)
						if "lambasını" in  l:
							lamp_re = re.search('(.+)lambasını',query)
							lamp = lamp_re.group(1)

						if "odasının" in lamp:
							lampL = lamp.split(" ")
							lampL[lampL.index("odasının")+1] = "odası"
							lampL[lampL.index("odasının")] = " "
							lamp2 = "".join(lampL)
						elif "mutfağın" in lamp:
							lamp2 = "mutfak"
						else:
							lamp2 = lamp.replace("un", "").replace("in", "")
						print(lamp)
						print(lamp2)
						self.return_a(lamp+"ışığı açılıyor")
						on = False

				for l in a_data["user"]["lamba_kapat"]:
					if l in query:
						if "ışığını" in l:
							lamp_re = re.search('(.+)ışığını',query)
							lamp = lamp_re.group(1)
						if "lambasını" in  l:
							lamp_re = re.search('(.+)lambasını',query)
							lamp = lamp_re.group(1)

						if "odasının" in lamp:
							lampL = lamp.split(" ")
							lampL[lampL.index("odasının")+1] = "odası"
							lampL[lampL.index("odasının")] = " "
							lamp2 = "".join(lampL)
						elif "mutfağın" in lamp:
							lamp2 = "mutfak"
						else:
							lamp2 = lamp.replace("un", "").replace("in", "")
						print(lamp)
						print(lamp2)
						self.return_a(lamp+"ışığı kapatılıyor")
						on = False

				for l in a_data["user"]["kapi_kilit_ac"]:
					if l == query:
						self.return_a("Kapı kilidi açılıyor")
						on = False

				for l in a_data["user"]["kapi_kilit_kapat"]:
					if l == query:
						self.return_a("Kapı kilidi kapatılıyor")
						on = False

				for l in a_data["user"]["fan_ac"]:
					if l == query:
						self.return_a("Fan açılıyor")
						on = False

				for l in a_data["user"]["fan_kapat"]:
					if l == query:
						self.return_a("Fan kapatılıyor")
						on = False

				if on:
					self.return_a("Anlamadım")
					print(query)

	def return_a_w_msg(self,query,text):
		if query == "none":
			text = "Ses Tanıma Hatası"
			ses.tts(text)
			self.ui.textEdit.append('<span style="color:#0000FF">Asistan</span> ==> '+text+'<br>')

		else:
			ses.tts(text)
			self.ui.textEdit.append('<span style="color:#0000FF">Sen</span> ==> '+query+'<br><span style="color:#0000FF">Asistan</span> ==> '+text+"<br>")

	def return_a_w_msg2(self,query):
		if query == "none":
			text = "Ses Tanıma Hatası"
			ses.tts(text)
			self.ui.textEdit.append('<span style="color:#0000FF">Asistan</span> ==> '+text+'<br>')

		else:
			self.ui.textEdit.append('<span style="color:#0000FF">Sen</span> ==> '+query)

	def return_a(self,text):
		ses.tts(text)

	def lampF(self):
		icon_on = QtGui.QIcon()
		icon_on.addPixmap(QtGui.QPixmap("Datas/icons/lamp_on.png"), QtGui.QIcon.Normal)

		icon_off = QtGui.QIcon()
		icon_off.addPixmap(QtGui.QPixmap("Datas/icons/lamp_off.png"), QtGui.QIcon.Normal)

		if data["lamp"]["status"] == "true":
			data["lamp"]["status"] = "false"
			self.ui.lampB.setIcon(icon_off)
			upload_data(data)
		elif data["lamp"]["status"] == "false":
			data["lamp"]["status"] = "true"
			self.ui.lampB.setIcon(icon_on)
			upload_data(data)

	def fanF(self):
		icon_on = QtGui.QIcon()
		icon_on.addPixmap(QtGui.QPixmap("Datas/icons/fan_on.png"), QtGui.QIcon.Normal)

		icon_off = QtGui.QIcon()
		icon_off.addPixmap(QtGui.QPixmap("Datas/icons/fan_off.png"), QtGui.QIcon.Normal)

		if data["fan"]["status"] == "true":
			data["fan"]["status"] = "false"
			self.ui.fanB.setIcon(icon_off)
			upload_data(data)
		elif data["fan"]["status"] == "false":
			data["fan"]["status"] = "true"
			self.ui.fanB.setIcon(icon_on)
			upload_data(data)

	def doorF(self):
		icon_on = QtGui.QIcon()
		icon_on.addPixmap(QtGui.QPixmap("Datas/icons/door_locked.png"), QtGui.QIcon.Normal)

		icon_off = QtGui.QIcon()
		icon_off.addPixmap(QtGui.QPixmap("Datas/icons/door_opened.png"), QtGui.QIcon.Normal)

		if data["door_lock"]["status"] == "true":
			data["door_lock"]["status"] = "false"
			self.ui.doorB.setIcon(icon_off)
			upload_data(data)
		elif data["door_lock"]["status"] == "false":
			data["door_lock"]["status"] = "true"
			self.ui.doorB.setIcon(icon_on)
			upload_data(data)

	def play(self):
		self.userAction = 1
		if self.player.state() == QtMultimedia.QMediaPlayer.StoppedState :
			if self.player.mediaStatus() == QtMultimedia.QMediaPlayer.NoMedia:
				print(self.playList.mediaCount())
				if self.playList.mediaCount() == 0:
					self.playlistAdd()
				if self.playList.mediaCount() != 0:
					self.playlistAdd()
			elif self.player.mediaStatus() == QtMultimedia.QMediaPlayer.LoadedMedia:
				self.player.play()
			elif self.player.mediaStatus() == QtMultimedia.QMediaPlayer.BufferedMedia:
				self.player.play()
		elif self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
			pass
		elif self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
			self.player.play()
			
	def pause(self):
		self.userAction = 2
		self.player.pause()
			
	def stop(self):
		self.userAction = 0
		if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
			self.stopState = True
			self.player.stop()
		elif self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
			self.player.stop()
		elif self.player.state() == QtMultimedia.QMediaPlayer.StoppedState:
			pass

	def qmp_mediaStatusChanged(self):
		if self.player.mediaStatus() == QtMultimedia.QMediaPlayer.LoadedMedia and self.userAction == 1:
			durationT = self.player.duration()
			self.ui.slider.setRange(0,durationT)
			self.ui.eta.setText('%d:%02d'%(int(durationT/60000),int((durationT/1000)%60)))
			self.player.play()
		if self.player.mediaStatus() == QtMultimedia.QMediaPlayer.EndOfMedia and self.player.state() != QtMultimedia.QMediaPlayer.StoppedState:
			self.playList.next()
			
	def qmp_stateChanged(self):
		if self.player.state() == QtMultimedia.QMediaPlayer.StoppedState:
			self.player.stop()
			
	def qmp_positionChanged(self, position,senderType=False):
		if senderType == False:
			self.ui.slider.setValue(position)
			self.ui.time.setText('%d:%02d'%(int(position/60000),int((position/1000)%60)))
	
	def seekPosition(self, position):
		sender = self.sender()
		if isinstance(sender,QtWidgets.QSlider):
			if self.player.isSeekable():
				self.player.setPosition(position)
				
	def qmp_volumeChanged(self):
		self.ui.vBar.show()
		self.ui.vBar.setValue(self.player.volume())
		time.sleep(0.5)
		self.ui.vBar.hide()

	def songChanged(self,media):
		if not media.isNull():
			url = media.canonicalUrl()
			name = url.fileName()
			self.ui.soundN.setText(name[:len(name)-4])
			durationT = self.player.duration()
			self.ui.slider.setRange(0,durationT)
			self.ui.eta.setText('%d:%02d'%(int(durationT/60000),int((durationT/1000)%60)))
		
	def vUp(self):
		vol = self.player.volume()
		vol = min(vol+5,100)
		self.player.setVolume(vol)
		
	def vDown(self):
		vol = self.player.volume()
		vol = max(vol-5,0)
		self.player.setVolume(vol)
	
	def playlistPrev(self):
		self.playList.previous()
	
	def playlistNext(self):
		self.playList.next()

	def playlistAdd(self):
		listF = os.listdir("Datas/müzikler")
		self.player.setPlaylist(self.playList)

		for name in listF:
			self.playList.addMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile("Datas/müzikler/"+name)))


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	win = mywindow()
	win.show()

	def update_info():
		global db
		global win
		global data
		global data1

		database_c(db)
		update_data(data1)
		
		for i in data:
			if i == "status":
				if data[i] == "true":
					win.ui.statusL.setText("Durum: Aktif")
				elif data[i] == "false":
					win.ui.statusL.setText("Durum: Kapalı")
				else:
					win.ui.statusL.setText("Dururm: Bilinmiyor")
			elif i == "temperature":
				win.ui.temperatureL.setText("Sıcaklık: "+str(data[i]))
			elif i == "moisture":
				win.ui.moistureL.setText("Nem: "+str(data[i]))
			elif i == "lamp":
				if data[i]["status"] == "true":
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/lamp_on.png"), QtGui.QIcon.Normal)
					win.ui.lampB.setIcon(icon)
				elif data[i]["status"] == "false":
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/lamp_off.png"), QtGui.QIcon.Normal)
					win.ui.lampB.setIcon(icon)
				else:
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/error.png"), QtGui.QIcon.Normal)
					win.ui.lampB.setIcon(icon)
			elif i == "fan":
				if data[i]["status"] == "true":
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/fan_on.png"), QtGui.QIcon.Normal)
					win.ui.fanB.setIcon(icon)
				elif data[i]["status"] == "false":
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/fan_off.png"), QtGui.QIcon.Normal)
					win.ui.fanB.setIcon(icon)
				else:
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/error.png"), QtGui.QIcon.Normal)
					win.ui.fanB.setIcon(icon)
			elif i == "door_lock":
				if data[i]["status"] == "true":
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/door_locked.png"), QtGui.QIcon.Normal)
					win.ui.doorB.setIcon(icon)
				elif data[i]["status"] == "false":
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/door_opened.png"), QtGui.QIcon.Normal)
					win.ui.doorB.setIcon(icon)
				else:
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap("Datas/icons/error.png"), QtGui.QIcon.Normal)
					win.ui.doorB.setIcon(icon)

	def check():
		while True:
			update_info()
			time.sleep(1)

	def reji():
		global win
		while True:
			a_data = BaseModule.a_data()
			query = ses.stt().lower()
			if query in a_data["user"]["cem"]:
				win.return_a(choice(a_data["assistant"]["cem"])+info["ad"])
				query = ses.stt().lower()
				win.assistant(query)
			elif query != "cem" and "cem" in query:
				query = re.search("cem (.+)", query).group(1)
				win.assistant(query)


	th_check = Thread(target=check)
	th_check.daemon = True
	th_check.start()

	th_reji = Thread(target=reji)
	th_reji.daemon = True
	th_reji.start()

	update_info()


	#face_recognition.start()
	#ses.tts("selam "+face_recognition.result)

	sys.exit(app.exec())
