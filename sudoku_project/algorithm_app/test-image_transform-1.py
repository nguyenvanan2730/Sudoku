import cv2
import numpy as np

# Let's load a simple image with 3 black squares
image = cv2.imread('/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-level100.jpeg')

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 30, 200)

# Finding Contours
# Use a copy of the image e.g. edged.copy()
# since findContours alters the image
ext_contours, hierarchy = cv2.findContours(edged,
	cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)
deta=cv2.arcLength(ext_contours[0],True)
#曲線など多数の点で構成される輪郭をより少ない点で近似できます
#img_approx = cv2.approxPolyDP(contour, 0.015*deta, True)
img_approx = cv2.approxPolyDP(ext_contours[0], 0.015*deta, True)
#cv2.imshow('Canny Edges After Contouring', edged)
i=int(0)
for contour in ext_contours[0:1]:
	cv2.drawContours(image, ext_contours[i], -1, (0, 255, 0), 6)
	cv2.imshow('img_contours%d'%i, image)
	i=i+1
	x,y,w,h = cv2.boundingRect(contour)
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
	cv2.imshow("rectangle.png",image)
	print(x,y,w,h)
	# # Make one pixel red
	# image_point = cv2.circle(image, (x[0],x[1]), radius=10, color=(0, 0, 255), thickness=-1) #Red  ---> BOTTOM LEFT
	# image_point = cv2.circle(image, (y[0],y[1]), radius=15, color=(0, 255, 0), thickness=-1)  #Green  --->TOP LEFT
	# image_point = cv2.circle(image, (x[0]+w,x[1]+h), radius=20, color=(255, 0, 0), thickness=-1)  #Blue  ===> TOP RIGHT
	# image_point = cv2.circle(image, (y[0]+w,y[1]+h), radius=25, color=(0, 255, 255), thickness=-1) #Yellow ---> BOTTOM RIGHT
	# cv2.imshow("result.png",image_point)
cv2.waitKey(0)

print("Number of Contours found = " + str(len(ext_contours)))
print("Print the contours[0]: ",ext_contours[0])
print("Print the img_approx:", img_approx)
# Draw all contours
# -1 signifies drawing all contours
#cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
cv2.drawContours(image, ext_contours[0], -1, (0, 255, 0), 6)

cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import cv2
img = cv2.imread('/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-level11.jpeg')
# dimensions = img.shape
# print(f"Dimensions: {dimensions}")

# # Make one pixel red
# image_point = cv2.circle(img, (514,388), radius=10, color=(0, 0, 255), thickness=-1) #Red  ---> BOTTOM LEFT
# image_point = cv2.circle(img, (68,416), radius=15, color=(0, 255, 0), thickness=-1)  #Green  --->TOP LEFT
# image_point = cv2.circle(img, (49,897), radius=20, color=(255, 0, 0), thickness=-1)  #Blue  ===> TOP RIGHT
# image_point = cv2.circle(img, (610,838), radius=25, color=(0, 255, 255), thickness=-1) #Yellow ---> BOTTOM RIGHT
# # Save
# cv2.imshow("result.png",image_point)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # #[(170, 366), (128, 846), (650, 871), (636, 366)]