import time
from Focuser import Focuser
from picamera2 import *

focuser = Focuser('/dev/v4l-subdev1')
print(focuser)
picam2 = Picamera2()
capture_config = picam2.still_configuration()
picam2.configure(capture_config)
picam2.start()
start = time.perf_counter()
for focus in range(1024, 4095, 256):
    focuser.set(Focuser.OPT_FOCUS, focus)
    picam2.capture_file(f"test_full-{focus}.jpg")
print(time.perf_counter() - start)
