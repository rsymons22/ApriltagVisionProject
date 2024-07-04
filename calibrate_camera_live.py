import numpy as np
import cv2 as cv
from time import sleep
import glob

image_num = 0
camera = cv.VideoCapture(0)

while True:
    status, img = camera.read()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,6), None)

    print(f"ret: {ret}")

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("success")
        cv.imwrite(f"image_success{image_num}.jpg", img)
        image_num += 1

    cv.imshow('img', img)
    if cv.waitKey(3000) == 13: break
        
    # sleep(4)
    # print("ready")
    # sleep(2)

cv.destroyAllWindows()
