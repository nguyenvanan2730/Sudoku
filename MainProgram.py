from re import VERBOSE
import numpy as np
import cv2

import ImageProcess as ImageProcess
#import Predict as Predict
import SudokuAlgorithm as SudokuAlgorithm
import DisplayResult as DisplayResult


#1. Get the Image from local storage
#  Input: The sudoku image from local storage
#  Output: Save the sudoku's area of the cropped image
frame = ImageProcess.read_img()
img_corners = ImageProcess.detect_image(frame)
img_crop = ImageProcess.image_transform(frame,img_corners)

#2. Using Textract to recognize number.
# Input: The image was be cropped.
# Output: The number was be recognized by Textact.
