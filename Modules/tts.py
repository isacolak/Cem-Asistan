import sys
import pyttsx3

text = "".join(sys.argv[1:])

en = pyttsx3.init("sapi5")
v = en.getProperty("voices")
en.setProperty("voice", v[14].id)
en.setProperty("rate",150)
en.say(text)
en.runAndWait()