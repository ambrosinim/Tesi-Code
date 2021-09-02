import tensorflow as tf
import cv2
import numpy as np
import sys
import os
import time

try:
    label_name = sys.argv[1]
    num_samples = int(sys.argv[2])
except:
    print("Arguments missing.")

    exit(-1)

IMG_SAVE_PATH = 'Test_data'
IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, label_name)

i = 0
try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass
try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")
    list_files = os.listdir(IMG_CLASS_PATH)
    list_noextension = [el.split('.')[0] for el in list_files]
    integer_map = map(int, list_noextension)
    integer_list = list(integer_map)
    i = max(integer_list)

cap = cv2.VideoCapture(0)
print(i)
start = False
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if count == num_samples:
        break

    cv2.rectangle(frame, (200, 200), (500, 500), (255, 255, 255), 2)

    if start:
        roi = frame[200:500, 200:500]
        save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(i+count + 1))
        cv2.imwrite(save_path, roi)
        count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Collecting {}".format(count),
            (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)

    k = cv2.waitKey(10)
    time.sleep(1.0)
    if k == ord('a'):
        start = not start
    if k == ord('s'):
        start = False
    if k == ord('q'):
        break

print("\n{} image(s) saved to {}".format(count, IMG_CLASS_PATH))
cap.release()
cv2.destroyAllWindows()


