import os
import cv2
import json
import time
import numpy as np
from PIL import Image

cam = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier("Datas/face_recognition/datas/cascades/haarcascade_frontalface_default.xml")

user = input("Kullanıcı Adını Gir >>> ")
print("\n[BİLGİ] Kameraya Bakın ve Bekleyin...")
print("\n[BİLGİ] Veri Kaydı Başlatılıyor..")
time.sleep(1)
print("\n[BİLGİ] Veri Kaydı Başlatıldı.")
say = 0
os.mkdir("Datas/face_recognition/datas/faces/"+user)

while True:
	ret,cerceve = cam.read()
	cerceve = cv2.flip(cerceve, 1)
	gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
	faces = face_detector.detectMultiScale(gri, 1.5, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(cerceve, (x,y), (x+w,y+h), (255,0,0),2)
		say += 1
		path = "Datas/face_recognition/datas/faces/"+user+"/"
		cv2.imwrite(path+str(say)+".jpg", gri[y:y+h,x:x+w])
		cv2.imshow("DATA", cerceve)
	k = cv2.waitKey(100) & 0xFF
	if k == 27:
		break
	elif say >= 100:
		break

cam.release()
cv2.destroyAllWindows()

print("\n[BİLGİ] Veri Kaydı Tamamlandı.")
time.sleep(1.5)
print("\n[BİLGİ] Eğitim Başlatılıyor...")

yol = "Datas/face_recognition/datas/faces"

tani = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier("Datas/face_recognition/datas/cascades/haarcascade_frontalface_default.xml")

def getImageAndLabels(yol):
	faceSamples = []
	ids = []
	labels = []
	klasorler = os.listdir(yol)
	dictionary = {}

	print("[BİLGİ] Eğitim başlatıldı.")

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

print("[BİGİ] Eğitim Tamamlandı.")

print("\n[BiLGİ] Kullanıcı Başarıyla Kayıtedildi.")
time.sleep(5)