from re import I
import cv2
import numpy as np

#1. Import the image
def read_img():
    #url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-1.png"
    url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-level15.jpeg"
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
    cv2.imshow("img",img)
    cv2.waitKey(0)

    #ksize.width and ksize.height can differ but they both must be positive and odd.
    img_gauss = cv2.GaussianBlur(img.copy(), (7, 7), 0)
    cv2.imwrite(f"{path}img2_GaussianBlur.png",img_gauss)
    cv2.imshow("img_gauss",img_gauss)
    cv2.waitKey(0)

    #2.2 Thresholding: Segmenting the regions of the image
    img_thres = cv2.adaptiveThreshold(img_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 131, 2)
    cv2.imwrite(f"{path}img3_adaptiveThreshold.png",img_thres)
    cv2.imshow("adaptiveThreshold",img_thres)
    cv2.waitKey(0)
    
    #2.3 Dilating the image: In cases like noise removal, erosion is followed by dilation.
    #object to be found should be white and background should be black.
    img_bitwise = cv2.bitwise_not(img_thres,img_thres)
    cv2.imwrite(f"{path}img4_bitwise.png",img_bitwise)
    cv2.imshow("img_bitwise",img_bitwise)
    cv2.waitKey(0)
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

    for contour in ext_contours[0:1]:
        #print("The lengt of contours: ", len(ext_contours))
        #輪郭の周囲の長さを計算できます
        deta=cv2.arcLength(contour,True)
        #曲線など多数の点で構成される輪郭をより少ない点で近似できます
        img_approx = cv2.approxPolyDP(contour, 0.015*deta, True)
    
        if len(img_approx) == 4:

            corners = [(corner[0][0],corner[0][1]) for corner in img_approx]
            #img_approx = np.argmin(img_approx,axis=0)
            #print ("img_approx before", corners )
            corners = np.array(corners)
            """ 0/0---x--->
                |
                |
                y
                |
                |
                v """
 
            #20221222-fix the image was be roate incorrectly
            top_right = corners[0]
            top_left = corners[1]
            bottom_left = corners[2]
            bottom_right = corners[3]
            
            #print("The value of img_approx: ", img_approx)
            #corners = [(corner[0][0],corner[0][1]) for corner in img_approx]
            corners = [top_right, top_left, bottom_left, bottom_right]
            print(corners)
            return corners
    else: return 0

#4. Crop and transform the image
def image_transform(image,corners):
    cv2.imshow("img_transform",image)
    cv2.waitKey(0)
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
    dimensions = np.array([[0,0],  [width-1,0], [0, height-1], [width-1, height-1]], dtype="float32")

    #convert to Numpy format
    ordered_corners = np.array([top_left,top_right, bottom_left, bottom_right], dtype = "float32")
    #ordered_corners = np.array([top_left, top_right, bottom_right, bottom_left], dtype = "float32")

    #Crop the image
    grid = cv2.getPerspectiveTransform(ordered_corners, dimensions)
    img_crop = cv2.warpPerspective(image,grid,(width,height))
    
    img_crop = cv2.resize(img_crop,(450,450))
    cv2.imwrite("/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/crop-input-image/crop-input-image-.png",img_crop)
    #create logic check image had or not.
    return img_crop

#5. Create image's matrix 9x9
def create_img_matrix(img_read, img_crop):
    grid = np.copy(img_crop)
    
    edge_w = np.shape(grid)[0]
    edge_h = np.shape(grid)[1]
    celledge_h = edge_h // 9
    celledge_w = edge_w //9
    
    #   1   2   3   4   5   6   7   8   9   
    #   10  11  12  13  14  15  16  17  18
    #   19  20  21  22  23  24  25  26  27
    #   28  29  30  31  32  33  34  35  36
    #   37  38  39  40  41  42  43  44  45
    #   46  47  48  49  50  51  52  53  54
    #   55  56  57  58  59  60  61  62  63
    #   64  65  66  67  68  69  70  71  72
    #   73  74  75  76  77  78  79  80  81 

    img_matrix=[]
    X = []
    Y = []
    i=0
    for cell_h in range(0, edge_h, celledge_h):
        for cell_w in range(0, edge_w, celledge_w):
            #img_cell_crop=grid[0:50,0:50]
            x0 = cell_w
            x1 = x0 + celledge_w
            y0 = cell_h
            y1 = y0 + celledge_h
            X.append([x0,y0])
            Y.append([y0,y1])

            img_cell_crop = grid[y0 : y1, x0:x1 ]
            cv2.imwrite("/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/matrix-input-image%d.png"%i,img_cell_crop)
            img_matrix.append(img_cell_crop)
            i+=1

    return img_matrix

#6.Extract the number from the cell
def extrac_number(img_matrix):

    number_state=np.zeros(81,dtype=int)

    for i in range(81):

        grid = cv2.cvtColor(img_matrix[i], cv2.COLOR_BGR2GRAY)
        img_gauss = cv2.GaussianBlur(grid.copy(), (13, 13), 0)
        grid = cv2.bitwise_not(cv2.adaptiveThreshold(img_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 171, 1))
        cv2.imwrite("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/number_extract/img%d.png"%i,grid)
        #Find contours
        cnts,_ = cv2.findContours(grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #cv2.waitKey(0)
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)

            if (x < 3 or y < 3 or x > 25 or y > 25 or h < 10 or w < 10 or h*w < 250): #15*25pixel
            # Note the number is always placed in the center
            # Since image is 28x28
            # the number will be in the center thus x >3 and y>3
            # Additionally any of the external lines of the sudoku will not be thicker than 3
                continue
            else: number_state[i]=1

    number_state = np.reshape(number_state,(9,9))
    print("number_state: ", number_state)

    for i in range(9):
        for j in range(9):

            if number_state[i][j] ==1:

                img_gray = cv2.cvtColor(img_matrix[i*9+j], cv2.COLOR_BGR2GRAY)
                img_gauss = cv2.GaussianBlur(img_gray.copy(), (7, 7), 0)
                img_bit = cv2.bitwise_not(cv2.adaptiveThreshold(img_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 1))    
                
                cnts, _ = cv2.findContours(img_bit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                ext_cnts = sorted(cnts, key=cv2.contourArea, reverse=True)               
                for c in ext_cnts[0:2]:
                    x, y, w, h = cv2.boundingRect(c)

                    if (x > 3 and y > 3 and x < 25 and y < 25 and h*w > 250): #15*25pixel
                        
                        img_matrix_num = img_bit[y:y + h, x:x + w]
                        
                        ratio = 100//h
                        w1 = ratio*w
                        h1 = ratio*h

                        top = (120 - h1)//2
                        bottom = 120 - h1 - top
                        left = (120 - w1)//2
                        right = 120 - w1 - left

                        img_matrix_num = cv2.resize(img_matrix_num,(w1,h1))
                        img_matrix_num = cv2.copyMakeBorder(img_matrix_num, top, bottom, left, right, cv2.BORDER_CONSTANT)

                        cv2.imwrite("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/number/img{}{}.png".format(i,j),img_matrix_num)
            else:
                img_empty = cv2.imread("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/test/img50x50.png")
                cv2.imwrite("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/number/img{}{}.png".format(i,j),img_empty)


def detect_image(img_frame):
    # img_read = read_img(frame)
    img_proce = processing(img_frame)
    corners  = find_corners(img_proce, img_frame)
    return corners if corners !=0 else 0
    
def extract_image(img_frame,corners):
    img_crop = image_transform(img_frame,corners)
    img_matrix = create_img_matrix(img_frame, img_crop)
    extrac_number(img_matrix)
    return img_matrix, img_crop

