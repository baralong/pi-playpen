#!/usr/bin/env python
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import socket

inky_display = auto()
inky_display.set_border(inky_display.BLACK)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
from font_fredoka_one import FredokaOne

hostname = socket.gethostname()
net = ifcfg.interfaces() # this is a dictionary,. I want wlan0 and usb0, but want to check if present first
text = hostname + "\n"
if('wlan0' in net and 'inet' in net['wlan0'] and net['wlan0']['inet'] is not None): 
    text += 'w:' + net['wlan0']['inet'] + '\n'
if('usb0' in net and 'inet' in net['usb0'] and net['usb0']['inet'] is not None): 
    text += 'u:' + net['usb0']['inet']

font = ImageFont.truetype(FredokaOne, 20)
draw.text((20, 20), text, inky_display.BLACK, font)

inky_display.set_image(img)
inky_display.show()
