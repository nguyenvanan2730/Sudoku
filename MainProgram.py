from re import VERBOSE
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
   
    while(True):
        
        ret, frame = capture.read()
        #frame = cv2.flip(frame, Q1)
        cv2.imshow("frame",frame)
        key = cv2.waitKey(1) & 0xFF

        if ret == False:
                print("カメラから映像を取得できませんでした")
                break
  
    #1. Get the Image by the camera
    #  Input: The sudoku image from camera
    #  Output: 4 conner of the sudoku frame
        img_corners = ImageProcess.detect_image(frame)

        if img_corners !=0:
            if cv2.waitKey(1) & 0xFF == ord('c'):

    #2 Extract the image
    #  Input:  The sudoku image frame
    #  Output: The image matrix: 9x9          
                img_matrix, img_crop = ImageProcess.extract_image(frame,img_corners)

    #3 Predict the number
    #  Input:  The image matrix: 9x9
    #  Output:  The number of this image: [0,1,2,3,4,5,6,7,8,9]           
                number_matrix = Predict.predict()
                print("number_matrix_before",number_matrix)

    #4. Solve the sudoku's task            
                result_matrix,state = SudokuAlgorithm.soduku_algorithm(number_matrix.copy())

    #5. Display the result on the screen            
                if state ==True:
                    print("number_matrix_after",number_matrix)
                    print("result_matrix", result_matrix)
                    img_result = DisplayResult.DisplayResult(number_matrix.copy(),result_matrix.copy())
                    DisplayResult.showInMovedWindow("SudoKu",img_crop,300,200)
                    DisplayResult.showInMovedWindow("Sloved",img_result,800,200)
                    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindows()

except:
    import sys
    print("This Error is by computer:", sys.exc_info()[0])
