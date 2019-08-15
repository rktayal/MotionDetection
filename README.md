# MotionDetection
The repo includes a plug and play basic motion detection module which can be used across various Vision based application. Credits to Adrian Rosebrock for his comprehensive tutorial on the same.

### Requirements
Below are the Python packages which will be required.
```
1. imutils
2. opencv-python
```
You can install above python packages using `pip install <package_name>` command.


### Run Demo app
Sample code to use the Motion Detection module is shown below:
```
import cv2
from motion_detection_engine import MotionDetection

cap = cv2.VideoCapture('test_data/video_file.mp4')
md_obj = MotionDetection(width=640, height=480)
ret, frame = cap.read()        
md_obj.set_reference_frame(frame)
while True:
    ret, frame = cap.read()
    status = md_obj.is_motion(frame)
    print(status)
```
The above demo code does the following things in order.
- Initialize a VideoCapture object to fetch frames. `cv2.VideoCapture(vid_file)`
- Initialize the motion detection class object.
  `class MotionDetection(visual=1, minarea=500, thresh=25, width=None, height=None)`

    Parameters:

    1. `visual`: To toggle the visual dispaly of frames. (enabled by default)
    2. `minarea`: Minimum area to take into consideration of contour for motion detection (500 by default)
    3. `thresh`: Value used to threshold the frameDelta i.e. difference between refrence frame and current frame.
    if the pixel difference is less than `thresh`, it will be discarded.
    4. `width`: To resize the frame's width (will retain original frame's width, if not passed)
    5. `height`: To resize the frame's height (will retain original frame's height, if not passed)<br />
    Above we have called the `MotionDetection()` constructor with no arguments. Therefore, it will take the original frame width and height.
- Set the reference frame by calling the `md_obj.set_reference_frame(frame)` method.
- Fetch frames from `cap` object and compare them with reference frame using `md_obj.is_motion(frame)` to detect if there is any motion.

Similarly you can also get the metrics of difference between the reference frame and the current frame using
get methods for contours, thresh and frame delta.
```
frame_delta = md_obj.get_frame_delta()
contours = md_obj.get_contours()
```
### Background on Motion Detection
It computes the difference between the reference frame and subsequent new frames from the video stream.<br /><br />
Computing the difference between two frames is a simple subtraction, where we take the absolute value of their corresponding pixel intensity differences. <br /><br />
`delta = |background_model – current_frame|` <br /><br />
Next we will threshold the delta, based on the value of `thresh`. Only those pixels will be considered whose delta value
will be higher than the `thresh` value. <br />
Once this computation is done, we will extract the contours (using contour detection) to find outlines of such areas. If the contour area is larger than our supplied `minarea` , then we’ll draw the bounding box surrounding the motion region and the status will be motion detected.<br />
### References
- https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
