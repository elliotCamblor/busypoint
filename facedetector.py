import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profileface_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

cap = cv2.VideoCapture("vid_cropped.mp4")

while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	profile_faces = profileface_cascade.detectMultiScale(frame, 1.3, 5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
	for (x,y,w,h) in profile_faces:
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
	k = cv2.waitKey(30) & 0xff
	cv2.imshow('frame', frame)
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()
