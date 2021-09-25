from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import pickle
from plot_confusion_matrix import plot_confusion_matrix
import tensorflow as tf
import time

MOBILE_CLASSIC_MODEL = 'mobile_handsRGB_model.h5'
MOBILE_NEW_AUG = 'newAUG_mobile_handsRGB_model.h5'

Half_trainable = 'Half_trainable.h5'
VGG_CLASSIC_MODEL = 'VGG_handsRGB_model.h5'
Bigdata_SQUEEZE = 'bigdata_simple_squeeze.h5'

SQUEEZE_2STEPS = 'squeezenet_twosteps.h5'  #
SQUEEZE_FT = 'Squeeze_FT_imagenet_AUG.h5'
SQUEEZE_CLASSIC = 'classic_squeeze.h5'
SQUEEZE_SIMPLE = 'simple_squeeze.h5'
SQUEEZE_64 = 'simple_squeeze_64batches.h5'
SQ32 = 'SQ32best_model.h5'
simple32 = 'simple_squeeze.h5'

BD_SQ1 = 'BDclassic_squeeze.h5'
BD_SQ2 = 'BDSqueeze_FT_imagenet_AUG.h5'
BD_SQ3 = 'BDsqueeze_reduced_imagenet.h5'
BD_SQ4 = 'SQ_best_model.h5'
BD_SQ16 = 'SQ16.h5'
BD_SQ64 = 'SQ64_best_model.h5'
BD_SQ = 'BDsimple_squeeze.h5'
BD_MOB = 'BDmobile_handsRGB_model.h5'
BD_MOB4='bigdata_mobile_handsRGB_model.h5'
BD_MOB1 = 'Mobile_best_model.h5'
BD_MOB2 = 'MobileNet_Full_trainable.h5'
BD_MOB3 = 'best_model_latter.h5'
MobRMS = "RMlast.h5"
MobRMS2 = "RMSbest_model2.h5"
MobSGD = "SGDbest_model.h5"

Full_trainable = 'VGG16_Full_trainable.h5'
BD_VGG2 = 'BD_AUG_VGGtwosteps_model.h5'
BD_VGG3 = 'BD_VGG_model.h5'
Augmented = 'Augmented_VGG16.h5'

#BEST OF
MODELS = [BD_SQ16, BD_MOB2, BD_MOB, Full_trainable]

#trying VGG16
#MODELS = [Full_trainable, Half_trainable, Augmented]

#Squeezenet
#MODELS = [BD_SQ16, BD_SQ, SQ32]

#optimizers
#MODELS = [MobRMS2, MobSGD]

x = pickle.load(open('X_test.pickle', 'rb'))
y = pickle.load(open('y_test.pickle', 'rb'))

x_test = np.array(x)
y_test = np.array(y)

# print(y_test.dtype)
for mod in MODELS:
    model = load_model(mod)
    # model.summary()
    # Evaluate the model on the test data using `evaluate`
    print("Evaluate on test data" + mod)
    model.summary()
    test_labels = y_test
    y_hot = tf.keras.utils.to_categorical(y_test)
    elapsed = 0
    for j in range(10):
        start_time = time.time()                        # START

        predictions = model.predict(x_test, batch_size=10, verbose=0)

        elapsed = elapsed + time.time() - start_time

    print(elapsed*(1000/200)/10, "millis")                      # STOP

    [L, Acc] = model.evaluate(x_test, y_hot, batch_size=10)

    cm = confusion_matrix(y_test, np.argmax(predictions, axis=1)) #dovresti trovare il modo di renderle non onehotencoded
    cm_plot_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    plot_confusion_matrix(cm, cm_plot_labels, model_name=mod, accuracy=Acc)

plt.show()


#from matplotlib import pyplot as plt

#plt.imshow(x_test[7, :, :, :].squeeze(), interpolation='nearest')
#plt.show()