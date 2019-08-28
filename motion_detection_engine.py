# Template Class to detect motion across 
# sequence of frames
#

import os
import sys
import cv2
import time
import types
import imutils
import argparse
from datetime import datetime
from imutils.video import VideoStream

class MotionDetection(object):
    """ The class is provides methods to detect motion across frames. It implements
        strategy design pattern that enables algorithm's behavior to be selected 
        at runtime. MotionDetection is a single class and replace 
        the method of this class at runtime, with a different function
        based on a given context.
    """
    def __init__(self, minarea=500, thresh=25,
                visual=1, width=None, height=None, algorithm=None):
        self.min_area = minarea
        self.delta_thresh = thresh
        self.visual = visual
        self.width = width
        self.height = height
        self.cnts = None
        self.thresh = None
        self.frame_delta = None
        self.reference_frame = None
        self.avg = None
        self.frame = None
        self.status = "No motion"
        if algorithm is not None:
            # take a function, bind it to this instance, and replace
            # the default bound method 'execute' with this new bound
            # method.
            self.name = "{}_{}".format(self.__class__.__name__, algorithm.__name__)
            print ('self.name, self.execute', self.name, self.execute)
            self.execute = types.MethodType(algorithm, self)
        else:
            self.name = "{}_default".format(self.__class__.__name__)


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
        # if the average frame is None, initialize it as well
        self.avg = pframe.copy().astype("float")

    def execute(self, frame):
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
        self.execute(frame)
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

def weighted_difference(self, frame):
    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between current
    # frame and running average
    pframe = self._pre_process_frame(frame)
    cv2.accumulateWeighted(pframe, self.avg, 0.5)
    self.frame_delta = cv2.absdiff(pframe, cv2.convertScaleAbs(self.avg))
    self.thresh = cv2.threshold(self.frame_delta, self.delta_thresh,
                                255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find
    # contours on thresholded images
    self.thresh = cv2.dilate(self.thresh, None, iterations=2)
    self.cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
    self.cnts = imutils.grab_contours(self.cnts)
