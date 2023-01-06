import numpy as np
import cv2
import ImageProcess as ImageProcess

def DisplayResult(img_matrix):
    # Load the image
    img =cv2.imread("/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Board/sudoku_board.jpeg")

    #Add the number on the image
    lb_x0 = 17
    lb_y0 = 35
    for i in range(9):
        for j in range(9):
            x = lb_x0 + 50*j
            y = lb_y0 + 50*i
            if img_matrix[i][j] !=0:
                img_text = cv2.putText(img, str(int(img_matrix[i][j])), (x, y),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv2.LINE_AA)

            # else:
            #     img_text = cv2.putText(img, str(int(img_result[i][j])), (x, y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 2, cv2.LINE_AA)
    cv2.imshow("Sudoku Result:",img_text)
    cv2.imshow("Sudoku Input",cv2.imread(ImageProcess.url))
    cv2.waitKey(0)
    return img_text