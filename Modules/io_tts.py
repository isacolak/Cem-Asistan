import requests
from bs4 import BeautifulSoup

class io_TTS:
	def __init__(self, text):

		self.base_url = "https://freetts.com/Home/PlayAudio?Language=tr-TR&Voice=tr-TR-Standard-B&TextMessage={}&id=undefined&type=0"

		self.sound_base_url = "https://freetts.com"

		self.url = self.base_url.format(text)

		self.req = requests.get(self.url)

		if self.req.status_code == 200:

			soup = BeautifulSoup(self.req.content,"html.parser")

			if soup.find_all("audio")[0].source["src"]:

				audio_src = soup.find_all("audio")[0].source["src"]

				file_url = self.sound_base_url+audio_src

				self.file_req = requests.get(file_url,stream=True)

			else:
				raise Exception("TTS Kullanım Sınırına Ulaşıldı!")
		else:
			raise Exception("TTS Sunucusuna Erişilemedi!")

	def save(self,file_path):
		with open(file_path,"wb") as f:
			for i in self.file_req.iter_content():
				f.write(i)
			f.close()

	def play_without_save(self):
		import io
		import wave
		import pyaudio
		import miniaudio

		self.src = miniaudio.decode(self.file_req.content, dither=miniaudio.DitherMode.TRIANGLE)

		with io.BytesIO() as file:
			wave_file = wave.open(file,"wb")
			try:
				wave_file.setnchannels(self.src.nchannels)
				wave_file.setsampwidth(self.src.sample_width)
				wave_file.setframerate(self.src.sample_rate)
				wave_file.writeframes(self.src.samples.tobytes())
				wave_data = file.getvalue()
			finally:
				wave_file.close()

		with io.BytesIO(wave_data) as file:
			p = pyaudio.PyAudio()
			f = wave.open(file,"rb")
			try:
				stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
								channels = f.getnchannels(),
								rate = f.getframerate(),
								output = True
				)

				data = f.readframes(1024)
 
				while data:
					stream.write(data)
					data = f.readframes(1024)

			finally:
				stream.stop_stream()
				stream.close()
				p.terminate()
				f.close()