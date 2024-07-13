import cv2 as cv
import numpy as np
import apriltag
import os
import RPi.GPIO as GPIO


# cv displays will show on the pi, w/o this command program crashes
#os.system("export DISPLAY=:0.0")

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(36, GPIO.IN)
# while True:
#    print(GPIO.input(36))

HEIGHT_PX = 480
WIDTH_PX = 640

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

   gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

   results = detector.detect(gray)
   #print(results)

   for r in results:

      # Corners and center points
      (ptA, ptB, ptC, ptD) = r.corners
      ptB = (int(ptB[0]), int(ptB[1]))
      ptC = (int(ptC[0]), int(ptC[1]))
      ptD = (int(ptD[0]), int(ptD[1]))
      ptA = (int(ptA[0]), int(ptA[1]))

      center = (int(r.center[0]), int(r.center[1]))

      # Calculate offsets
      horiz = center[0] - (WIDTH_PX / 2)
      vert = center[1] - (HEIGHT_PX / 2)

      # Draw pertinent information on the screen
      cv.putText(dst, f"t{str(r.tag_id)}|h:{horiz}|v:{vert}", (ptA[0], ptA[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
      cv.line(dst, ptA, ptB, (0, 255, 0), 2)
      cv.line(dst, ptB, ptC, (0, 255, 0), 2)
      cv.line(dst, ptC, ptD, (0, 255, 0), 2)
      cv.line(dst, ptD, ptA, (0, 255, 0), 2)

      cv.circle(dst, center, 1, (0, 0, 255), 2)

      



   cv.imshow("Video", dst)

   


   if cv.waitKey(10) in range(128):
      break
cv.destroyAllWindows()

