try:
	import os
	import re
	import sys
	import time
	import socket
	from Modules.gui import *
	from random import choice
	from threading import Thread
	from PyQt5 import QtMultimedia
	from assistant import Assistant
	from Modules.BaseModule import ses, web

	try:
		assistant = Assistant()
		ses = ses()
		db = assistant.db
		web = web()
	except Exception as e:
		print("Hata: ",e)
		sys.exit()

	
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

			self.win_assistant(query,w=True)

		def win_assistant(self,query,w=False):
			web.close()

			text, i, ii = None, None, None

			result = assistant.get_result(query.lower())

			if isinstance(result,tuple) and len(result) == 3:
				text, i, ii = result
			elif isinstance(result,tuple) and len(result) == 2:
				text, i = result
			elif isinstance(result,str):
				text = result

			if i == "h_lar_oku":
				reminder_list = ii

				reminder_list.sort(reverse=True)

				if w:
					self.return_a_w_msg(query, text, th=False)
				else:
					self.return_a(text)

				for r in reminder_list:
					if w:
						self.return_a_w_msg3(r)
					else:
						self.return_a(r)

			elif i == "durumD":
				if w:
					self.return_a_w_msg2(query)

			elif i == "google_ac":
				if w:
					self.return_a_w_msg(query, text)
				else:
					self.return_a(text)
				web.open_google()

			elif i == "google_kapa":
				if w:
					self.return_a_w_msg(query, text)
				else:
					self.return_a(text)
				web.close()

			elif i == "youtube_ac":
				if w:
					self.return_a_w_msg(query, text)
				else:
					self.return_a(text)
				web.open_youtube()

			elif i == "youtube_kapa":
				if w:
					self.return_a_w_msg(query, text)
				else:
					self.return_a(text)
				web.close()

			elif i == "ses_seviyesi":
				r = ses.currentVolume()
				if r[1] == 0:
					status = "açık"
				elif r[1] == 1:
					status = "kapalı"
				if w:
					self.return_a_w_msg(query, text.format(r[0],status))
				else:
					self.return_a(text.format(r[0],r[1]))

			elif i == "ses_ayar":
				r = ses.setVolume(ii)
				if r:
					if w:
						self.return_a_w_msg(query, text.format(ii))
					else:
						self.return_a(text.format(ii))
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "ses_arttır2":
				r = ses.volumeUp(ii)
				if r:
					if w:
						self.return_a_w_msg(query, text.format(ii))
					else:
						self.return_a(text.format(ii))
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "ses_azalt2":
				r = ses.volumeDOWN(ii)
				if r:
					if w:
						self.return_a_w_msg(query, text.format(ii))
					else:
						self.return_a(text.format(ii))
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "ses_arttır":
				r = ses.volumeUP(5)
				if r:
					if w:
						self.return_a_w_msg(query, text)
					else:
						self.return_a(text)
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "ses_azalt":
				r = ses.volumeDOWN(5)
				if r:
					if w:
						self.return_a_w_msg(query, text)
					else:
						self.return_a(text)
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "ses_kapat":
				r = ses.volumeSetMute(True)
				if r:
					if w:
						self.return_a_w_msg(query, text)
					else:
						self.return_a(text)
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "ses_aç":
				r = ses.volumeSetMute(False)
				if r:
					if w:
						self.return_a_w_msg(query, text)
					else:
						self.return_a(text)
				else:
					if w:
						self.return_a_w_msg(query, "Malesef bir hata oluştu!")
					else:
						self.return_a("Malesef bir hata oluştu!")

			elif i == "kapi_son_kilit":
				last_lock_date = data["door_lock"]["last_lock_date"].replace("\"","")

				if w:
					self.return_a_w_msg(query, text.format(last_lock_date))
				else:
					self.return_a(text.format(last_lock_date))

			elif i == "selam_ver":
				query2 = query.split()
				del query2[-2:]

				for g in query2:
					gg = g.split("'")
					if len(gg) > 1:
						query2[query2.index(g)] = "".join(gg[0])

					elif "abla" in g:
						del query2[query2.index(g)]

					elif "abi" in g:
						del query2[query2.index(g)]

					elif g.lower() == "anneme":
						query2[query2.index(g)] = "Sevgül"

					elif g.lower() == "babama":
						query2[query2.index(g)] = "Cevdet"

				query2 = " ".join(query2)

				if w:
					self.return_a_w_msg(query, text.format(query2))
				else:
					self.return_a(text.format(query2))

			elif i == "m_g" and not w:
				while True:
					con = self.ses.stt()
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
						self.return_a("self.Ses tanıma hatası. Lütfen tekrar söylermisin.")
				try:
					self.return_a(self.mail.mailG(to, con, subj))
				except Exception as e:
					self.return_a(e)

			else:
				if w:
					self.return_a_w_msg(query, text)
				else:
					self.return_a(text)

			
		def return_a_w_msg(self,query,text,th=True):
			def say(text):
				ses.tts(text)

			if query == "none":
				text = "Ses Tanıma Hatası"

				self.ui.textEdit.append('<br><span style="color:#0000FF">Asistan</span> ==> '+text+'')

			else:
				self.ui.textEdit.append('<br><span style="color:#0000FF">Sen</span> ==> '+query+'<br><span style="color:#0000FF">Asistan</span> ==> '+text)
			
			if th:
				th = Thread(target=say,args=(text,))
				th.daemon = True
				th.start()
			else:
				say(text)

		def return_a_w_msg2(self,query,th=True):
			def say(text):
				ses.tts(text)

			if query == "none":
				text = "Ses Tanıma Hatası"
				self.ui.textEdit.append('<br><span style="color:#0000FF">Asistan</span> ==> '+text)

				if th:
					th = Thread(target=say,args=(text,))
					th.daemon = True
					th.start()
				else:
					say(text)

			else:
				self.ui.textEdit.append('<br><span style="color:#0000FF">Sen</span> ==> '+query)

			

		def return_a_w_msg3(self,text,th=True):
			def say(text):
				ses.tts(text)

			self.ui.textEdit.append('<span style="color:#0000FF">Asistan</span> ==> '+text)

			if th:
				th = Thread(target=say,args=(text,))
				th.daemon = True
				th.start()
			else:
				say(text)

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
				data["lamp"]["last_work"] = "\""+time.strftime("%d.%m.%Y %H:%M")+"\""
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
				data["fan"]["last_work"] = "\""+time.strftime("%d.%m.%Y %H:%M")+"\""
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
				data["door_lock"]["last_lock_date"] = "\""+time.strftime("%d.%m.%Y %H:%M")+"\""
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

		def cem():
			global a_data
			global win
			while True:
				a_data = assistant.a_data()
				query = ses.stt().lower()
				if query in a_data["user"]["asistan_ac"]:
					win.return_a(choice(a_data["assistant"]["asistan_ac"]))
					query = ses.stt()
					win.win_assistant(query)
				elif query != "cem" and "cem" in query:
					query = re.search("cem (.+)", query)
					if "group" in dir(query):
						win.win_assistant(query.group(1))
					else:
						win.return_a(choice(a_data["assistant"]["asistan_ac"]))
						query = ses.stt()
						win.win_assistant(query)


		th_check = Thread(target=check)
		th_check.daemon = True
		th_check.start()

		th_reji = Thread(target=cem)
		th_reji.daemon = True
		th_reji.start()

		update_info()


		#face_recognition.start()
		#ses.tts("selam "+face_recognition.result)

		sys.exit(app.exec())

except Exception as e:
	print("Hata: ",e)