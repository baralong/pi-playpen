#!/usr/bin/env python
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import ifcfg
import socket
import os
import shutil 
import getpass

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f'{round(size)}{power_labels[n]}'

inky_display = auto()
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
vga_font = os.path.dirname(os.path.realpath(__file__)) + '/Perfect DOS VGA 437.ttf' 

y = 10 # start 10 pixles down
hostname = socket.gethostname()
font = ImageFont.truetype(vga_font,24)
w, h = font.getsize(hostname)
x = (inky_display.WIDTH / 2) - (w / 2)

# draw a box around the text with 5 pixel padding
draw.rounded_rectangle([(x-7,y-5),(x+w+5, y+h+5)],
                       5, inky_display.RED, inky_display.BLACK, 2)
draw.text((x, y), hostname, inky_display.WHITE, font)
y += h + 15
y2=y

font_awesome_solid = ImageFont.truetype('./Font Awesome 6 Free-Solid-900.otf', 16)
font_awesome_brands = ImageFont.truetype('./Font Awesome 6 Brands-Regular-400.otf', 16)
font = ImageFont.truetype(vga_font, 16)

net = ifcfg.interfaces() # this is a dictionary. I want wlan0 and usb0, but want to check if present first

if('wlan0' in net and 'inet' in net['wlan0'] and net['wlan0']['inet'] is not None): 
    w, h = font_awesome_solid.getsize('\uf1eb')
    draw.text((5, y), '\uf1eb', inky_display.RED, font_awesome_solid)
    draw.text((w + 10, y), net['wlan0']['inet'], inky_display.BLACK, font)
    y += h + 3

if('usb0' in net and 'inet' in net['usb0'] and net['usb0']['inet'] is not None): 
    w, h = font_awesome_brands.getsize('\uf287')
    draw.text((5, y), '\uf287', inky_display.RED, font_awesome_brands)
    draw.text((w + 10, y), net['usb0']['inet'], inky_display.BLACK, font)
    y += h + 3

if(getpass.getuser() == 'root'):
    os.system('umount /usbdisk.d')
    os.system('mount -o loop -t exfat /usbdisk.img /usbdisk.d')
    print('remounted')

usage = shutil.disk_usage("/usbdisk.d")
font = ImageFont.truetype(vga_font, 16)

text = f'u:{format_bytes(usage.used)}'
w, h = font.getsize(text)
x = 3
y = inky_display.HEIGHT - h - 4
draw.rectangle(
        xy = [(0, y-2),(inky_display.WIDTH-1, inky_display.HEIGHT-1)],
        fill = inky_display.RED,
        outline = inky_display.BLACK,
        width = 1)

draw.text((x,y), text, inky_display.WHITE, font)

text = f'f:{format_bytes(usage.free)}'
w, h = font.getsize(text)
x = (inky_display.WIDTH - w)/2
draw.text((x,y), text, inky_display.WHITE, font)

text = f't:{format_bytes(usage.total)}'
w, h = font.getsize(text)
x = inky_display.WIDTH - 4 - w
draw.text((x,y), text, inky_display.WHITE, font)

y -= 6 # space above

usageSize = y - y2
draw.ellipse(xy = [(inky_display.WIDTH - usageSize, y2),
                   (inky_display.WIDTH-2, y-2)],
             outline = inky_display.BLACK, 
             fill = inky_display.WHITE, 
             width = 2)

draw.pieslice(xy = [(inky_display.WIDTH - usageSize, y2),
                 (inky_display.WIDTH-2, y-2)],
             fill = inky_display.RED, 
             width = 2,
             start = 0,
             end = (usage.used/usage.total) * 360)

inky_display.set_image(img)
inky_display.show()
