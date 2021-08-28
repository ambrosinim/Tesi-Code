# ** FINAL APPLICATION: **
#  - USER INTERFACE
#  - PREDICTION OF THE INPUT IMAGE
#  - ARDUINO COMMUNICATION


from tensorflow.keras.models import load_model
import cv2
import numpy as np
import serial
import time
import csv


CLASSIC_MODEL = 'mobile_handsRGB_model.h5'
AUG_MODEL = 'AUG_mobile_handsRGB_model.h5'
NEW_AUG = 'newAUG_mobile_handsRGB_model.h5'
SQ_64 = 'simple_squeeze_64batches.h5'

# BEST OF
BD_SQ16 = 'SQ16.h5'
BD_MOB2 = 'MobileNet_Full_trainable.h5'
Full_trainable = 'VGG16_Full_trainable.h5'

model = load_model(BD_SQ16)

CLASS_MAP = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine"
}


def mapper(val):
    return CLASS_MAP[val]


def crc8(data):
    crc = 0
    for i in range(len(data)):
        byte = ord(data[i])
        for b in range(8):
            fb_bit = (crc ^ byte) & 0x01
            if fb_bit == 0x01:
                crc = crc ^ 0x18
            crc = (crc >> 1) & 0x7f
            if fb_bit == 0x01:
                crc = crc | 0x80
            byte = byte >> 1

    return crc


def compute_crc8(stringa):
    crc = 0

    for w in range(len(stringa)):

        byte = ord(stringa[w])

        crc = crc ^ byte  # XOR-in the next input byte

        for u in range(8):

            if (crc & 0x80) != 0:

                crc = (crc << 1) ^ 0x8c
                # polynomial = x^8 + x^5 + x^3 + x^2 + x + 1 (ignore MSB which is always 1)

            else:
                crc = crc << 1

    return crc


def write_read(inp):

    data = arduino.readline()[:-2].decode('UTF-8')
    print(data)
    time.sleep(0.05)
    if data == 'y':
        string = "s/" + str(inp) + "*"
        crc_src = crc8(list(string))
        string = string + str(crc_src) + "/f"
        arduino.write(string.encode())  #struct.pack('>B', inp)
        time.sleep(0.05)
        print('sent: ')  # printing the value
        print(string)


# pay attention to COM number!
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.5)

cap = cv2.VideoCapture(0)

last_index = np.zeros(5, dtype='int64')  # per stabilizzare le previsioni prevedo di prendere il più frequente di 5 previoni (50ms)
i = 0

elapsed_row = []

while True:

    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (200, 200), (424, 424), (255, 255, 255), 2)

    # extract the region of image within the user rectangle
    roi = frame[200:424, 200:424]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    image = np.array([img])
    image = image.reshape(1, 224, 224, 3)

    image = image.astype('float32')
    image /= 255
    # print(image.shape)

    # predict the move made
    # we want to measure thw time elapsed in one prediction
    start_time = time.time()                       # START
    elapsed = 0

    prediction = model.predict(image)

    elapsed = elapsed + time.time() - start_time  # STOP

    # we save in a csv file named "extime.csv" the execution time of one prediction to calculate its mean value
    # write a row to the csv file
    elapsed = elapsed*1000
    elapsed_row.append(elapsed)

    pred_index = np.argmax(prediction[0])

    last_index[i] = pred_index
    i += 1
    if i == 5:
        i = 0
    # we take the most frequent number predicted between the last five predictions to make it more robust
    pred_index = np.bincount(last_index).argmax()
    pred_num = mapper(pred_index)

    # Taking input from user and sending it to Arduino
    write_read(pred_index)

    # Set the graphic's features
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Number: " + pred_num,
                (50, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.namedWindow("NUM", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("NUM", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("NUM", frame)
    k = cv2.waitKey(1)

    if k == ord('q'):
        break

with open("extime.csv", "w") as file:
    writer = csv.writer(file, delimiter='\n')
    writer.writerow(elapsed_row)


cap.release()
cv2.destroyAllWindows()








