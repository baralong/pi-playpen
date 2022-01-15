#!/usr/bin/python3
# requires sudo pip3 install rpi_ws281x
# contrary to documentation power via 3.3V so you shouldn't need a logic level converter
from rpi_ws281x import PixelStrip, Color
import time

LEDCOUNT = 5       # Number of LEDs
GPIOPIN = 18
FREQ = 800000
DMA = 5
INVERT = False       # Invert required when using inverting buffer and we aren't
BRIGHTNESS = 100

rainbow = [
	Color(255,0,0),   # red
	Color(255,127,0), # orange
	Color(255,255,0), # yellow
	Color(0,255,0),   # green
	Color(0,0,255),   # blue
	Color(75,0,130),  # indigo
	Color(143,0,255)  # violet
	]
strip = PixelStrip(LEDCOUNT, GPIOPIN, FREQ, DMA, INVERT, BRIGHTNESS) # Intialize the library (must be called once before other functions).

strip.begin()
while True:
    for index in range(len(rainbow)+LEDCOUNT):
        for pixel in range(LEDCOUNT):
            color = index - pixel
            if (color < 0 or color >= len(rainbow)): strip.setPixelColor(pixel, Color(0,0,0))
            else: strip.setPixelColor(pixel, rainbow[color])
        strip.show()
        time.sleep(0.5)

