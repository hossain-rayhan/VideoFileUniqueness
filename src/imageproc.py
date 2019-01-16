import numpy as np
import cv2

cap = cv2.VideoCapture('/home/dbarry/link.avi')

print("Step 1")

ret, frame = cap.read()

print("Step 2")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

print("Step 3")

#cv2.imshow('frame',gray)
cv2.imwrite("juggle.jpg",gray)

print("Step 4")

