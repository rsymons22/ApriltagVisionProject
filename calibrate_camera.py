import numpy as np
import cv2 as cv
import glob

# chessboard dimensions
HEIGHT = 9
WIDTH = 6

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((WIDTH*HEIGHT,3), np.float32)
objp[:,:2] = np.mgrid[0:HEIGHT,0:WIDTH].T.reshape(-1,2)
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob("calibration_pictures/*.jpg")

flag = True
 
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if flag: cv.imwrite("before_img.jpg", img)
    
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (HEIGHT,WIDTH), None)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
    
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
    
        # Draw and display the corners
        cv.drawChessboardCorners(img, (HEIGHT,WIDTH), corners2, ret)

    if flag: cv.imwrite("after_img.jpg", img)
    cv.imshow('img', img)
    cv.waitKey(500)
    flag = False
 
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(f"ret: {ret} | mtx: {mtx} | dist: {dist} | rvecs: {rvecs} | tvecs: {tvecs}")
np.savez("calibration_data", mtx, dist)

print("Calibration data exported to calibration_data.npz")

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
 
print("Total error: {}".format(mean_error/len(objpoints)))