from re import VERBOSE
#from tensorflow import keras
import numpy as np
import cv2

import ImageProcess as ImageProcess
import Predict as Predict
import SudokuAlgorithm as SudokuAlgorithm
import DisplayResult as DisplayResult

try:

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1400)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # windowsName = "Live"
    # cv2.namedWindow(windowsName,cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty(windowsName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    while(True):

        ret, frame = capture.read()
        #frame = cv2.flip(frame, Q1)
        cv2.imshow("frame",frame)
        key = cv2.waitKey(1) & 0xFF

        if ret == False:
                print("カメラから映像を取得できませんでした")
                break
  
    #1. Input: The sudoku image from camera
    #   Output: The matrix image 9x9
        img_corners = ImageProcess.detect_image(frame)

        if img_corners !=0:
            if cv2.waitKey(1) & 0xFF == ord('c'):
                img_matrix, img_crop = ImageProcess.extract_image(frame,img_corners)
                
                number_matrix = Predict.predict()
                print("number_matrix_before",number_matrix)
                result_matrix,state = SudokuAlgorithm.soduku_algorithm(number_matrix.copy())
                
                if state ==True:
                    print("number_matrix_after",number_matrix)
                    print("result_matrix", result_matrix)
                    img_result = DisplayResult.DisplayResult(number_matrix.copy(),result_matrix.copy())
                    DisplayResult.showInMovedWindow("SudoKu",img_crop,300,200)
                    DisplayResult.showInMovedWindow("Sloved",img_result,800,200)
                    
        #img_matrix = ImageProcess.extract_image(frame)
        #cv2.imshow("img_matrix",img_matrix)

        #cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindows()

except:
    import sys
    print("This Error is by computer:", sys.exc_info()[0])


