import io
import os
import re
from . import gsr
import cv2
import wave
import time
import math
import json
import pickle
import smtplib
import requests
import warnings
import miniaudio
#import webbrowser
import numpy as np
import firebase_admin
from gtts import gTTS
import soundfile as sf
import sounddevice as sd
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from comtypes import CLSCTX_ALL
from playsound import playsound
import speech_recognition as sr
from ctypes import cast, POINTER
from email.mime.text import MIMEText
from firebase_admin import credentials, db
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.options import Options
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

files = pickle.load(open("Datas/files","rb"))

cred_json = files["firebase"]

def info():
	return json.load(open('Datas/info.json','r',encoding="latin5"))

def a_data():
	return json.load(open("Datas/a_data.json","r",encoding="latin5"))

iinfo = info()

def remove_file(path):
	os.remove(path)

def start():
	dir_name = "Datas/sounds/"
	s = 0
	for i in os.listdir(dir_name):
		th = Thread(target=remove_file,args=(dir_name+i,))
		th.daemon = True
		th.start()
		s += 1

start()

class hava:
	def __init__(self):
		self.ilce = None
		self.il = None

	def havaD(self,il=iinfo['konum']["il"],ilce=None):
		if il != iinfo['konum']["il"]:
			self.il = il
			self.ilce = ilce
		else:
			self.il = iinfo['konum']["il"]
			self.ilce = iinfo['konum']["ilce"]

		if self.ilce:
			url = "https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il="+self.il+"&ilce="+self.ilce
		else:
			url = "https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il="+self.il

		warnings.filterwarnings("ignore")

		driver = webdriver.PhantomJS("Datas/selenium/phantomjs.exe")

		driver.get(url)

		if driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[5]/div[1]/div[2]/div[2]").text and driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[5]/div[1]/div[1]").text:
			weather_info = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[5]/div[1]/div[2]/div[2]").text
			weather_degree = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[5]/div[1]/div[1]").text

			driver.quit()

			return self.il,self.ilce,weather_info+' '+weather_degree
		else:
			driver.quit()
			return self.il,self.ilce,None
		
	def havaDY(self,il=iinfo['konum']["il"],ilce=iinfo['konum']["ilce"]): 
		if il != iinfo['konum']["il"]:
			self.il = il
			self.ilce = ilce
		else:
			self.il = iinfo['konum']["il"]
			self.ilce = iinfo['konum']["ilce"]

		if self.ilce:
			url = "https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il="+self.il+"&ilce="+self.ilce
		else:
			url = "https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il="+self.il

		warnings.filterwarnings("ignore")

		driver = webdriver.PhantomJS("Datas/selenium/phantomjs.exe")

		driver.get(url)

		if driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[8]/table/tbody/tr[1]/td[2]/img").get_attribute("title") and driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[8]/table/tbody/tr[1]/td[3]").text:
			weather_info = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[8]/table/tbody/tr[1]/td[2]/img").get_attribute("title")
			weather_degree = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/section/div[8]/table/tbody/tr[1]/td[3]").text

			driver.quit()

			return self.il,self.ilce,weather_info+' '+weather_degree

		else:
			driver.quit()
			return self.il,self.ilce,None

