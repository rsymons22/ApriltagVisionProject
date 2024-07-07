import cv2 as cv
import numpy as np
import apriltag
import AprilTag.scripts.apriltag

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

cap = cv.VideoCapture(0)
while True:
   status, img = cap.read()

   res, overlay = AprilTag.scripts.apriltag.detect_tags(img, detector, (fx, fy, cx, cy), TAG_WIDTH_M, 3, 3, True)

   cv.imshow("Streaming Video", overlay)
   if cv.waitKey(10) == 13:
      break
cv.destroyAllWindows()

