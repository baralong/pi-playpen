import time
from Focuser import Focuser
import libcamera
import cv2
from datetime import datetime

focuser = Focuser('/dev/v4l-subdev1')
width = 4656
height = 3496

# Instantiate the libcamera class
cam = libcamera.libcamera()
ret = cam.initCamera(width, height, libcamera.PixelFormat.RGB888, buffercount=1 , rotation=0)
if not ret: exit
ret = cam.startCamera()
focuser.set(Focuser.OPT_FOCUS, 0)
time.sleep(1)

startTime = datetime.now().strftime('%Y%m%d%H%M')
start = time.perf_counter()
for focus in range(0, 4095, 256):
    focuser.set(Focuser.OPT_FOCUS, focus)
    ret, data = cam.readFrame()
    if not ret:
        continue
    frame = data.imageData
    cam.returnFrameBuffer(data)
    cv2.imwrite(f'/home/pi/stack-{start}-{focus:04}.jpg', frame)

print(time.perf_counter() - start)
