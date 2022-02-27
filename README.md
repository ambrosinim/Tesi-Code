# Tesi-Code
### Folders in Repository and content:
- Braccio_arduino_finalcode:
  - C++ Arduino code for communication with the PC and actuate the small robotic arm through 3 servos.
- Python Code:
  - Python PC application
  - Squeezenet and MobileNet models (no VGG16 models)
  - Testing application
  - Confusion Matrices plotting
  - Snippets for the training and testing datasets formation
- More models:
   - Other trained models, less performant than the ones in "Python Code"
- Jupyter (Colab) notebooks for training:
  - Notebooks keeping track of the training of the main models.


# Training
To execute further training with the same GitHub setup to access the dataset is suggested the use of Colab (https://research.google.com/colaboratory/).
The acess to the dataset is already present in the Jupyter notebooks.

**Traing dataset:** https://github.com/ma-tesi/hands_dataset.git
# Testing Finale
The testing process can be executed by working on your architecture by downloading the folder "Python Code" and by these following steps:
1.open and execute **testpickle.py** that creates the files **X_test.pickle** and **Y_test.pickle** inside the folder "Test Data". Those files consist in the test inputs and the corresponding true labels;
2. open and execute **test.py** that prints out the performance of each model and their confusion matrices.

Before executing pay attention to the path pointed by **IMG_SAVE_PATH** and eventually fix it.

#### Raccogliere immagini personali
Further tests can be carried out by using the application "gather_testimages.py" that adds new gathered images to the "Test Data" folder without overwriting.
Eventually a totally new dataset can be created by changing the **IMG_SAVE_PATH** path.
The **gather_testimages.py** program must be launched from **prompt** command line by positioning in the directory containing the application together with the testing images folder.
In my case, after positioning in the "Python code" folder I insert the following command:

**python gather_testimages.py label number_of_samples**.

For instance: "**python gather_testimages.py three 10**" gathers 10 images in the folder "three" that gets created (if doesn't exist already) inside the folder pointed by "IMG_SAVE_PATH".

The newly gathered images can also be used to update the traing dataset.

Finally it is possible to test the application in real time with the application
# Example of inference:
![NUM 18_07_2021 15_53_17](https://user-images.githubusercontent.com/79223382/136415970-91a7821f-2ae7-46ae-ac63-1863fab07f27.png)
