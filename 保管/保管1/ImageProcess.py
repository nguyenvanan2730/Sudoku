import cv2
import numpy as np

#1. Import the image
def read_img():
    url = "C://Users/nguye/Desktop/VanAn/SUDOKU/sudoku_an.jpg"
    image = cv2.imread(url) #画像は強制的にグレイスケール画像として読み込まれます。
    #cv2.imshow("read_img",image)
    return image

#2. Preprocessing the image
def processing(img):

    #2.1 Gaussian blur:  reduce noise obtained in thresholding algorithm (adaptive thresholding)
    #convert color image to gray image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    #ksize.width and ksize.height can differ but they both must be positive and odd.
    img_gauss = cv2.GaussianBlur(img.copy(), (9, 9), 0) 

    #2.2 Thresholding: Segmenting the regions of the image
    img_thres = cv2.adaptiveThreshold(img_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #cv2.imshow("adaptiveThreshold",img_thres)
    
    #2.3 Dilating the image: In cases like noise removal, erosion is followed by dilation.
    img_bitwise = cv2.bitwise_not(img_thres,img_thres)
    #cv2.imshow("bitwise_not",img_thres)
    return img_bitwise

#3. Find Contours
def find_corners(img_proce, img_read):

    #find the contours on the img_proce
    ext_contours,hierarchy = cv2.findContours(img_proce, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #ext_contours = ext_contours[0] if len(ext_contours) == 2 else ext_contours[1]
    #Make the contours sort from the big to small
    ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)

    for contour in ext_contours[0:1]:
        print("The lengt of contours: ", len(ext_contours))
        #輪郭の周囲の長さを計算できます
        deta=cv2.arcLength(contour,True)
        #曲線など多数の点で構成される輪郭をより少ない点で近似できます
        img_approx = cv2.approxPolyDP(contour, 0.015*deta, True)
        
        #if the contour after approxPolyDP have 4 point
        if len(img_approx) ==4:
            #Plot the point on the screen
            plt_approx = cv2.drawContours(img_read, img_approx, -1, (0,255,0), 3)
            #cv2.imshow("find_corers", plt_approx)
            
            #Number of data point before and after approxPolyDP
            #print(f"contour {contour}: before: {len(contour)}, after: {len(img_approx)}")
            #print(f"The value of img_approx: {img_approx}")
            
            #上下右左ポイントの座標取得
            # Index 0 - top-right
            #       1 - top-left
            #       2 - bottom-left
            #       3 - bottom-right
            # corners=[]
            # for corner in img_approx:
            # corners.append([corner[0][0], corner[0][1]])

            corners = [(corner[0][0],corner[0][1]) for corner in img_approx]

            return corners   

#4. Crop the image
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

    #Contruct new points to obtain top-down view of image
    dimensions = np.array([[0,0],[width-1,0],[width-1, height -1],[0, height -1]], dtype="float32")

    #convert to Numpy format
    ordered_corners = np.array([top_left, top_right, bottom_right, bottom_left], dtype = "float32")

    #Crop the image
    grid = cv2.getPerspectiveTransform(ordered_corners, dimensions)
    img_crop = cv2.warpPerspective(image,grid,(width,height))
    img_crop = cv2.resize(img_crop,(450,450))
    cv2.imshow("img_crop",img_crop)
    cv2.waitKey(0)
    #cv2.imwrite("C:/Users/huyen/OneDrive/Desktop/VanAn/SUDOKU/img_crop.jpeg",img_crop)
    return img_crop

#4. Create matrix 9x9 image
def create_img_matrix(img_read, img_crop):
    grid = np.copy(img_crop)
    grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)
    grid = cv2.bitwise_not(cv2.adaptiveThreshold(grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1))
    print("grid.shape: ", grid.shape)
    #cv2.imshow("grid",grid)
    edge_h = np.shape(grid)[0]
    edge_w = np.shape(grid)[1]
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

            img_cell_crop = img_crop[x0:x1, y0 : y1]
            #img_matrix_crop = cv2.resize(img_cell_crop,(28,28))
            #img_matrix_crop = cv2.cvtColor(img_matrix_crop, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/cell/img%d.jpeg"%i,img_cell_crop)
            img_matrix.append(img_cell_crop)

            i+=1
    return img_matrix

#5.Extract the number from the cell
def extrac_number():

    for i in range(81):
        
        img_num = cv2.imread("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/cell/img%d.jpeg"%i,0)
        #cv2.imshow("img_num", img_num)
        #thresold the image
        #gray = cv2.threshold(img_num, 128, 255, cv2.THRESH_BINARY)[1]
        gray = img_num
        #cv2.imshow("gray",gray)
        #Find contours
        cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #cv2.waitKey(0)
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)

            if (x < 3 or y < 3 or h < 3 or w < 3):
            # Note the number is always placed in the center
            # Since image is 28x28
            # the number will be in the center thus x >3 and y>3
            # Additionally any of the external lines of the sudoku will not be thicker than 3
                continue
            ROI = gray[y:y + h, x:x + w]
            cv2.imwrite("C://Users/nguye/Desktop/VanAn/SUDOKU/Image/number/img%d.jpeg"%i,gray)
    # increasing the size of the number allws for better interpreation,
    # try adjusting the number and you will see the differnce
        


img_read = read_img()
img_proce = processing(img_read)
corners  = find_corners(img_proce, img_read)
img_crop = image_transform(img_read,corners)
#img_crop2 = processing(img_crop)
img_matrix = create_img_matrix(img_read, img_crop)
#extrac_number()

cv2.waitKey(0)
cv2.destroyAllWindows("")