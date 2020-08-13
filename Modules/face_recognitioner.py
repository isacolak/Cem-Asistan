import os
import cv2
import json
import numpy as np

tani = cv2.face.LBPHFaceRecognizer_create()
tani.read("Datas/face_recognition/datas/trainer.yml")

faceCascade = cv2.CascadeClassifier("Datas/face_recognition/datas/cascades/haarcascade_frontalface_default.xml")

font = cv2.FONT_HERSHEY_SIMPLEX

idd = 0

dictionary = {}
names = []

dosya = open("Datas/face_recognition/datas/ids.json")

dictionary = json.load(dosya)

cam = cv2.VideoCapture(0)

for key,value in dictionary.items():
	names.append(key)

while True:
	ret,cerceve = cam.read()
	cerceve = cv2.flip(cerceve, 1)
	gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(gri,scaleFactor=1.5,minNeighbors=5)

	for (x,y,w,h) in faces:
		cv2.rectangle(cerceve, (x,y), (x+w,y+h), (0,255,0),2)
		idd,oran = tani.predict(gri[y:y+h,x:x+w])
		print(idd)
		print("\n",oran)

		if (oran >= 30):
			idd = names[idd]
		else:
			idd = "Bilinmiyor"

		cv2.putText(cerceve, str(idd), (x+5,y-5), font, 1, (255,255,255),2)
		
		cv2.imshow("KAMERA", cerceve)
		
		k = cv2.waitKey(1) & 0xFF

		if k == 27:
			break

cam.release()
cv2.destroyAllWindows()