class ses:
	def __init__(self):
		self.s = 0

		self.devices = AudioUtilities.GetSpeakers()
		self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
		self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

	def sesOynat(self, audio):
		playsound(audio)

	def currentVolume(self):
		currentVolumeSc = self.volume.GetMasterVolumeLevelScalar()
		mute = self.volume.GetMute()
		return (math.ceil(currentVolumeSc*100),mute)

	def setVolume(self,vLevel):
		level = float(vLevel/100)
		if level > 1.0:
			level = 1.0
		elif level < 0.0:
			level = 0.0
		try:
			self.volume.SetMasterVolumeLevelScalar(level,None)
			return True
		except:
			return False

	def volumeUP(self,vLevel):
		vLevelSc = float(vLevel/100)
		currentVolumeSc = self.volume.GetMasterVolumeLevelScalar()
		if currentVolumeSc < 1.0:
			level = currentVolumeSc+vLevelSc
			if level > 1.0:
				level = 1.0
			try:
				self.volume.SetMasterVolumeLevelScalar(level,None)
				return True
			except:
				return False
		else:
			return False

	def volumeDOWN(self,vLevel):
		vLevelSc = float(vLevel/100)
		currentVolumeSc = self.volume.GetMasterVolumeLevelScalar()
		if currentVolumeSc > 0.0:
			level = currentVolumeSc-vLevelSc
			if level < 0.0:
				level = 0.0
			try:
				self.volume.SetMasterVolumeLevelScalar(level,None)
				return True
			except:
				return False
		else:
			return False

	def setVolumeMuted(self,mute):
		try:
			self.volume.SetMute(mute,None)
			return True
		except:
			return False
		
	def tts_g(self,text,language='tr'):
		filename = "Datas/sounds/temp"+str(self.s)+".mp3"
		self.s += 1
		ttss = gTTS(text,lang=language)
		ttss.save(filename)
		self.sesOynat(filename)

	def tts1(self,text,lang="tr"):
		file_name = "Datas/sounds/temp"+str(self.s)+".mp3"
		self.s += 1

		url = "https://translate.google.com/translate_tts?ttsspeed=1&textlen=8&client=tw-ob&idx=0&tk=95822.511418&ie=UTF-8&total=1&q="+text+"&tl="+lang
		urlo = requests.get(url)

		with open(file_name,"wb") as f:
			for i in urlo.iter_content():
				f.write(i)
			f.close()

		self.sesOynat(file_name)

	def tts(self,text):
		file_name = "Datas/sounds/temp"+str(self.s)+".mp3"
		self.s += 1

		base = "https://freetts.com"
		url = "https://freetts.com/Home/PlayAudio?Language=tr-TR&Voice=tr-TR-Standard-B&TextMessage="+text+"&id=undefined&type=0"

		req = requests.get(url)

		if req.status_code == 200:

			soup = BeautifulSoup(req.text,"html.parser")

			if soup.find_all("audio")[0].source["src"]:

				audio_src = soup.find_all("audio")[0].source["src"]

				file_url = base+audio_src

				file_req = requests.get(file_url,stream=True)

				src = miniaudio.decode(file_req.content, dither=miniaudio.DitherMode.TRIANGLE)

				with io.BytesIO() as file:
					wave_file = wave.open(file,"wb")
					try:
						wave_file.setnchannels(src.nchannels)
						wave_file.setsampwidth(src.sample_width)
						wave_file.setframerate(src.sample_rate)
						wave_file.writeframes(src.samples.tobytes())
						wave_data = file.getvalue()
					finally:
						wave_file.close()

				data, fs = sf.read(io.BytesIO(wave_data))

				sd.play(data, fs)
				status = sd.wait()

			else:
				raise Exception("TTS Kullanım Sınırına Ulaşıldı!")
		else:
			raise Exception("TTS Sunucusuna Erişilemedi!")

	def tts2(self,text):
		os.system("python Modules/tts.py "+text)

	def stt2(self,lang='tr-Tr'): 
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("\nDinleniyor...")
			r.pause_threshold = 1
			audio = r.listen(source)
		
		try:
			print("Tanımlanıyor...")
			query = r.recognize_google(audio, language=lang)
			print("Bunu Söyledin : " + query+"\n")
		
		except Exception as e:
			print(e)
			print("Lütfen Tekrarla...")
			query = "None"
		return query

	def stt(self, lang="tr-Tr"):
		print("Dinleniyor...\n")
		audio = gsr.listen()
		print("Tanımlanıyor...\n")
		try:
			query = gsr.recognize(audio)
			print("Şunu Söyledin:",query,"\n")
		except Exception as e:
			print(e)
			print("Lütfen Tekrarla...\n")
			query = "None"
		return query

