#1. Import the image
import cv2
    #url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-1.png"
url = "/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-5.png"
img = cv2.imread(url) #画像は強制的にグレイスケール画像として読み込まれます。
    #cv2.imshow("read_img",image)

#2. Preprocessing the image
    #2.1 Gaussian blur:  reduce noise obtained in thresholding algorithm (adaptive thresholding)
    #convert color image to gray image
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    #ksize.width and ksize.height can differ but they both must be positive and odd.
img_gauss = cv2.GaussianBlur(img.copy(), (7, 7), 0) 

    #2.2 Thresholding: Segmenting the regions of the image
img_thres = cv2.adaptiveThreshold(img_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 131, 2)
    #cv2.imshow("adaptiveThreshold",img_thres)
    
    #2.3 Dilating the image: In cases like noise removal, erosion is followed by dilation.
#img_bitwise = cv2.bitwise_not(img_thres,img_thres)
img_bitwise = cv2.bitwise_not(img_gauss,img_gauss)

cv2.imwrite("/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/preprocess-input-image/image_transform.png",img_bitwise)