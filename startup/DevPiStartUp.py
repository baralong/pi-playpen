#!/usr/bin/env python
# startup service for the devpi with the buttonshim and the LED shim
from contextlib import nullcontext
from datetime import datetime
from itertools import takewhile
import math
import signal
import threading
import buttonshim
from enum import Enum
import ledshim
import time
import subprocess

allButtons = [buttonshim.BUTTON_A, buttonshim.BUTTON_B, buttonshim.BUTTON_C, buttonshim.BUTTON_D, buttonshim.BUTTON_E]
class ButtonState(Enum):
    # really a "pressed" event should be triggered on release
    UNPRESSED = 0
    PRESSED = 1 # triggered on release IIF on_hold wasn't triggered 
    HELD = 2

buttonStates = [ButtonState.UNPRESSED] * 5
ledLock = threading.Lock()

ledshim.clear()
ledshim.show()

@buttonshim.on_press(allButtons)
def handle_press(button, state):
    global ledLock
    exit_time = time.perf_counter() + 0.3 
    with ledLock:
        step = 0
        button_pixel = ledshim.width - 3 - round(button * 3.75)
        pixels = range(button_pixel - 3, button_pixel)
        while time.perf_counter() < exit_time:
            ledshim.set_multiple_pixels(pixels, (255,0,0))
            ledshim.show()
            time.sleep(0.05)
            ledshim.clear()
            ledshim.show()
            time.sleep(0.05)

@buttonshim.on_hold(allButtons, hold_time = 1)
def handle_hold(button):
    global buttonStates
    buttonStates[button] = ButtonState.HELD

@buttonshim.on_release(allButtons)
def handle_release(button, state):
    global buttonStates
    if buttonStates[button] == ButtonState.HELD:
        buttonStates[button] = ButtonState.UNPRESSED
    else:
        buttonStates[button] = ButtonState.PRESSED


# class handler:
#     # does the current state match this handler
#     def match(self, state):
#         return False
#     def launch(self):
#         pass

# class start_handler(handler):
#     count = 0
#     def match(self, state):
#         return self.count == 0
#     def __iter__(self):
#         return self
#     def __next__(self):
#         raise StopIteration

# class rainbow_handler(handler):
#     pass



# handlers = [
#     start_handler(),
#     rainbow_handler(),
#     handler()
# ]

signal.pause()
