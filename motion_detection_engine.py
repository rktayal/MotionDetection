# Template Class to detect motion across 
# sequence of frames
#

import os
import sys
import cv2
import time
import imutils
import argparse
from datetime import datetime
from imutils.video import VideoStream

class MotionDetection(object):
    """ The class is provides methods to detect motion across frames
    """
    def __init__(self, minarea=500, thresh=25,
                visual=1, width=None, height=None):
        print ('no fucks given')
        self.min_area = minarea
        self.delta_thresh = thresh
        self.visual = visual
        self.width = width
        self.height = height
        self.cnts = None
        self.thresh = None
        self.frame_delta = None
        self.reference_frame = None
        self.frame = None
        self.status = "No motion"

    def get_contours(self):
        return self.cnts

    def get_thresh(self):
        return self.thresh

    def get_frame_delta(self):
        return self.frame_delta

    def _pre_process_frame(self, frame):
        if self.width:
            frame = cv2.resize(frame, (self.width, self.height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def set_reference_frame(self, frame):
        pframe = self._pre_process_frame(frame)
        self.reference_frame = pframe

    def _compute_difference(self, frame):
        ''' The method computes pixel wise difference between the
        reference frame and current frame
        '''
        pframe = self._pre_process_frame(frame)
        self.frame_delta = cv2.absdiff(self.reference_frame, pframe)
        self.thresh = cv2.threshold(self.frame_delta, self.delta_thresh,
                                    255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find
        # contours on thresholded images
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)
        self.cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = imutils.grab_contours(self.cnts)

    def _update_frame(self, c):
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        self.status = "Motion Detected"

    def is_motion(self, frame):
        self.frame = frame
        if self.width:
            self.frame = cv2.resize(self.frame, (self.width, self.height))
        self.status = "No motion"
        self._compute_difference(frame)
        motion = 0
        for c in self.cnts:
            # if the contours is too small, no motion
            if cv2.contourArea(c) > self.min_area:
                self._update_frame(c)
                motion = 1
        if self.visual:
            self.show_visual()
        if motion:
            return True
        return False

    def show_visual(self):
        cv2.putText(self.frame, "Status: {}".format(self.status), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(self.frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, self.frame.shape[0]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Feed", self.frame)
        cv2.imshow("Thresh", self.thresh)
        cv2.imshow("Frame Delta", self.frame_delta)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            cv2.destroyAllWindows()
            sys.exit(-1)
