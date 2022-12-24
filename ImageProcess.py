from re import I
import cv2
import numpy as np
import os
url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-level64.jpeg"
file_name=os.path.splitext(os.path.basename(url))[0]
#1. Import the image
def read_img():
    #url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-1.png"
    #url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-level15.jpeg"
    image = cv2.imread(url) #画像は強制的にグレイスケール画像として読み込まれます。
    #cv2.imshow("read_img",image)
    return image

#2. Preprocessing the image
def processing(img):
    path = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/preprocess-input-image/"
    #2.1 Gaussian blur:  reduce noise obtained in thresholding algorithm (adaptive thresholding)
    #convert color image to gray image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f"{path}img1_bgr2gray.png",img)
    # cv2.imshow("img",img)
    # cv2.waitKey(0)

    #ksize.width and ksize.height can differ but they both must be positive and odd.
    img_gauss = cv2.GaussianBlur(img.copy(), (7, 7), 0)
    cv2.imwrite(f"{path}img2_GaussianBlur.png",img_gauss)
    # cv2.imshow("img_gauss",img_gauss)
    # cv2.waitKey(0)

    #2.2 Thresholding: Segmenting the regions of the image
    img_thres = cv2.adaptiveThreshold(img_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 131, 2)
    cv2.imwrite(f"{path}img3_adaptiveThreshold.png",img_thres)
    # cv2.imshow("adaptiveThreshold",img_thres)
    # cv2.waitKey(0)
    
    #2.3 Dilating the image: In cases like noise removal, erosion is followed by dilation.
    #object to be found should be white and background should be black.
    img_bitwise = cv2.bitwise_not(img_thres,img_thres)
    cv2.imwrite(f"{path}img4_bitwise.png",img_bitwise)
    # cv2.imshow("img_bitwise",img_bitwise)
    # cv2.waitKey(0)
    return img_bitwise

#3. Find the the sudoku's frame
def find_corners(img_proce, img_read):

    #find the contours on the img_proce
    ext_contours,hierarchy = cv2.findContours(img_proce, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #ext_contours = ext_contours[0] if len(ext_contours) == 2 else ext_contours[1]
    #Make the contours sort from the big to small
    ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)

    # Fix-green-point-when-crop
    # sudoku_board = cv2.drawContours(img_read_draw, ext_contours[0], -1, (0,255,0), 3)
    # cv2.imshow('Contours',sudoku_board)
    # cv2.waitKey(0)
    #cv2.destroyAllWindows()

    for contour in ext_contours[0:2]:
        #print("The lengt of contours: ", len(ext_contours))
        #輪郭の周囲の長さを計算できます
        deta=cv2.arcLength(contour,True)
        #曲線など多数の点で構成される輪郭をより少ない点で近似できます
 
        img_approx = cv2.approxPolyDP(contour, 0.015*deta, True)

        if len(img_approx) == 4:

            corners = [(corner[0][0],corner[0][1]) for corner in img_approx]
            #img_approx = np.argmin(img_approx,axis=0)
            print ("img_approx before", corners )
            corners = np.array(corners)
            """ 0/0---x--->
                |
                |
                y
                |
                |
                v """

            #20221222-fix the image was be roate incorrectly
            left_point=[]
            right_point=[]
            x_corner=[corners[0][0],corners[1][0],corners[2][0],corners[3][0]]
            y_corner=[corners[0][1],corners[1][1],corners[2][1],corners[3][1]]
            x_corner.sort()
            for index,item in enumerate(corners):
                if corners[index][0] < x_corner[2]:
                    left_point.append(corners[index])
                else:
                    right_point.append(corners[index])

            if left_point[0][1]<left_point[1][1]:
                top_left = left_point[0]
                bottom_left =left_point[1]
            else:
                top_left = left_point[1]
                bottom_left =left_point[0]                

            if right_point[0][1]<right_point[1][1]:
                top_right = right_point[0]
                bottom_right =right_point[1]
            else:
                top_right = right_point[1]
                bottom_right =right_point[0]

            corners = [top_right, top_left, bottom_left, bottom_right]
            print(f"top_right, top_left, bottom_left, bottom_right", corners)
            return corners
    else: 
        print("Cannot found the boudary of sudoku, please make sure the boundary is clear")
        return 0

#4. Crop and transform the image
def image_transform(image,corners):
    #Get these corners
    top_right, top_left, bottom_left, bottom_right = corners[0], corners[1], corners[2], corners[3]

    #Calculate the width of the cropping image
    width_top = np.sqrt((top_right[0]-top_left[0])**2 + (top_right[1]-top_left[1])**2)
    width_bottom = np.sqrt((bottom_right[0]-bottom_left[0])**2 + (bottom_right[1]-bottom_left[1])**2)
    width = max(int(width_top), int(width_bottom))

    #Calculate the height of the cropping image
    height_right = np.sqrt((top_right[0]-bottom_right[0])**2 + (top_right[1]-bottom_right[1])**2)
    height_left = np.sqrt((top_left[0]-bottom_left[0])**2 + (top_left[1]-bottom_left[1])**2)
    height = max(int(height_right), int(height_left))
    print("width: {}/nheight: {}".format(width,height))
    #Contruct new points to obtain top-down view of image
    #dimensions = np.array([[0,0],  [width-1,0], [0, height-1], [width-1, height-1]], dtype="float32")
    dimensions = np.array([[0,0],  [width,0], [0, height], [width, height]], dtype="float32")
    #convert to Numpy format
    ordered_corners = np.array([top_left,top_right, bottom_left, bottom_right], dtype = "float32")
    #ordered_corners = np.array([top_left, top_right, bottom_right, bottom_left], dtype = "float32")

    #Crop the image
    grid = cv2.getPerspectiveTransform(ordered_corners, dimensions)
    img_crop = cv2.warpPerspective(image,grid,(width,height))
    
    img_crop = cv2.resize(img_crop,(450,450))
    cv2.imwrite("/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/crop-input-image/%s.png"%file_name,img_crop)
    #create logic check image had or not.
    return file_name


def detect_image(img_frame):
    # img_read = read_img(frame)
    img_proce = processing(img_frame)
    corners  = find_corners(img_proce, img_frame)
    return corners if corners !=0 else 0
