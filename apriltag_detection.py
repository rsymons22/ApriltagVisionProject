import cv2 as cv
import numpy as np
import apriltag

data = np.load("calibration_data.npz")
mtx = data["arr_0"]
dist = data["arr_1"]

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

fx = mtx[0][0]
fy = mtx[1][1]
cx = mtx[0][2]
cy = mtx[1][2]

TAG_WIDTH_M = 0.1651

h = 480
w = 640
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

cap = cv.VideoCapture(0)
while True:
   status, img = cap.read()

   dst = cv.undistort(img, mtx, dist, None, newcameramtx)

   x, y, w, h = roi
   dst = dst[y:y+h, x:x+w]

   cv.imshow("Video", dst)

   gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

   print(detector.detect(gray))
   

   if cv.waitKey(10) in range(128):
      break
cv.destroyAllWindows()

