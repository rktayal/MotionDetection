import os
import sys
import cv2
import argparse
from imutils.video import VideoStream

from motion_detection_engine import MotionDetection

if  __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())
     
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        vs = VideoStream(src=0).start()
 
    # otherwise, we are reading from a video file
    else:
        vs = cv2.VideoCapture(args["video"])

    md_obj = MotionDetection(width=640, height=480)
    frame = vs.read()
    ref_frame = frame if args.get("video", None) is None else frame[1]
    md_obj.set_reference_frame(ref_frame)
    while True:
        frame = vs.read()
        frame = frame if args.get("video", None) is None else frame[1]
        status = md_obj.is_motion(frame)
        print ('status', status)
