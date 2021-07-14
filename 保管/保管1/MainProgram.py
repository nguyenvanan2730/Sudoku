from re import VERBOSE
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import cv2

import ImageProcess as ImageProcess

#1. Input: The sudoku image from camera
#   Output: The matrix image 9x9
img_read = ImageProcess.read_img()
img_proce = ImageProcess.processing(img_read)
corners  = ImageProcess.find_corners(img_proce, img_read)
img_crop = ImageProcess.image_transform(img_read,corners)
img_crop2 = ImageProcess.processing(img_crop)
img_matrix = ImageProcess.create_img_matrix(img_read, img_crop)

#2. Input: The matrix image 9x9
#   Output: Predict the number of each image
model_mnist = load_model('C://Users/nguye/Desktop/VanAn/SUDOKU/model/mnist_handwritting.h5')

img_input = np.array(img_matrix)
print("img_input shape1: ", img_input.shape)
print("img_input lenght2: ", len(img_input))
img_input = img_input.astype('float32')
img_input = np.resize(img_input, (81, 28, 28, 1))
#img_input = img_input.reshape(img_input.shape[0], 28, 28, 1).astype('float32')
img_input /= 255
print("img_input shape: ", img_input.shape)
print("img_input lenght2: ", len(img_input))
print(img_input[0].shape)

pred_result = model_mnist.predict(img_input)
print(pred_result.shape)

# pred_num = []
# for i in len(pred_result[0]):
#     number = np.argmax(i)
#     if number > 0.5:
#         pred_num.append(pred_result[i][number.index])

number = np.argmax(pred_result, axis=1)
print(number)