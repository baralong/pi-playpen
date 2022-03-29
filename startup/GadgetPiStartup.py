#!/usr/bin/env python
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import ifcfg
import socket
import os
import shutil 
import getpass
import psutil

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
font_awesome_brands = ImageFont.truetype('./Font Awesome 6 Brands-Regular-400.otf', 24)
font_dejavu = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
y = 5
x = 5
hostname = socket.gethostname()
rpi = '\uf7bb'
piw, pih = font_awesome_brands.getsize(rpi)
hostw, hosth = font_dejavu.getsize(hostname)
texth = max(pih, hosth)
# draw a box around the text with 5 pixel padding
draw.rounded_rectangle([(x,y),(x+piw+hostw+12, y+texth+10)],
                       5, inky_display.RED, inky_display.BLACK, 2)
titlebb = y+texth+10
x += 5
y += 5 + (texth / 2)
draw.text((x, y+2), rpi, inky_display.WHITE, font_awesome_brands, 'lm')
x += piw + 3
draw.text((x,y), hostname, inky_display.WHITE, font_dejavu, 'lm')

if(getpass.getuser() == 'root'):
    os.system('umount /usbdisk.d')
    os.system('mount -o loop -t exfat /usbdisk.img /usbdisk.d')
    #print('remounted')

usage = shutil.disk_usage("/usbdisk.d")
font_dejavu = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)

labels = 'Used\nFree\nTotal'
lw,lh = draw.multiline_textsize(
            text = labels, 
            font = font_dejavu, 
            spacing = 2)

values = (f'{format_bytes(usage.used)}\n'+
          f'{format_bytes(usage.free)}\n'+
          f'{format_bytes(usage.total)}')

vw,vh = draw.multiline_textsize(
            text = values, 
            font = font_dejavu, 
            spacing = 2)
 
tx = inky_display.WIDTH - (lw + vw+ 5) - 10 # border, text width, box padding 
ty = 10
draw.rounded_rectangle(
        xy = [(tx-5,ty-5),(inky_display.WIDTH-1, ty + lh + 10)],
        fill = inky_display.RED,
        outline = inky_display.BLACK,
        width = 2,
        radius = 5)
draw.multiline_text(xy = (tx,ty-1), 
                    text = labels, 
                    fill = inky_display.WHITE, 
                    font = font_dejavu,
                    align = 'left')
draw.multiline_text(xy = (inky_display.WIDTH - 4 - vw,ty-1), 
                    text = values, 
                    fill = inky_display.WHITE, 
                    font = font_dejavu,
                    align = 'right')

# find the biggest box for the pie chart
usageSize = min( 
             inky_display.WIDTH - tx,
             inky_display.HEIGHT - (ty + lh + 10)) - 10
chartx = (inky_display.WIDTH + tx - usageSize) / 2
charty = inky_display.HEIGHT - usageSize - 5
draw.ellipse(xy =  [(chartx, charty), (chartx+usageSize, charty+usageSize)],
             outline = inky_display.BLACK, 
             fill = inky_display.WHITE, 
             width = 2)

draw.pieslice(xy = [(chartx, charty), (chartx+usageSize, charty+usageSize)],
             fill = inky_display.RED, 
             width = 2,
             start = 0,
             end = (usage.used/usage.total) * 360)

y = titlebb + 10
font_dejavu = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
net = ifcfg.interfaces() 

# this is a dictionary. I want wlan0 and usb0, 
# but want to check if present first

if('wlan0' in net and 'inet' in net['wlan0'] 
          and net['wlan0']['inet'] is not None): 
    font_awesome_solid = ImageFont.truetype('./Font Awesome 6 Free-Solid-900.otf', 16)
    w, h = font_awesome_solid.getsize('\uf1eb')
    draw.text((5, y), '\uf1eb', inky_display.RED, font_awesome_solid)
    draw.text((w + 10, y), net['wlan0']['inet'], inky_display.BLACK, font_dejavu)
    y += h + 3

if('usb0' in net and 'inet' in net['usb0'] 
         and net['usb0']['inet'] is not None): 
    font_awesome_brands = ImageFont.truetype('./Font Awesome 6 Brands-Regular-400.otf', 16)
    w, h = font_awesome_brands.getsize('\uf287')
    draw.text((5, y), '\uf287', inky_display.RED, font_awesome_brands)
    draw.text((w + 10, y), net['usb0']['inet'], inky_display.BLACK, font_dejavu)
    y += h + 3

y += 5
font_dejavu = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
def draw_text(xy, text, color, font):
    w,h = font.getsize(text)
    draw.text(xy, text, color, font)
    return (w, h)
for user in psutil.users():
    y += 2
    x = 5
    hMax = 0
    w, h = draw_text((x, y), '[', inky_display.RED, font_dejavu)
    x += w
    hMax = max(hMax, h)
    w, h = draw_text((x, y), user.name, inky_display.BLACK, font_dejavu)
    x += w
    hMax = max(hMax, h)
    w, h = draw_text((x, y), '@', inky_display.RED, font_dejavu)
    x += w
    hMax = max(hMax, h)
    host = user.terminal[:3] if user.host == '' else user.host
    w, h = draw_text((x, y), host, inky_display.BLACK, font_dejavu)
    x += w
    hMax = max(hMax, h)
    w, h = draw_text((x, y), ']', inky_display.RED, font_dejavu)
    hMax = max(hMax, h)
    y += hMax    


inky_display.set_image(img)
inky_display.show()
