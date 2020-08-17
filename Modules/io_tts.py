import io
import wave
import requests
import miniaudio
import soundfile as sf
import sounddevice as sd

url = "https://translate.google.com/translate_tts?ttsspeed=1&textlen=8&client=tw-ob&idx=0&tk=95822.511418&ie=UTF-8&total=1&q=saat şuan 18:05&tl=tr"
urlo = requests.get(url)

src = miniaudio.decode(urlo.content, dither=miniaudio.DitherMode.TRIANGLE)


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
sd.wait()

# import pyaudio 

# #define stream chunk   
# chunk = 1024  

# #instantiate PyAudio  
# p = pyaudio.PyAudio()  
# #open stream  
	

# with io.BytesIO(wave_data) as file:
# 	f = wave.open(file,"rb")
# 	try:
# 		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
# 	                channels = f.getnchannels(),  
# 	                rate = f.getframerate(),  
# 	                output = True)  
# 		#read data  
# 		data = f.readframes(chunk)  

# 		#play stream  
# 		while data:  
# 		    stream.write(data)  
# 		    data = f.readframes(chunk)  

# 		#stop stream  
# 		stream.stop_stream()  
# 		stream.close()  

# 		#close PyAudio  
# 		p.terminate()  
# 	finally:
# 		f.close()
