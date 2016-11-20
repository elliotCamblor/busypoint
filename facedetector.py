import numpy as np
import cv2

def checkIfOldFace(face):
	# check if oldfaces is empty
	if len(oldFaces.keys()):
		# check for the current location in oldFaces, if it's found update the frame counts and set wasFound to true
		if tuple(face) in oldFaces:
			oldFaces[tuple(face)]["frameCount"] += 1
			oldFaces[tuple(face)]["wasFound"] = True
			return
		# Check the faces for a nearby face. If its found update the key, frame count, and wasFound, delete old key entry
		for oldFaceCoord, value in oldFaces.iteritems():
			if isFaceClose(face, oldFaceCoord) and "wasFound" not in value:
				print "here"
				oldFaces[tuple(face)] = oldFaces[tuple(oldFaceCoord)]
				oldFaces[tuple(face)]["frameCount"] += 1
				oldFaces[tuple(face)]["wasFound"] = True
				del oldFaces[tuple(oldFaceCoord)]
				break

		# If no match was found assume its a new face
		else:
			oldFaces[tuple(face)] = {
				"frameCount": 1,
				"wasFound": True
			}
	# if there are no entries add it as the first
	else:
		oldFaces[tuple(face)] = {
			"frameCount": 1,
			"wasFound": True
		}

def cleanupFaceDict():
	for key in oldFaces.keys():
		# If the face was found this frame set mia frames to 0 and delete wasFound for the next frame
		if "wasFound" in oldFaces[key]:
			oldFaces[key]["miaFrames"] = 0
			del oldFaces[key]["wasFound"]
		# Otherwise if its been mia for less than 29 frames increase the counter
		elif oldFaces[key]["miaFrames"] < 29:
			oldFaces[key]["miaFrames"] = oldFaces[key]["miaFrames"] + 1
		# If its been mia more than 29 frames delete the entry
		else:
			del oldFaces[key]


def isFaceClose(face, oldFace):
	if abs(face[0] - oldFace[0]) < 20 and abs(face[1] - oldFace[1]) < 20 and abs(face[1] - oldFace[1]) < 20 and abs(face[2] - oldFace[2]) < 20 and abs(face[3] - oldFace[3]) < 20:
		return True
	return False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profileface_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

cap = cv2.VideoCapture("vid_cropped.mp4")
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
oldFaces = {}
while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	cv2.putText(frame,str(fps),(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1)

	# print oldFaces
	for i in range(len(faces)):
		(x,y,w,h) = faces[i]
		cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
		checkIfOldFace(tuple(faces[i]))
		cv2.putText(frame, str(oldFaces[tuple(faces[i])]["frameCount"]),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),1)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
	print oldFaces
	cleanupFaceDict()
	k = cv2.waitKey(30) & 0xff
	cv2.imshow('frame', frame)
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()


