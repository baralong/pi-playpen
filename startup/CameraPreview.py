import time
from Focuser import Focuser
import libcamera
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path
from displayhatmini import DisplayHATMini

focuser = Focuser('/dev/v4l-subdev1')
width = 4656
height = 3496

# Instantiate the libcamera class
cam = libcamera.libcamera()
print((DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
ret = cam.initCamera(DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT, libcamera.PixelFormat.BGR888, buffercount=1, rotation=0)
ret = cam.startCamera()
buffer = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
draw = ImageDraw.Draw(buffer)
display_hat = DisplayHATMini(buffer)

if ret != 0:
    cam.stopCamera()
    cam.closeCamera()
    exit()

# focus adjustment
focus_step = 10
def step_focus_up():
    focuser.set(Focuser.OPT_FOCUS,focuser.get(Focuser.OPT_FOCUS) + focus_step)
def step_focus_down():
    focuser.set(Focuser.OPT_FOCUS,focuser.get(Focuser.OPT_FOCUS) - focus_step)

def button_callback(pin):
    if pin == display_hat.BUTTON_A:
            step_focus_up()
    elif pin == display_hat.BUTTON_B:
            step_focus_down()
    elif pin == display_hat.BUTTON_C:
            pass
    elif pin == display_hat.BUTTON_D:
            pass

display_hat.on_button_pressed(button_callback)

input("init")
focuser.set(Focuser.OPT_FOCUS, 2048)

startTime = datetime.now().strftime('%Y%m%dt%H%M')
path = f'/home/pi/stack/D{startTime}'
Path(path).mkdir(parents=True, exist_ok=True)
time.sleep(0.5)
start = time.perf_counter()
while True:
     ret, data = cam.readFrame()
     if not ret:
         continue
     frame = data.imageData
     img =  Image.fromarray(frame, 'RGB')
     display_hat.buffer = img
     display_hat.display()
     cam.returnFrameBuffer(data)

# for focus in range(4095, 2000, -50):
#     focuser.set(Focuser.OPT_FOCUS, focus)
#     ret, data = cam.readFrame()
#     if not ret:
#         continue
#     frame = data.imageData
#     cam.returnFrameBuffer(data)
#     cv2.imwrite(f'{path}/pic-{(4095-focus):04}.jpg', frame)

# print(time.perf_counter() - start)
# cam.stopCamera()
# cam.closeCamera()
