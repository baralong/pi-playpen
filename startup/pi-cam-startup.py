from displayhatmini import DisplayHATMini
import time
from PIL import Image,ImageDraw,ImageFont,ImageColor
import ifcfg
import socket
from gpiozero import CPUTemperature
import psutil

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

buffer = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
draw = ImageDraw.Draw(buffer)
display_hat = DisplayHATMini(buffer)

def drawLCD():
    hostname = socket.gethostname()
    net = ifcfg.interfaces() # this is a dictionary,. I want wlan0 and usb0, but want to check if present first
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

    image = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT), "BLACK")
    draw.rectangle([(0,0),(DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT)], "BLACK","BLACK")
    font = ImageFont.truetype('/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf', 16)
    draw.multiline_text((5,5), text, fill = "WHITE", font = font)
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

while(True):
    drawLCD()
    time.sleep(1)
