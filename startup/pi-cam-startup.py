from displayhatmini import DisplayHATMini
import time
from PIL import Image,ImageDraw,ImageFont,ImageColor
import ifcfg
import socket
from gpiozero import CPUTemperature
import psutil
from Focuser import Focuser
import libcamera
import numpy
from datetime import datetime
from pathlib import Path

class processStats:
    color = {
            'temperature': 'RED',
            'cpu': 'GREEN',
            'memory': 'BLUE',
        }
    def __init__(self, temperature, cpu, memory) -> None:
        self.temperature = round(temperature)
        self.cpu = round(cpu)
        self.memory = round(memory)

allStats = []

def drawLCD():
    hostname = socket.gethostname()
    net = ifcfg.interfaces() # this is a dictionary, I want wlan0 and usb0, but want to check if present first
    text = hostname + "\n"
    if('wlan0' in net and 'inet' in net['wlan0'] and net['wlan0']['inet'] is not None): 
        text += 'w:' + net['wlan0']['inet'] + '\n'
    if('usb0' in net and 'inet' in net['usb0'] and net['usb0']['inet'] is not None): 
        text += 'u:' + net['usb0']['inet']
    currentStats = processStats(
            CPUTemperature().temperature, 
            psutil.cpu_percent(), 
            psutil.virtual_memory().percent)
    allStats.insert(0, currentStats)
    while(len(allStats) > DisplayHATMini.WIDTH):
        allStats.pop(-1)

    font = ImageFont.truetype('/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf', 16)
    draw.multiline_text((5,5), text, fill = "WHITE", font = font)
    clock_text = datetime.now().strftime('%Y-%m-%d %H:%M')
    draw.text((DisplayHATMini.WIDTH - 5, 5), clock_text, fill = "RED", font = font, anchor = 'ra')
    draw.line([(0,DisplayHATMini.HEIGHT-51 -20),(DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT-51-20)], "WHITE")
    draw.line([(0,DisplayHATMini.HEIGHT -20),(DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT-20)], "WHITE")
    draw.text((5,DisplayHATMini.HEIGHT-15), f"T:{currentStats.temperature}°C", fill = "RED", font = font)
    draw.text((6+(2*DisplayHATMini.WIDTH/3),DisplayHATMini.HEIGHT-15), f"C:{currentStats.cpu}%", fill = "GREEN", font = font)
    draw.text((12+ (DisplayHATMini.WIDTH/3),DisplayHATMini.HEIGHT-15), f"M:{currentStats.memory}%", fill = "BLUE", font = font)
    for x in range(len(allStats)):
        draw.point((x,DisplayHATMini.HEIGHT-(allStats[x].temperature/2)-21),"RED")
        draw.point((x,DisplayHATMini.HEIGHT-(allStats[x].cpu/2)-21),"GREEN")
        draw.point((x,DisplayHATMini.HEIGHT-(allStats[x].memory/2)-21),"BLUE")
    display_hat.display()

focuser = Focuser('/dev/v4l-subdev1')
width = 4656
height = 3496

# Instantiate the libcamera class
cam = libcamera.libcamera()
print((DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
ret = cam.initCamera(DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT, libcamera.PixelFormat.BGR888, buffercount=1, rotation=0)
ret = cam.startCamera()

if ret != 0:
    cam.stopCamera()
    cam.closeCamera()
    exit()

buffer = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
draw = ImageDraw.Draw(buffer)
display_hat = DisplayHATMini(buffer)

def color_angle(angle):
    # each color increases and decreases over 240 degrees overlapping the next color
    # red's peak at 0, green at 120, blue at 240
    step = 255/120
    if angle < 120:
        return (255 - round(step * angle), round(step * angle), 0)
    angle -= 120
    if angle < 120:
        return (0, 255 - round(step * angle), round(step * angle))
    angle -= 120
    if angle < 120:
        return (round(step * angle), 0, 255 - round(step * angle))

center_square = [
    (round((DisplayHATMini.WIDTH - DisplayHATMini.HEIGHT)/2) + 5, 5),
    (round((DisplayHATMini.WIDTH + DisplayHATMini.HEIGHT)/2) - 5, DisplayHATMini.HEIGHT - 5)]

delay = 0.0001
for angle in range(360):
    draw.pieslice(
        xy = center_square,
        outline = color_angle(angle),
        fill = color_angle(angle),
        width = 0,
        start = angle,
        end = angle+1)
    currentStats = processStats(
            CPUTemperature().temperature,
            psutil.cpu_percent(),
            psutil.virtual_memory().percent)
    display_hat.display()
    time.sleep(delay)

drawLCD()
time.sleep(0.5)

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

focuser.set(Focuser.OPT_FOCUS, 2048)


while True:
    ret, data = cam.readFrame()
    if not ret:
        continue
    frame = data.imageData
    buffer.paste(Image.fromarray(frame, 'RGB'))
    cam.returnFrameBuffer(data)
    drawLCD()
