# MotionDetection
The repo includes a plug and play basic motion detection module which can be used across various Vision based application using OpenCV-Python. Credits to Adrian Rosebrock for his comprehensive tutorial on the same.

### Requirements
```
1. imutils
2. opencv-python
```
You can instal above python packages using `pip install <package_name>` command.


### Run Demo app
Sample code to use the Motion Detection module is shown below:
```
cap = cv2.VideoCapture('video_file')
md_obj = MotionDetection()
ret, frame = cap.read()
md_obj.set_reference_frame(frame)
while True:
    ret, frame = cap.read()
    status = md_obj.is_motion(frame)
    print(status)
```
The above demo code does the following things in order.
- Initialize a VideoCapture object to fetch frames
- Initialize the motion detection class object.
  `class MotionDetection(visual=1, minarea=500, thresh=25, width=None, height=None)`
  Parameters:
    1. visual: To toggle the visual dispaly of frames. (enabled by default)
    2. minarea: Minimum area to take into consideration of contour for motion detection (500 by default)
    3. thresh: Value used to threshold the frameDelta i.e. difference between refrence frame and current frame.
    if the pixel difference is less than `thresh`, it will be discarded.
    4. width: To resize the frame's width (will retain original frame's width, if not passed)
    5. height: To resize the frame's height (will retain original frame's height, if not passed)
- Set the reference frame
- Fetch frames from `cap` object and compare them with reference frame using `md_obj.is_motion(frame)` to detect if there is any motion.

Similarly you can also get the metrics of difference between the reference frame and the current frame using
get methods for contours, thresh and frame delta.
```
frame_delta = md_obj.get_frame_delta()
contours = md_obj.get_contours()
```

### References
- https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
