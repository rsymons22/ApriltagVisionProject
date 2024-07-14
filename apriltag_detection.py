import cv2 as cv
import numpy as np
import apriltag
import os
import math

# cv displays will show on the pi, w/o this command program crashes
#os.system("export DISPLAY=:0.0")

HEIGHT_PX = 480
WIDTH_PX = 640

class ApriltagDetection():
   def __init__(self):
      data = np.load("calibration_data.npz")
      self.mtx = data["mtx"]
      self.dist = data["dist"]
      self.roi = data["roi"]
      self.newmtx = data["newmtx"]

      self.detector = apriltag.Detector(apriltag.DetectorOptions(families="tag36h11"))

      self.horiz = None
      self.vert = None


   def run_detection(self):
      cap = cv.VideoCapture(0)
      while True:
         status, img = cap.read()

         dst = cv.undistort(img, self.mtx, self.dist, None, self.newmtx)

         x, y, w, h = self.roi
         dst = dst[y:y+h, x:x+w]

         gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

         results = self.detector.detect(gray)
         
         if results != []:
            r = results[0]

            # Corners and center points
            (ptA, ptB, ptC, ptD) = r.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))

            center = (int(r.center[0]), int(r.center[1]))

            # Calculate offsets
            self.horiz = center[0] - (WIDTH_PX / 2)
            self.vert = center[1] - (HEIGHT_PX / 2)

            # Draw pertinent information on the screen
            cv.putText(dst, f"t{str(r.tag_id)}|h:{self.horiz}|v:{self.vert}", (ptA[0], ptA[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.line(dst, ptA, ptB, (0, 255, 0), 2)
            cv.line(dst, ptB, ptC, (0, 255, 0), 2)
            cv.line(dst, ptC, ptD, (0, 255, 0), 2)
            cv.line(dst, ptD, ptA, (0, 255, 0), 2)

            cv.circle(dst, center, 1, (0, 0, 255), 2)

            #print(math.atan2(r.homography[1, 0], r.homography[0, 0]))
         else:
            self.horiz = None
            self.vert = None

         
         cv.imshow("Video", dst)
         cv.waitKey(10)

         # if cv.waitKey(10) in range(128):
         #    break
      cv.destroyAllWindows()



