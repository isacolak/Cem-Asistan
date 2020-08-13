try:
	import os
	import re
	import time
	import json
	from random import choice
	from threading import Thread
	from datetime import date,datetime
	from Modules.BaseModule import ses, hava, reminders, mail, doviz, data_base, FaceRecognition, web

except ImportError as e:
	print(e)


class Assistant:
	def __init__(self):
		super().__init__()

		self.start()

		self.ses = ses()
		self.hava = hava()
		self.hatirlatici = reminders()
		self.mail = mail()
		self.doviz = doviz()
		self.db = data_base().db
		self.face_recognition = FaceRecognition()
		self.web = web()

		self.haftaGün = {'1':'Pazartesi','2':'Salı','3':'Çarşamba','4':'Perşembe','5':'Cuma','6':'Cumartesi','7':'Pazar'}
		self.yılAy = {'01':'Ocak','02':'Şubat','03':'Mart','04':'Nisan','05':'Mayıs','06':'Haziran','07':'Temmuz','08':'Ağustos','09':'Eylül','10':'Ekim','11':'Kasım','12':'Aralık'}

		self.dayToGün = {"Mon":"Pazartesi","Tue":"Salı","Wed":"Çarşamba","Thu":"Perşembe","Fri":"Cuma","Sat":"Cumartesi","Sun":"Pazar"}
		self.monToAy = {"Jan":"Ocak","Feb":"Şubat","Mar":"Mart","Apr":"Nisa","May":"Mayıs","Jun":"Haziran","Jul":"Temmuz","Aug":"Ağustos","Sep":"Eylül","Oct":"Ekim","Nov":"Kasım","Dec":"Aralık"}

	def remove_file(self,path):
		os.remove(path)

	def start(self):
		dir_name = "Datas/sounds/"
		s = 0
		for i in os.listdir(dir_name):
			th = Thread(target=self.remove_file,args=(dir_name+i,))
			th.daemon = True
			th.start()
			s += 1

	def info(self):
		return json.load(open('Datas/info.json','r',encoding="utf-8"))

	def a_data(self):
		return json.load(open("Datas/a_data.json","r",encoding="utf-8"))

	def get_result(self,query):
		self.web.close()

		a_data = self.a_data()

		on = True

		for i in a_data["user"]:
			if query.lower() in a_data["user"][i]:
				on = False
				if i == "geliştirici":
					return (choice(a_data["assistant"][i]),i)
						
				elif i == "saat":
					return (a_data["assistant"][i].format(time.strftime("%H:%M")),i)
						
				elif i == "tarih":
					return (a_data["assistant"][i].format(time.strftime("%d"),self.yılAy[time.strftime("%m")],self.haftaGün[time.strftime("%w")]),i)
						
				elif i == "durum":
					return (choice(a_data["assistant"][i]),i)
							
				elif i == "durumD":
					return (None,i)
							
				elif i == "iltifat":
					return (choice(a_data["assistant"][i]),i)
							
				elif i == "yil":
					return (a_data["assistant"][i].format(time.strftime("%Y")),i)
							
				elif i == "gun2":
					return (a_data["assistant"][i].format(self.haftaGün[time.strftime("%w")]),i)
							
				elif i == "hava":
					il,ilce,havad = self.hava.havaD()

					return (a_data["assistant"][i].format(il+" "+ilce if ilce else il,havad),i)
							
				elif i == "havaY":
					il,ilce,havad = self.hava.havaDY()

					return (a_data["assistant"][i].format(il+" "+ilce if ilce else il,havad),i)
							
				elif i == "doviz":
					return (self.doviz.doviz(),i)

				elif i == "ses_arttır":
					self.ses.volumeUP(5)
					return (a_data["assistant"][i],i)

				elif i == "ses_azalt":
					self.ses.volumeDOWN(5)
					return (a_data["assistant"][i],i)

				elif i == "ses_kapat":
					self.ses.volumeSetMute(True)
					return (a_data["assistant"][i],i)

				elif i == "ses_aç":
					self.ses.volumeSetMute(False)
					return (a_data["assistant"][i],i)

				elif i == "ses_seviyesi":
					r = self.ses.currentVolume()
					return (a_data["assistant"][i],i,r)
						
				elif i == "google_ac":
					return ("Google açılıyor",i)
						
				elif i == "google_kapa":
					return ("Google kapatılıyor",i)
						
				elif i == "youtube_ac":
					return ("Youtube açılıyor",i)
						
				elif i == "youtube_kapa":
					return ("Youtube kapatılıyor",i)
						
				elif i == "h_lar_oku":

					reminders = self.hatirlatici.read_reminders()

					reminders_count = 0

					for d in reminders:
						reminders_count += len(reminders[d])

					reminder_list = []

					for d in reminders:
						g,a,y = d.split(".")
						sp = date(int(y),int(a),int(g)).ctime().split(" ")
						g2 = self.dayToGün[sp[0]]
						a2 = self.monToAy[sp[1]]

						if date(int(y),int(a),int(g)).isocalendar()[1] == datetime.now().isocalendar()[1]:
							for t in reminders[d]:
								reminder_list.append(self.haftaGün[str(date(int(y),int(a),int(g)).isocalendar()[2])]+", "+t+", "+reminders[d][t])
						else:
							for t in reminders[d]:
								reminder_list.append(d+", "+t+", "+reminders[d][t])

					return ("Toplam "+str(reminders_count)+" tane hatırlatıcı bulunuyor.",i,reminder_list)

				elif i == "h_oluş":
					return ("Lütfen hatırlatıcının tarihini söylermisin. Örneğin 20 Mart saat 11:25 balo.",i)
								
					while True:
						r_data =  self.ses.stt()

						if r_data != "None":
							break
						else:
							return ("self.Ses tanıma hatası. Lütfen tekrar söylermisin.",i)

					print(r_data)


		for s in a_data["user"]["m_g"]:
			if s in query.lower():
				on = False
				to = re.search('(.+) '+s, query).group(1).split("'")[0]
				return ("Lütfen e-postanın içeriğini söylermisin.","m_g")

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

					return (lamp+" ve "+lamp2+" ışığı açılıyor","lamba_ac")
							
				else:
					print(lamp)
					print(lampp)

					return (lamp+"ışığı açılıyor","lamba_ac")
							
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

					return (lamp+" ve "+lamp2+" ışığı kapatılıyor","lamba_kapat")
							
				else:
					print(lamp)
					print(lampp)

					return (lamp+"ışığı kapatılıyor","lamba_kapat")
						
				on = False

		for l in a_data["user"]["kapi_kilit_ac"]:
			if l == query.lower():
				return ("Kapı kilidi açılıyor","kapi_kilit_ac")
						
				on = False

		for l in a_data["user"]["kapi_kilit_kapat"]:
			if l == query.lower():
				return ("Kapı kilidi kapatılıyor","kapi_kilit_kapat")
						
				on = False

		for l in a_data["user"]["fan_ac"]:
			if l == query.lower():
				return ("Fan açılıyor","fan_ac")
						
				on = False

		for l in a_data["user"]["fan_kapat"]:
			if l == query.lower():
				return ("Fan kapatılıyor","fan_kapat")
						
				on = False
		"""
		if on:
			if False:
				return (query, query+" Google'da aranıyor.",i)
				self.web.search_google(query)
			else:
				if query == "None":
					text = "self.Ses Tanıma Hatası"
					return (text,i)
				else:
					return (query+" Google'da aranıyor.",i)
					self.web.search_google(query)
		"""

		s = query.split()

		if len(s) == 4:
			l = s[-2]

			if query == a_data["user"]["ses_ayar"].format(l):
				return (a_data["assistant"]["ses_ayar"],"ses_ayar",int(l))

		elif len(s) == 3:
			l = s[-2]

			if query == a_data["user"]["ses_arttır2"].format(l):
				return (a_data["assistant"]["ses_arttır2"],"ses_arttır2",int(l))

			elif query == a_data["user"]["ses_azalt2"].format(l):
				return (a_data["assistant"]["ses_azalt2"],"ses_azalt2",int(l))

		return "Anlamadım."

