import numpy as np
import cv2

def checkIfOldFace(face, oldFace):
	print face
	if tuple(oldFace) in frame_counts and abs(face[0] - oldFace[0]) < 10 and abs(face[1] - oldFace[1]) < 10 and abs(face[1] - oldFace[1]) < 10 and abs(face[2] - oldFace[2]) < 10 and abs(face[3] - oldFace[3]) < 10:
		frame_counts[tuple(face)] = frame_counts[tuple(oldFace)] + 1
		del frame_counts[tuple(oldFace)]

	else:
		frame_counts[tuple(face)] = 1


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profileface_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

cap = cv2.VideoCapture("vid_cropped.mp4")
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
oldFaces = []
frame_counts = {}
while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	cv2.putText(frame,str(fps),(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1)
	# profile_faces = profileface_cascade.detectMultiScale(frame, 1.3, 5)
	faceDict = {}
	for i in range(len(faces)):
		(x,y,w,h) = faces[i]
		faceDict[tuple(faces[i])] = True
		cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
		if tuple(faces[i]) in frame_counts:
			frame_counts[tuple(faces[i])] += 1
			cv2.putText(frame, str(frame_counts[tuple(faces[i])]),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),1)
		elif i + 1 <= len(oldFaces):
			checkIfOldFace(faces[i], oldFaces[i])
			cv2.putText(frame, str(frame_counts[tuple(faces[i])]),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),1)
		else:
			frame_counts[tuple(faces[i])] = 1
		
		print frame_counts
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
	oldFaces = faces
	k = cv2.waitKey(30) & 0xff
	cv2.imshow('frame', frame)
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()


