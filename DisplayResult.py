import numpy as np
import cv2

def DisplayResult(img_matrix, img_result):
    # Load the image
    img =cv2.imread("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/test/board.png")
    #Add the number on the image
    lb_x0 = 17
    lb_y0 = 35
    for i in range(9):
        for j in range(9):
            x = lb_x0 + 50*j
            y = lb_y0 + 50*i
            if img_matrix[i][j] !=0:
                img_text = cv2.putText(img, str(int(img_matrix[i][j])), (x, y),cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2, cv2.LINE_AA)
                # cv2.imshow("Slove",img_text)
                # cv2.waitKey(0)
            else:
                img_text = cv2.putText(img, str(int(img_result[i][j])), (x, y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 2, cv2.LINE_AA)
                # cv2.imshow("slove",img_text)
                # cv2.waitKey(0)
    return img_text
                
def showInMovedWindow(winname, img, x, y):
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, x, y)   # Move it to (x,y)
    cv2.imshow(winname,img)

# img = DisplayResult(matrix, result)
# cv2.imshow("Solve",img)
# cv2.waitKey(0)               