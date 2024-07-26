import cv2 as cv
import numpy as np
import apriltag
import os
import math

# Command to display grahics on pi: export DISPLAY=:0.0

HEIGHT_PX = 480
WIDTH_PX = 640
TAG_WIDTH_MM = 152.4 # 6in

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
      self.stop = False
      self.distance = None

   def calculate_distance(self, corners, theta):
      """
      Calculates the distance from the apriltag to the camera using the formula:

      D = (real_width * focal length x) / pixels_width

      :param corners: size 4 tuple of size 2 coordinate tuples of the 4 corners
      :param theta: yaw angle of the april tag
      :return: distance in inches

      """
      m1 = ((corners[0][0] + corners[3][0]) / 2, (corners[0][1] + corners[3][1]) / 2)
      m2 = ((corners[1][0] + corners[2][0]) / 2, (corners[1][1] + corners[2][1]) / 2)

      width_px = math.sqrt((m2[0] - m1[0])**2 + (m2[1] - m1[1])**2)
      # Rotated april tags will appear to have a smaller "width", this can be corrected
      # by using the formula: real_width = apparent_width / cos(theta)
      width_px_adjusted = math.fabs(width_px / math.cos(theta))

      # Focal length is in mm, so must first calculate dist in mm then convert to inches
      dist_mm = (TAG_WIDTH_MM * self.newmtx[0][0]) / width_px_adjusted
      dist_in = dist_mm / 25.4
      self.distance = dist_in

   def run_detection(self):
      cap = cv.VideoCapture(0)
      while True:
         if self.stop: break

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
            self.calculate_distance(r.corners, math.atan2(r.homography[1, 0], r.homography[0, 0]))
            
         else:
            self.horiz = None
            self.vert = None

         
         cv.imshow("Video", dst)
         cv.waitKey(10)

         # if cv.waitKey(10) in range(128):
         #    break
      cv.destroyAllWindows()



