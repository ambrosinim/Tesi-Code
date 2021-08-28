import pickle
from sklearn.utils import shuffle
import tensorflow as tf
import cv2
import numpy as np
import sys
import os
# create pickle files to save the test data and lables

IMG_SAVE_PATH = 'Test_dataX'


CLASS_MAP = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

NUM_CLASSES = len(CLASS_MAP)


def mapper(val):
    return CLASS_MAP[val]


dataset = []

for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        dataset.append([img, directory])

data, labels = zip(*dataset)
labels = list(map(mapper, labels))


# one hot encode the labels
#labels = tf.keras.utils.to_categorical(labels)
y = np.array(labels)

datanp = np.array(data)
# select only the R colour channel
print(datanp.shape)

# print(datanp.dtype)

X = datanp.astype('float32')
X /= 255



pickle_out = open("X_test.pickle", "wb")  # write bytes
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y_test.pickle", "wb")   # se lo carichi rb = read bytes
pickle.dump(y, pickle_out)
pickle_out.close()
