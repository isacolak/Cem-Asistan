import os
import cv2
import json
import numpy as np
from PIL import Image

yol = "Datas/face_recognition/datas/faces"

tani = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier("Datas/face_recognition/datas/cascades/haarcascade_frontalface_default.xml")

def getImageAndLabels(yol):
	faceSamples = []
	ids = []
	labels = []
	klasorler = os.listdir(yol)
	dictionary = {}

	for i,kl in enumerate(klasorler):
		dictionary[kl] = int(i)

	f = open("Datas/face_recognition/datas/ids.json","w")
	a = json.dump(dictionary, f)
	f.close()

	for kl in klasorler:
		for res in os.listdir(os.path.join(yol,kl)):
			PIL_img = Image.open(os.path.join(yol,kl,res)).convert("L")
			img_numpy = np.array(PIL_img,"uint8")
			idd = int(dictionary[kl])
			faces = detector.detectMultiScale(img_numpy)
			for (x,y,w,h) in faces:
				faceSamples.append(img_numpy[y:y+h,x:x+w])
				ids.append(idd)
	return faceSamples, ids

faces,ids = getImageAndLabels(yol)

tani.train(faces,np.array(ids))
tani.write("Datas/face_recognition/datas/trainer.yml")