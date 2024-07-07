import cv2 as cv
import numpy as np
import apriltag

data = np.load("calibration_data.npz")
mtx = data["mtx"]
dist = data["dist"]
roi = data["roi"]
newmtx = data["newmtx"]

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

cap = cv.VideoCapture(0)
while True:
   status, img = cap.read()

   dst = cv.undistort(img, mtx, dist, None, newmtx)

   x, y, w, h = roi
   dst = dst[y:y+h, x:x+w]

   cv.imshow("Video", dst)

   gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

   print(detector.detect(gray))
   
   if cv.waitKey(10) in range(128):
      break
cv.destroyAllWindows()

