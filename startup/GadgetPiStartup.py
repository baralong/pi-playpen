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


# draw a box around the text with 5 pixel padding
draw.rounded_rectangle([(5,y-5),(w+10, y+h+5)],
                       5, inky_display.RED, inky_display.BLACK, 2)
draw.text((10, y), hostname, inky_display.WHITE, font)
y += h + 15

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
    #print('remounted')

usage = shutil.disk_usage("/usbdisk.d")
font = ImageFont.truetype(vga_font, 16)

labels = 'Used\nFree\nTotal'
lw,lh = draw.multiline_textsize(
            text = labels, 
            font = font, 
            spacing = 2)

values = (f'{format_bytes(usage.used)}\n'+
          f'{format_bytes(usage.free)}\n'+
          f'{format_bytes(usage.total)}')

vw,vh = draw.multiline_textsize(
            text = values, 
            font = font, 
            spacing = 2)
 
bx = inky_display.WIDTH - 3 - (lw + vw+ 5) - 10 # border, text width, box padding 
by = inky_display.HEIGHT - 3 - lh - 10 #border, text height, box padding
draw.rounded_rectangle(
        xy = [(bx,by),(inky_display.WIDTH-1, inky_display.HEIGHT-1)],
        fill = inky_display.RED,
        outline = inky_display.BLACK,
        width = 1,
        radius = 5)
tx = bx + 6
ty = by + 4
draw.multiline_text(xy = (tx,ty), 
                    text = labels, 
                    fill = inky_display.WHITE, 
                    font = font,
                    align = 'left')
draw.multiline_text(xy = (inky_display.WIDTH - 4 - vw,ty), 
                    text = values, 
                    fill = inky_display.WHITE, 
                    font = font,
                    align = 'right')

# find the biggest box for the pie chart
bw = inky_display.WIDTH - bx
usageSize = min(bw - 5,by - 6) 
chartx = bx + (0.5*(bw - usageSize)) + 2
draw.ellipse(xy =  [(chartx, 2), (chartx+usageSize, usageSize + 2)],
             outline = inky_display.BLACK, 
             fill = inky_display.WHITE, 
             width = 2)

draw.pieslice(xy = [(chartx, 2), (chartx+usageSize, usageSize + 2)],
             fill = inky_display.RED, 
             width = 2,
             start = 0,
             end = (usage.used/usage.total) * 360)

inky_display.set_image(img)
inky_display.show()
