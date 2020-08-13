try:
	import os
	import re
	import sys
	import time
	import socket
	from gui import *
	from PyQt5 import QtMultimedia
	from random import choice
	from threading import Thread
	from Modules import BaseModule
	from datetime import date,datetime

	try:
		ses = BaseModule.ses()
		hava = BaseModule.hava()
		hatirlatici = BaseModule.reminders()
		mail = BaseModule.mail()
		doviz = BaseModule.doviz()
		db = BaseModule.data_base().db
		info = BaseModule.info()
		face_recognition = BaseModule.FaceRecognition()
		web = BaseModule.web()
	except Exception as e:
		print("Hata: ",e)

	haftaGün = {'1':'Pazartesi','2':'Salı','3':'Çarşamba','4':'Perşembe','5':'Cuma','6':'Cumartesi','7':'Pazar'}
	yılAy = {'01':'Ocak','02':'Şubat','03':'Mart','04':'Nisan','05':'Mayıs','06':'Haziran','07':'Temmuz','08':'Ağustos','09':'Eylül','10':'Ekim','11':'Kasım','12':'Aralık'}

	dayToGün = {"Mon":"Pazartesi","Tue":"Salı","Wed":"Çarşamba","Thu":"Perşembe","Fri":"Cuma","Sat":"Cumartesi","Sun":"Pazar"}
	monToAy = {"Jan":"Ocak","Feb":"Şubat","Mar":"Mart","Apr":"Nisa","May":"Mayıs","Jun":"Haziran","Jul":"Temmuz","Aug":"Ağustos","Sep":"Eylül","Oct":"Ekim","Nov":"Kasım","Dec":"Aralık"}

	data = {}
	data1 = db.reference("/").get()

	def database_c(db):
		global data
		global data1
		try:
			data2 = db.reference("/").get()
			if data2 != data1:
				data1 = data2
					
		except Exception as e:
			print('Hata: ',e)

	def update_data(data_s):
		global data
		for key, val in data_s.items():
			data[key] = val

	def upload_data(data):
		db.reference("/").set(data)

	update_data(data1)


	class mywindow(QtWidgets.QMainWindow):
		def __init__(self):
			super().__init__()
			self.ui = Ui_Form()
			self.ui.setupUi(self)

			self.ui.sideBar.hide()
			self.ui.logo.hide()
			self.ui.assistant.hide()
			self.ui.music_player.hide()

			self.ui.sideBar.setCurrentRow(0)

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
				icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/menu_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.ui.sideBarB.setIcon(icon)
				self.ui.sideBar.show()
				self.ui.logo.show()
			else:
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/menu_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				self.ui.sideBarB.setIcon(icon)
				self.ui.sideBar.hide()
				self.ui.logo.hide()

		def clicked(self,item):
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/menu_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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

			self.assistant(query,w=True)

		def assistant(self,query,w=False):

			web.close()

			a_data = BaseModule.a_data()

			on = True

			for i in a_data["user"]:
				if query.lower() in a_data["user"][i]:
					on = False
					if i == "geliştirici":
						if w:
							self.return_a_w_msg(query, choice(a_data["assistant"][i]))
						else:
							self.return_a(choice(a_data["assistant"][i]))
						
					elif i == "saat":
						if w:
							self.return_a_w_msg(query, a_data["assistant"][i].format(time.strftime("%H:%M")))
						else:
							self.return_a(a_data["assistant"][i].format(time.strftime("%H:%M")))
						
					elif i == "tarih":
						if w:
							self.return_a_w_msg(query, a_data["assistant"][i].format(time.strftime("%d"),yılAy[time.strftime("%m")],haftaGün[time.strftime("%w")]))
						else:
							self.return_a(query, a_data["assistant"][i].format(time.strftime("%d"),yılAy[time.strftime("%m")],haftaGün[time.strftime("%w")]))
						
					elif i == "durum":
						if w:
							self.return_a_w_msg(query, choice(a_data["assistant"][i]))
						else:
							self.return_a(choice(a_data["assistant"][i]))
							
					elif i == "durumD":
						if w:
							self.return_a_w_msg2(query)
						else:
							pass
							
					elif i == "iltifat":
						if w:
							self.return_a_w_msg(query, choice(a_data["assistant"][i]))
						else:
							self.return_a(choice(a_data["assistant"][i]))
							
					elif i == "yil":
						if w:
							self.return_a_w_msg(query, a_data["assistant"][i].format(time.strftime("%Y")))
						else:
							self.return_a(a_data["assistant"][i].format(time.strftime("%Y")))
							
					elif i == "gun2":
						if w:
							self.return_a_w_msg(query, a_data["assistant"][i].format(haftaGün[time.strftime("%w")]))
						else:
							self.return_a(a_data["assistant"][i].format(haftaGün[time.strftime("%w")]))
							
					elif i == "hava":
						il,ilce,havad = hava.havaD()

						if w:
							self.return_a_w_msg(query, a_data["assistant"][i].format(il+" "+ilce if ilce else il,havad))
						else:
							self.return_a(a_data["assistant"][i].format(il+" "+ilce if ilce else il,havad))
							
					elif i == "havaY":
						il,ilce,havad = hava.havaDY()

						if w:
							self.return_a_w_msg(query, a_data["assistant"][i].format(il+" "+ilce if ilce else il,havad))
						else:
							self.return_a(a_data["assistant"][i].format(il+" "+ilce if ilce else il,havad))
							
					elif i == "doviz":
						if w:
							self.return_a_w_msg(query, doviz.doviz())
						else:
							self.return_a(doviz.doviz())
							
					elif i == "google_ac":
						if w:
							self.return_a_w_msg(query, "Google açılıyor")
						else:
							self.return_a("Google açılıyor")
						web.open_google()
						
					elif i == "google_kapa":
						if w:
							self.return_a_w_msg(query, "Google kapatılıyor")
						else:
							self.return_a("Google kapatılıyor")
						web.close()
						
					elif i == "youtube_ac":
						if w:
							self.return_a_w_msg(query, "Youtube açılıyor")
						else:
							self.return_a("Youtube açılıyor")
						web.open_youtube()
						
					elif i == "youtube_kapa":
						if w:
							self.return_a_w_msg(query, "Youtube kapatılıyor")
						else:
							self.return_a("Youtube kapatılıyor")
						web.close()
						
					elif i == "h_lar_oku":

						reminders = hatirlatici.read_reminders()

						reminders_count = 0

						for d in reminders:
							reminders_count += len(reminders[d])

						if w:
							self.return_a_w_msg(query, "Toplam "+str(reminders_count)+" tane hatırlatıcı bulunuyor.")
						else:
							self.return_a("Toplam "+str(reminders_count)+" tane hatırlatıcı bulunuyor.")

						for d in reminders:
							g,a,y = d.split(".")
							sp = date(int(y),int(a),int(g)).ctime().split(" ")
							g2 = dayToGün[sp[0]]
							a2 = monToAy[sp[1]]

							if date(int(y),int(a),int(g)).isocalendar()[1] == datetime.now().isocalendar()[1]:
								for t in reminders[d]:
									if w:
										self.return_a_w_msg3(haftaGün[str(date(int(y),int(a),int(g)).isocalendar()[2])]+", "+t+", "+reminders[d][t])
									else:
										self.return_a(haftaGün[str(date(int(y),int(a),int(g)).isocalendar()[2])]+", "+t+", "+reminders[d][t])
							else:
								for t in reminders[d]:
									if w:
										self.return_a_w_msg3(d+", "+t+", "+reminders[d][t])
									else:
										self.return_a(d+", "+t+", "+reminders[d][t])
					elif i == "h_oluş" and not w:
						self.return_a("Lütfen hatırlatıcının tarihini söylermisin. Örneğin 20 Mart saat 11:25 balo.")
								
						while True:
							r_data =  ses.stt()

							if r_data != "None":
								break
							else:
								self.return_a("Ses tanıma hatası. Lütfen tekrar söylermisin.")

						print(r_data)

			for s in a_data["user"]["m_g"]:
				if s in query.lower() and not w:
					on = False
					to = re.search('(.+) '+s, query).group(1).split("'")[0]
					self.return_a("Lütfen e-postanın içeriğini söylermisin.")

					while True:
						con = ses.stt()
						if con != "None":
							break
						else:
							self.return_a("Ses tanıma hatası. Lütfen tekrar söylermisin.")

					self.return_a("Lütfen e-postanın konusunu söylermisin.")

					while True:
						subj = ses.stt()
						if subj != "None":
							break
						else:
							self.return_a("Ses tanıma hatası. Lütfen tekrar söylermisin.")
					try:
						self.return_a(mail.mailG(to, con, subj))
					except Exception as e:
						self.return_a(e)

			for l in a_data["user"]["lamba_ac"]:
				if l in query.lower():
					lamp = None
					lamp2 = None
					if "ışığını" in l:
						if "ve" in query.lower():
							lamp_re = re.search('(.+) ve (.+)ışığını',query)
							lamp = lamp_re.group(1)
							lamp2 = lamp_re.group(2)
						else:
							lamp_re = re.search('(.+) ışığını',query)
							lamp = lamp_re.group(1)
							
					if "lambasını" in  l:
						if "ve" in query.lower():
							lamp_re = re.search('(.+) ve (.+) lambasını',query)
							lamp = lamp_re.group(1)
							lamp2 = lamp_re.group(2)
						else:
							lamp_re = re.search('(.+) lambasını',query)
							lamp = lamp_re.group(1)

					if "odasının" in lamp:
						lampL = lamp.split(" ")
						lampL[lampL.index("odasının")+1] = "odası"
						lampL[lampL.index("odasının")] = " "
						lampp = "".join(lampL)
					elif "mutfağın" in lamp:
						lampp = "mutfak"
					else:
						lampp = lamp.replace("un", "").replace("in", "")

					if lamp2:
						if "odasının" in lamp2:
							lampL2 = lamp2.split(" ")
							lampL2[lampL2.index("odasının")+1] = "odası"
							lampL2[lampL2.index("odasının")] = " "
							lampp2 = "".join(lampL2)
						elif "mutfağın" in lamp2:
							lampp2 = "mutfak"
						else:
							lampp2 = lamp2.replace("un", "").replace("in", "")
							
					if lamp2:
						print(lamp)
						print(lampp)
						print(lamp2)
						print(lampp2)

						if w:
							self.return_a_w_msg(query, lamp+" ve "+lamp2+" ışığı açılıyor")
						else:
							self.return_a_w_msg(query, lamp+" ve "+lamp2+" ışığı açılıyor")
							
					else:
						print(lamp)
						print(lampp)

						if w:
							self.return_a_w_msg(query, lamp+"ışığı açılıyor")
						else:
							self.return_a_w_msg(query, lamp+"ışığı açılıyor")
							
					on = False

			for l in a_data["user"]["lamba_kapat"]:
				if l in query.lower():
					lamp = None
					lamp2 = None
					if "ışığını" in l:
						if "ve" in query.lower():
							lamp_re = re.search('(.+) ve (.+) ışığını',query)
							lamp = lamp_re.group(1)
							lamp2 = lamp_re.group(2)
						else:
							lamp_re = re.search('(.+) ışığını',query)
							lamp = lamp_re.group(1)
							
					if "lambasını" in  l:
						if "ve" in query.lower():
							lamp_re = re.search('(.+) ve (.+) lambasını',query)
							lamp = lamp_re.group(1)
							lamp2 = lamp_re.group(2)
						else:
							lamp_re = re.search('(.+) lambasını',query)
							lamp = lamp_re.group(1)

					if "odasının" in lamp:
						lampL = lamp.split(" ")
						lampL[lampL.index("odasının")+1] = "odası"
						lampL[lampL.index("odasının")] = " "
						lampp = "".join(lampL)
					elif "mutfağın" in lamp:
						lampp = "mutfak"
					else:
						lampp = lamp.replace("un", "").replace("in", "")

					if lamp2:
						if "odasının" in lamp2:
							lampL2 = lamp2.split(" ")
							lampL2[lampL2.index("odasının")+1] = "odası"
							lampL2[lampL2.index("odasının")] = " "
							lampp2 = "".join(lampL2)
						elif "mutfağın" in lamp2:
							lampp2 = "mutfak"
						else:
							lampp2 = lamp2.replace("un", "").replace("in", "")
							
					if lamp2:
						print(lamp)
						print(lampp)
						print(lamp2)
						print(lampp2)

						if w:
							self.return_a_w_msg(query, lamp+" ve "+lamp2+" ışığı kapatılıyor")
						else:
							self.return_a_w_msg(query, lamp+" ve "+lamp2+" ışığı kapatılıyor")
							
					else:
						print(lamp)
						print(lampp)

						if w:
							self.return_a_w_msg(query, lamp+"ışığı kapatılıyor")
						else:
							self.return_a_w_msg(query, lamp+"ışığı kapatılıyor")
						
					on = False

			for l in a_data["user"]["kapi_kilit_ac"]:
				if l == query.lower():
					if w:
						self.return_a_w_msg(query, "Kapı kilidi açılıyor")
					else:
						self.return_a_w_msg(query, "Kapı kilidi açılıyor")
						
					on = False

			for l in a_data["user"]["kapi_kilit_kapat"]:
				if l == query.lower():
					if w:
						self.return_a_w_msg(query, "Kapı kilidi kapatılıyor")
					else:
						self.return_a_w_msg(query, "Kapı kilidi kapatılıyor")
						
					on = False

			for l in a_data["user"]["fan_ac"]:
				if l == query.lower():
					if w:
						self.return_a_w_msg(query, "Fan açılıyor")
					else:
						self.return_a_w_msg(query, "Fan açılıyor")
						
					on = False

			for l in a_data["user"]["fan_kapat"]:
				if l == query.lower():
					if w:
						self.return_a_w_msg(query, "Fan kapatılıyor")
					else:
						self.return_a_w_msg(query, "Fan kapatılıyor")
						
					on = False

			if on:
				if w:
					self.return_a_w_msg(query, query+" Google'da aranıyor.")
					web.search_google(query)
				else:
					if query == "None":
						text = "Ses Tanıma Hatası"
						self.return_a(text)
					else:
						self.return_a(query+" Google'da aranıyor.")
						web.search_google(query)

		def return_a_w_msg(self,query,text):
			if query == "none":
				text = "Ses Tanıma Hatası"
				ses.tts(text)
				self.ui.textEdit.append('<br><span style="color:#0000FF">Asistan</span> ==> '+text+'')

			else:
				ses.tts(text)
				self.ui.textEdit.append('<br><span style="color:#0000FF">Sen</span> ==> '+query+'<br><span style="color:#0000FF">Asistan</span> ==> '+text)

		def return_a_w_msg2(self,query):
			if query == "none":
				text = "Ses Tanıma Hatası"
				ses.tts(text)
				self.ui.textEdit.append('<br><span style="color:#0000FF">Asistan</span> ==> '+text)

			else:
				self.ui.textEdit.append('<br><span style="color:#0000FF">Sen</span> ==> '+query)

		def return_a_w_msg3(self,text):
			ses.tts(text)
			self.ui.textEdit.append('<span style="color:#0000FF">Asistan</span> ==> '+text)

		def return_a(self,text):
			ses.tts(text)

		def lampF(self):
			icon_on = QtGui.QIcon()
			icon_on.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/lamp_on.png"), QtGui.QIcon.Normal)

			icon_off = QtGui.QIcon()
			icon_off.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/lamp_off.png"), QtGui.QIcon.Normal)

			if data["lamp"]["status"] == "true":
				data["lamp"]["status"] = "false"
				self.ui.lampB.setIcon(icon_off)
				upload_data(data)
			elif data["lamp"]["status"] == "false":
				data["lamp"]["status"] = "true"
				data["lamp"]["last_work"] = time.strftime("%d.%m.%Y %H:%M")
				self.ui.lampB.setIcon(icon_on)
				upload_data(data)

		def fanF(self):
			icon_on = QtGui.QIcon()
			icon_on.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/fan_on.png"), QtGui.QIcon.Normal)

			icon_off = QtGui.QIcon()
			icon_off.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/fan_off.png"), QtGui.QIcon.Normal)

			if data["fan"]["status"] == "true":
				data["fan"]["status"] = "false"
				self.ui.fanB.setIcon(icon_off)
				upload_data(data)
			elif data["fan"]["status"] == "false":
				data["fan"]["status"] = "true"
				data["fan"]["last_work"] = time.strftime("%d.%m.%Y %H:%M")
				self.ui.fanB.setIcon(icon_on)
				upload_data(data)

		def doorF(self):
			icon_on = QtGui.QIcon()
			icon_on.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/door_locked.png"), QtGui.QIcon.Normal)

			icon_off = QtGui.QIcon()
			icon_off.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/door_opened.png"), QtGui.QIcon.Normal)

			if data["door_lock"]["status"] == "true":
				data["door_lock"]["status"] = "false"
				self.ui.doorB.setIcon(icon_off)
				upload_data(data)
			elif data["door_lock"]["status"] == "false":
				data["door_lock"]["status"] = "true"
				data["door_lock"]["last_lock_date"] = time.strftime("%d.%m.%Y %H:%M")
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
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/lamp_on.png"), QtGui.QIcon.Normal)
						win.ui.lampB.setIcon(icon)
					elif data[i]["status"] == "false":
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/lamp_off.png"), QtGui.QIcon.Normal)
						win.ui.lampB.setIcon(icon)
					else:
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/error.png"), QtGui.QIcon.Normal)
						win.ui.lampB.setIcon(icon)
				elif i == "fan":
					if data[i]["status"] == "true":
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/fan_on.png"), QtGui.QIcon.Normal)
						win.ui.fanB.setIcon(icon)
					elif data[i]["status"] == "false":
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/fan_off.png"), QtGui.QIcon.Normal)
						win.ui.fanB.setIcon(icon)
					else:
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/error.png"), QtGui.QIcon.Normal)
						win.ui.fanB.setIcon(icon)
				elif i == "door_lock":
					if data[i]["status"] == "true":
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/door_locked.png"), QtGui.QIcon.Normal)
						win.ui.doorB.setIcon(icon)
					elif data[i]["status"] == "false":
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/door_opened.png"), QtGui.QIcon.Normal)
						win.ui.doorB.setIcon(icon)
					else:
						icon = QtGui.QIcon()
						icon.addPixmap(QtGui.QPixmap(":/icons/Datas/icons/error.png"), QtGui.QIcon.Normal)
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
				if query in a_data["user"]["asistan_ac"]:
					win.return_a(choice(a_data["assistant"]["asistan_ac"]))
					query = ses.stt().lower()
					win.assistant(query)
				elif query != "cem" and "cem" in query:
					query = re.search("cem (.+)", query)
					if "group" in dir(query):
						win.assistant(query.group(1))
					else:
						win.return_a(choice(a_data["assistant"]["asistan_ac"]))
						query = ses.stt().lower()
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

except Exception as e:
	print("Hata: ",e)