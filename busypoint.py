import numpy as np
import cv2

def isWithin(x, lowest_x):
	if lowest_x == 0 or abs(x - lowest_x) < 20:
		return True
	return False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profileface_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

miaFrames = 160
maxPixelDist = 30
cap = cv2.VideoCapture("vid_cropped.mp4")
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
lowest_x = 0
frameCount = 0
faceFound = False
while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	cv2.putText(frame,str(fps),(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1)
	for i in range(len(faces)):
		(x,y,w,h) = faces[i]
		cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		average_colour = np.average(np.average(roi_color, axis=0), axis=0)
		print i, ": ", average_colour
		if isWithin(x, lowest_x):
			faceFound = True
			lowest_x = x
	if faceFound:
		frameCount += 1
	else:
		frameCount = 0
		lowest_x = 0
	faceFound = False
	cv2.putText(frame, str(frameCount),(500,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),1)
	k = cv2.waitKey(30) & 0xff
	cv2.imshow('frame', frame)
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()