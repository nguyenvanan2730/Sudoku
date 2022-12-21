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


import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

file_name = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/crop-input-image/image_transform.png"
bucket = "text-extract-sudoku"

import boto3
s3 = boto3.resource('s3')
s3.Bucket('text-extract-sudoku').upload_file(file_name, "image_transform.png")

""" # 1. Upload the cropped image to S3.
if object_name is None:
    object_name = os.path.basename(file_name)  

s3_client = boto3.client('s3')
try:
    response= s3_client.upload_file(file_name, bucket)
except ClientError as e:
    logging.error(e)
    print("False")
print("True") """