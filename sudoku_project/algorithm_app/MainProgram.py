from re import VERBOSE
import numpy as np
import cv2

from algorithm_app import ImageProcess as ImageProcess
from algorithm_app import SudokuAlgorithm as SudokuAlgorithm
from algorithm_app import DisplayResult as DisplayResult
from algorithm_app import UploadCropImageToS3 as UploadCropImageToS3
from algorithm_app import RecogizeNumberUsingTextract as RecogizeNumberUsingTextract

def mainProgram(file_path):
    #1. Get the Image from local storage
    #  Input: The sudoku image from local storage
    #  Output: Save the sudoku's area of the cropped image
    frame = ImageProcess.read_img(file_path)
    img_corners = ImageProcess.detect_image(frame)
    local_crop_img_url = ImageProcess.image_transform(frame,img_corners,file_path)
    s3_crop_img_url = UploadCropImageToS3.upload_file(local_crop_img_url)
    matrix = RecogizeNumberUsingTextract.recognize_number(s3_crop_img_url)
    #image_text=DisplayResult.DisplayResult(matrix)
    matrix_result=SudokuAlgorithm.soduku_algorithm(matrix)
    DisplayResult.DisplayResult(matrix_result)
    #2. Using Textract to recognize number.
    # Input: The image was be cropped.
    # Output: The number was be recognized by Textact.
