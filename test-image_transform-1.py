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
contours, hierarchy = cv2.findContours(edged,
	cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#cv2.imshow('Canny Edges After Contouring', edged)

print("Number of Contours found = " + str(len(contours)))
print("Print the contours: ",contours)
# Draw all contours
# -1 signifies drawing all contours
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
img = cv2.imread('/Users/nguyenvanan2730/Projects/Sudoku-AWS/sudoku/Images/Input-image-example/sudoku-image-example-level100.jpeg')
dimensions = img.shape
print(f"Dimensions: {dimensions}")

# Make one pixel red
image = cv2.circle(img, (589,374), radius=10, color=(0, 0, 255), thickness=-1) #Red
image = cv2.circle(img, (70,384), radius=15, color=(0, 255, 0), thickness=-1)  #Green
image = cv2.circle(img, (61,927), radius=20, color=(255, 0, 0), thickness=-1)  #Blue
image = cv2.circle(img, (623,951), radius=25, color=(0, 255, 255), thickness=-1) #Yellow
# Save
cv2.imshow("result.png",image)
cv2.waitKey(0)
cv2.destroyAllWindows()