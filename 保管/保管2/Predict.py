#from tensorflow.keras.models import load_model
import numpy as np
import cv2
import pickle

def predict():
    #Load the model
    filename = 'C://Users/nguye/Desktop/VanAn/SUDOKU/model/chars74k_2.sav'
    model_chars74k = pickle.load(open(filename, 'rb'))
    #Read the image data
    img_input = []
    for i in range(0,9):
        for j in range(0,9):
            img_read = cv2.imread("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/number/img{}{}.png".format(i,j),0)
            img_read = cv2.resize(img_read,(64,64))
            img_input.append(img_read)

    #Reshape the image data
    training_sudoku = np.array(img_input).reshape(-1,4096)

    #Predict the data
    pred_result = model_chars74k.predict(training_sudoku)
    

    #print the data
    number = np.array(pred_result)
    print("Predict value: \n",number.reshape(9,9))

    return number.reshape(9,9)