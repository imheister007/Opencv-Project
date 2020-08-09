import numpy as np
import cv2


# FUNCTION TO STACK IMAGES
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


'''function
    RETR_EXTERNAL--> retrieve external contours


'''


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    '''for each contour find area...'''
    for cnt in contours:

        area = cv2.contourArea(cnt)
        print(area)

        # will draw each contour
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)

            # going to count how many corner point
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))  # this will give corner point
            objcor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            if objcor == 3:
                objectType = "tri"
            elif objcor == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objcor > 4:
                objectType = "Circle"

            else:
                objectType = "None"
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # this will get bounding boxex over shapes
            cv2.putText(imgContour, objectType,
                        (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX,
                        0.5, (0, 0, 0), 2)


img = cv2.imread("sample pic/check1.png")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgContour = img.copy()

imgCAnny = cv2.Canny(imgBlur, 50, 50)  # fiding edges
imgBlack = np.zeros_like(img)

getContours(imgCAnny)
# sending image to contour function


imgstack = stackImages(0.8, ([img, imgGray, imgGray],
                             [imgCAnny, imgContour, imgBlack]))
'''We made two row'''

cv2.imshow("Stack", imgstack)
cv2.waitKey(0)