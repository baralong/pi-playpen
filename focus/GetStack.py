import time
from Focuser import Focuser
import libcamera
import cv2
from datetime import datetime
from pathlib import Path

focuser = Focuser('/dev/v4l-subdev1')
width = 4656
height = 3496

# Instantiate the libcamera class
cam = libcamera.libcamera()
ret = cam.initCamera(width, height, libcamera.PixelFormat.RGB888, buffercount=1, rotation=0)
ret = cam.startCamera()
if ret != 0: 
    cam.stopCamera()
    cam.closeCamera()
    exit()
input("init")
focuser.set(Focuser.OPT_FOCUS, 4095)

startTime = datetime.now().strftime('%Y%m%dt%H%M')
path = f'/home/pi/stack/D{startTime}'
Path(path).mkdir(parents=True, exist_ok=True)
time.sleep(0.5)
start = time.perf_counter()
for focus in range(4095, 2000, -50):
    focuser.set(Focuser.OPT_FOCUS, focus)
    ret, data = cam.readFrame()
    if not ret:
        continue
    frame = data.imageData
    cam.returnFrameBuffer(data)
    cv2.imwrite(f'{path}/pic-{(4095-focus):04}.jpg', frame)

print(time.perf_counter() - start)
cam.stopCamera()
cam.closeCamera()