class hatırlatıcı1:
	def __init__(self):
		self.Tarih = time.strftime("%d.%m.%Y")
		self.Saat = time.strftime("%H:%M")
		with open('Datas/reminders.json','r') as ajs:
			self.hatirla = json.load(ajs)
			ajs.close()
	def ayNC(self,tarih):
		aylar = {'ocak':'01','şubat':'02','mart':'03','nisan':'04','mayıs':'05','haziran':'06','temmuz':'07','ağustos':'08','eylül':'09','ekim':'10','kasım':'11','aralık':'12'}
		ay = tarih.split()
		for c in ay:
			if c.lower() in aylar:
				return ay[0]+'.'+aylar[c.lower()]+'.'+ay[2]
			else:
				pass
		return tarih
	
	def günHatırlatıcı(self,tarih):
		hatirla = self.hatirla
		if len(hatirla)>0:
			if len(hatirla[tarih])>0:
				try:
					for s in hatirla[tarih]['saat']:
						return s+' '+hatirla[tarih]['saat'][s]
				except:
					pass
			else:
				return
		else:
			return 'Hiç Hatırlatmanız Yok'

	def hatırlatıcılar(self):
		hatirla = self.hatirla
		if len(hatirla)>0:
			for t in hatirla:
				if len(t)>0:
					try:
						for s in hatirla[t]['saat']:
							c = '{} Saat {} {}'.format(t,s,hatirla[t]['saat'][s])
							return (c)                    
					except:
						pass
				else:
					pass
		else:
			return('Hiç Hatırlatmanız Yok')

	def hatırlatıcıO(self,tarih, saat,ad):
		tarih = ayNC(tarih)
		hatirla = self.hatirla
		if tarih in hatirla:
			if 'saat' in hatirla[tarih]:
				hatirla[tarih]['saat'][saat] = ad
			else:
				hatirla[tarih]['saat'] = {}
				hatirla[tarih]['saat'][saat] = ad
		else:
			hatirla[tarih] = {}
			hatirla[tarih]['saat'] = {}
			hatirla[tarih]['saat'][saat] = ad
		with open('Datas/reminders.json','w') as wjs:
			json.dump(hatirla,wjs,indent=4)
			wjs.close()

	def hatırlatıcıS(self,tarih,ad):
		hatirla = self.hatirla
		if tarih in hatirla:
			if len(hatirla[tarih])<=0:
				print('Böyle Bir Hatırlatıcı Zaten Bulunmuyor')
			else:
				try:
					for s in hatirla[tarih]['saat']:
						if ad == hatirla[tarih]['saat'][s]:
							del hatirla[tarih]['saat']
							if len(hatirla[tarih]['saat'])<0:
								del hatirla[tarih]
								print('j')
						else:
							pass
				except:
					pass
				with open('Datas/reminders.json','w') as wjs:
					json.dump(hatirla,wjs,indent=4)
					wjs.close()
		else:
			print('Böyle Bir Hatırlatıcı Zaten Bulunmuyor')

class reminders:
	def __init__(self):
		self.Tarih = time.strftime("%d.%m.%Y")
		self.Saat = time.strftime("%H:%M")

		self.reminders = pickle.load(open("Datas/reminders","rb"))

	def read_reminders(self):
		self.reminders = pickle.load(open("Datas/reminders","rb"))
		return self.reminders

	def read_reminder(self,r_date):
		self.reminders = pickle.load(open("Datas/reminders","rb"))

		if r_date in self.reminders:
			return self.reminders[r_date]
		else:
			return r_date+" tarihinde hiç hatırlatıcı bulunmuyor."

	def create_reminder(self,r_date,r_time,r_con):
		if r_date not in self.reminders:
			self.reminders[r_date] = {r_time:r_con}

			pickle.dump(self.reminders, open("Datas/reminders","wb"))

			self.reminders = pickle.load(open("Datas/reminders","rb"))
		else:
			if isinstance(self.reminders[r_date], dict):
				self.reminders[r_date][r_time] = r_con

				pickle.dump(self.reminders, open("Datas/reminders","wb"))

				self.reminders = pickle.load(open("Datas/reminders","rb"))

class mail:
	def __init__(self):
		self.mails = json.load(open('Datas/mails.json','r'))

	def mailG(self,to, content, subject=None):
		self.mails = json.load(open('Datas/mails.json','r'))

		if to in self.mails:
			message = MIMEMultipart()
			message["From"] = "isacolak04@gmail.com"  # Mail'i gönderen kişi
			message["To"] = self.mails[to]  # Mail'i alan kişi
			message["Subject"] = subject  # Mail'in konusu
		
			body = content  # Mail içerisinde yazacak içerik
			body_text = MIMEText(body, "plain")
		
			message.attach(body_text)
		
			# Gmail serverlerine bağlanma işlemi.
		
			try:
				mail = smtplib.SMTP("smtp.gmail.com", 587)
				mail.ehlo()
				mail.starttls()
				mail.login("isacolak04@gmail.com", "isaBaran2005")  # Maili gönderirken kullanılıcak hesap ve şifresi
				mail.sendmail(message["From"], message["To"], message.as_string())
				mail.close()
			
				return "Mail Başarılı bir şekilde gönderildi."
			except:
				raise Exception("Bir hata oluştu. Tekrar deneyin...")
		else:
			raise Exception( to+' Adlı Kişinin Mail Adresi Kayıtlı Değil')

