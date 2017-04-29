# Only working with python 3.5.2

import cv2

filename = "test.mp4"
cap = cv2.VideoCapture(filename)

if not cap.isOpened():
    print("Could not open:", filename)

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#print(frame_count)
# set the first frame to the desired frame (the last frame)
cap.set(1, frame_count - 10) 
ret, frame = cap.read()
#cv2.imshow("Window", frame)
cv2.imwrite("test.png", frame)
