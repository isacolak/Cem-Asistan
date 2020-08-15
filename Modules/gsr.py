import os
import io
import wave
import math
import json
import audioop
import pyaudio
import subprocess
import collections
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

class RequestError(Exception): pass
class RecognitionError(Exception): pass

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SAMPLE_WIDTH = pyaudio.get_sample_size(FORMAT)
RECORD_SECONDS = 5


def listen():
	audio = pyaudio.PyAudio()

	stream = audio.open(format=FORMAT, channels=CHANNELS,
					rate=RATE, input=True,
					frames_per_buffer=CHUNK)

	buffer = b""

	seconds_per_buffer = float(CHUNK) / RATE
	pause_buffer_count = int(math.ceil(1 / seconds_per_buffer))
	phrase_buffer_count = int(math.ceil(0.3 / seconds_per_buffer))
	non_speaking_buffer_count = int(math.ceil(0.5 / seconds_per_buffer))
	elapsed_time = 0
	energy_threshold = 300
	dynamic_energy_adjustment_damping = 0.15
	dynamic_energy_ratio = 1.5
	phrase_time_limit = None

	while True:
		frames = collections.deque()
		while True:
			elapsed_time += seconds_per_buffer

			buffer = stream.read(CHUNK)

			frames.append(buffer)

			if len(frames) > non_speaking_buffer_count:
				frames.popleft()

			energy = audioop.rms(buffer, SAMPLE_WIDTH)
			if energy > energy_threshold: break

			damping = dynamic_energy_adjustment_damping ** seconds_per_buffer
			target_energy = energy * dynamic_energy_ratio
			energy_threshold = energy_threshold * damping + target_energy * (1 - damping)

		phrase_count,pause_count = 0,0
		phrase_start_time = elapsed_time
		while True:
			elapsed_time += seconds_per_buffer
			if phrase_time_limit and elapsed_time - phrase_start_time > phrase_time_limit: break
			buffer = stream.read(CHUNK)

			if len(buffer) == 0: break

			frames.append(buffer)

			phrase_count += 1

			energy = audioop.rms(buffer, SAMPLE_WIDTH)

			if energy > energy_threshold :
				pause_count = 0
			else:
				pause_count += 1
			if pause_count > pause_buffer_count:
				break

		phrase_count -= pause_count

		if phrase_count >= phrase_buffer_count or len(buffer) == 0: break


	stream.stop_stream()
	stream.close()
	audio.terminate()

	with io.BytesIO() as wav_file:
		wav_writer = wave.open(wav_file,"wb")
		try:
			wav_writer.setnchannels(CHANNELS)
			wav_writer.setsampwidth(audio.get_sample_size(FORMAT))
			wav_writer.setframerate(RATE)
			wav_writer.writeframes(b''.join(frames))
			wav_data = wav_file.getvalue()
		finally:
			wav_writer.close()

	if os.name == "nt":
		startup_info = subprocess.STARTUPINFO()
		startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		startup_info.wShowWindow = subprocess.SW_HIDE
	else:
		startup_info = None

	process = subprocess.Popen(["flac","--stdout", "--totally-silent","--best","-",],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startup_info)

	flac_data, stderr = process.communicate(wav_data)

	return flac_data

def recognize(audio_data, language="tr-Tr"):

	url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
		"client": "chromium",
		"lang": language,
		"key": "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw",
	}))

	request = Request(url, data=audio_data, headers={"Content-Type": "audio/x-flac; rate={}".format(44100)})

	try:
		response = urlopen(request, timeout=None)
	except HTTPError as e:
		raise RequestError("Tanıma İsteği Başarısız Oldu: {}".format(e.reason))
	except URLError as e:
		raise RequestError("Tanıma Bağlantısı Başarısız Oldu: {}".format(e.reason))

	response_text = response.read().decode("utf-8")

	for line in response_text.split("\n"):
		if not line: raise RecognitionError("Tanıma Başarısız Oldu!")
		result = json.loads(line)["result"]
		if len(result) != 0:
			text = result[0]["alternative"][0]["transcript"]
			break

	return text
