import numpy as np
import cv2

img = cv2.imread("sample pic/card.jpg")

hor = np.hstack((img,img))
ver = np.vstack((img,img))

cv2.imshow("imh",hor)
cv2.imshow("vert",ver)
'''Both image should be same typ mean no one is grey or other is color 
as it is matrix typ'''



cv2.waitKey(0)
