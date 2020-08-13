import requests

url = "https://translate.google.com/translate_tts?ttsspeed=1&textlen=8&client=tw-ob&idx=0&tk=95822.511418&ie=UTF-8&total=1&q=Merhaba&tl=tr"

urlo = requests.get(url,stream=True)

with open("hh.mp3","wb") as f:
	for i in urlo.iter_content():
		f.write(i)
	f.close()
