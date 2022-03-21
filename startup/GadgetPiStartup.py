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
vgaFont = os.path.dirname(os.path.realpath(__file__)) + '/Perfect DOS VGA 437.ttf' 

y = 10 # start 10 pixles down
hostname = socket.gethostname()
font = ImageFont.truetype(vgaFont,24)
w, h = font.getsize(hostname)
x = (inky_display.WIDTH / 2) - (w / 2)
# draw a box around the text with 5 pixel padding
draw.rounded_rectangle([(x-7,y-5),(x+w+5, y+h+5)],
                       5, inky_display.RED, inky_display.BLACK, 2)
draw.text((x, y), hostname, inky_display.BLACK, font)
y += h + 15

font = ImageFont.truetype(vgaFont, 16)

net = ifcfg.interfaces() # this is a dictionary. I want wlan0 and usb0, but want to check if present first

if('wlan0' in net and 'inet' in net['wlan0'] and net['wlan0']['inet'] is not None): 
    text = 'w:' + net['wlan0']['inet'] + '\n'
    w, h = font.getsize(text)
    draw.text((10, y), text, inky_display.BLACK, font)
    y += h + 2

if('usb0' in net and 'inet' in net['usb0'] and net['usb0']['inet'] is not None): 
    text = 'u:' + net['usb0']['inet']
    w, h = font.getsize(text)
    draw.text((10, y), text, inky_display.BLACK, font)
    y += h + 2

inky_display.set_image(img)
inky_display.show()
