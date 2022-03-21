#!/usr/bin/env python
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import ifcfg
import socket
import os

inky_display = auto()
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

hostname = socket.gethostname()
net = ifcfg.interfaces() # this is a dictionary,. I want wlan0 and usb0, but want to check if present first
text = hostname + "\n"
if('wlan0' in net and 'inet' in net['wlan0'] and net['wlan0']['inet'] is not None): 
    text += 'w:' + net['wlan0']['inet'] + '\n'
if('usb0' in net and 'inet' in net['usb0'] and net['usb0']['inet'] is not None): 
    text += 'u:' + net['usb0']['inet']

drawFont = ImageFont.truetype(
    font=os.path.dirname(os.path.realpath(__file__)) + '/Perfect DOS VGA 437.ttf', 
    size=16) # multiples of 8
draw.text((10, 10), text, inky_display.BLACK, drawFont)

inky_display.set_image(img)
inky_display.show()