class doviz:
	def doviz(self):
		url = "https://m.doviz.com/"
		try:
			url_r = requests.get(url)
			soup = BeautifulSoup(url_r.text, 'html.parser')
			h = soup.find_all("span", class_="value")
			if h:
				usd = 'Amerikan Doları '+h[0].text[:4]+' TL'
				euro = 'Euro '+h[1].text[:4]+' TL'
				return usd+' '+euro+'.'
			else:
				return "Döviz bilgisi alınamadı."
		except:
			return 'Hata. Lütfen İnsternet Bağlantınızı Kontrol Edin.'

class data_base:
	def __init__(self):
		cred = credentials.Certificate(cred_json)
		firebase_admin.initialize_app(cred,{"databaseURL" : "https://cemassistant-68b2a.firebaseio.com"})

		self.db = db

class FaceRecognition:
	def __init__(self):

		self.tani = cv2.face.LBPHFaceRecognizer_create()
		self.tani.read("Datas/face_recognition/datas/trainer.yml")

		self.faceCascade = cv2.CascadeClassifier("Datas/face_recognition/datas/cascades/haarcascade_frontalface_default.xml")

		self.idd = 0

		self.dictionary = {}

		self.names = []

		dosya = open("Datas/face_recognition/datas/ids.json")

		self.dictionary = json.load(dosya)

		for key,value in self.dictionary.items():
			self.names.append(key)

		self.on = True

	def start(self):
		self.cam = cv2.VideoCapture(0)
		
		while self.on:
			ret,cerceve = self.cam.read()
			cerceve = cv2.flip(cerceve, 1)
			gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)

			faces = self.faceCascade.detectMultiScale(gri,scaleFactor=1.5,minNeighbors=5)

			for (x,y,w,h) in faces:
				cv2.rectangle(cerceve, (x,y), (x+w,y+h), (0,255,0),2)
				self.idd,self.oran = self.tani.predict(gri[y:y+h,x:x+w])

				if (self.oran >= 50):
					self.idd = self.names[self.idd]
					self.on = False
					self.cam.release()
					print(self.idd)
					self.result = self.idd
				else:
					self.idd = "Bilinmiyor"

class web2:
	def __init__(self):
		self.youtube_base = "https://www.youtube.com"
	def open_youtube(self):
		webbrowser.open("https://www.youtube.com")

	def open_video_youtube(self,query):
		query = query.replace(" ","+")
		url = "https://www.youtube.com/results?search_query="+query

		req = requests.get(url)

		soup = BeautifulSoup(req.text,"html.parser")

		a = soup.find_all("a","yt-uix-tile-link")

		webbrowser.open(self.youtube_base+a[0].get("href"))

	def search_youtube(self,query):
		query = query.replace(" ","+")
		webbrowser.open("https://www.youtube.com/results?search_query="+query)

	def open_google(self):
		webbrowser.open("https://www.google.com")

	def search_google(self,query):
		query = query.replace(" ","+")
		webbrowser.open("https://www.google.com/search?q="+query)

	def close(self):
		os.system("taskkill /F /IM chrome.exe")

class web:
	def __init__(self):
		self.adBlock_path = 'Datas/selenium/uBlockOrigin.crx'
		self.driver_path = 'Datas/selenium/chromedriver.exe'
		self.driver = None

		self.options = webdriver.ChromeOptions()
		self.options.add_extension(self.adBlock_path)
	def open_google(self):
		if self.driver != None:
			self.driver.quit()
			self.driver = None
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		elif self.driver == None:
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		
		self.driver.get("https://www.google.com")

	def search_google(self,query):
		if self.driver != None:
			self.driver.quit()
			self.driver = None
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		elif self.driver == None:
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		
		query = query.replace(" ","+")
		self.driver.get("https://www.google.com/search?q="+query)

	def open_youtube(self):
		if self.driver != None:
			self.driver.quit()
			self.driver = None
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		elif self.driver == None:
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		
		self.driver.get("https://www.youtube.com")

	def search_youtube(self,query):
		if self.driver != None:
			self.driver.quit()
			self.driver = None
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		elif self.driver == None:
			self.driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=self.options)
		
		query = query.replace(" ","+")
		self.driver.get("https://www.youtube.com/results?search_query="+query)

	def play_video(self,video_number):
		if self.driver != None:
			video = self.driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{}]".format(video_number)).click()
		else:
			print("Driver Oluşturulmamış")

	def playList(self):
		pass
	
	def close(self):
		if self.driver:
			self.driver.quit()
			self.driver = None