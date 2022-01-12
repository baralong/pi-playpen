import LCD_1in44
import LCD_Config
import time
from PIL import Image,ImageDraw,ImageFont,ImageColor
import ifcfg
import socket
from gpiozero import CPUTemperature
import psutil

LCD = LCD_1in44.LCD()
LCD.LCD_Init(LCD_1in44.D2U_L2R)
LCD.LCD_ShowImage(Image.new("RGB", (LCD.width, LCD.height), "BLACK"),0,0)

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
    while(len(allStats) > LCD.width):
        allStats.pop(-1)

    image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf', 10)
    draw.multiline_text((5,5), text, fill = "WHITE", font = font)
    draw.line([(0,LCD.height-51 -20),(LCD.width, LCD.height-51-20)], "WHITE")
    draw.line([(0,LCD.height -20),(LCD.width, LCD.height-20)], "WHITE")
    draw.text((5,LCD.height-15), f"T:{currentStats.temperature}°C", fill = "RED", font = font)
    draw.text((6+(2*LCD.width/3),LCD.height-15), f"C:{currentStats.cpu}%", fill = "GREEN", font = font)
    draw.text((12+ (LCD.width/3),LCD.height-15), f"M:{currentStats.memory}%", fill = "BLUE", font = font)
    for x in range(len(allStats)):
        draw.point((x,LCD.height-(allStats[x].temperature/2)-21),"RED") 
        draw.point((x,LCD.height-(allStats[x].cpu/2)-21),"GREEN") 
        draw.point((x,LCD.height-(allStats[x].memory/2)-21),"BLUE") 
    LCD.LCD_ShowImage(image,0,0)

while(True):
    drawLCD()
    time.sleep(1)
