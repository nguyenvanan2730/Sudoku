from re import VERBOSE
import numpy as np
import cv2

import ImageProcess as ImageProcess
import SudokuAlgorithm as SudokuAlgorithm
import DisplayResult as DisplayResult
import UploadCropImageToS3 as UploadCropImageToS3
import RecogizeNumberUsingTextract as RecogizeNumberUsingTextract


#1. Get the Image from local storage
#  Input: The sudoku image from local storage
#  Output: Save the sudoku's area of the cropped image
frame = ImageProcess.read_img()
img_corners = ImageProcess.detect_image(frame)
local_crop_img_url = ImageProcess.image_transform(frame,img_corners)
s3_crop_img_url = UploadCropImageToS3.upload_file(local_crop_img_url)
matrix = RecogizeNumberUsingTextract.recognize_number(s3_crop_img_url)
image_text=DisplayResult.DisplayResult(matrix)
matrix_result=SudokuAlgorithm.soduku_algorithm(matrix)
DisplayResult.DisplayResult(matrix_result)
#2. Using Textract to recognize number.
# Input: The image was be cropped.
# Output: The number was be recognized by Textact.
