from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)
# loop over the image paths
while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# load the image and resize it to (1) reduce detection time
	# and (2) improve detection accuracy
 
	# detect people in the image
	(rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
		padding=(8, 8), scale=1.2)

 
	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
 
	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
	# show the output images
	k = cv2.waitKey(30) & 0xff
	cv2.imshow('frame', frame)
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()