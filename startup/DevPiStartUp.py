#!/usr/bin/env python
# startup service for the devpi with the buttonshim and the LED shim
from contextlib import nullcontext
import signal
import buttonshim
from enum import Enum
import ledshim
import time
import subprocess

allButtons = [buttonshim.BUTTON_A, buttonshim.BUTTON_B, buttonshim.BUTTON_C, buttonshim.BUTTON_D, buttonshim.BUTTON_E]
class ButtonState(Enum):
    # really a "pressed" event should be triggered on release
    # then we could have another state for waiting.
    # the state machine is:
    #   unpressed
    #       => press
    #           => release => trigger "tapped" => unpressed
    #           => hold => trigger "held"
    #               => release => unpressed
    UNPRESSED = 0
    PRESSED = 1
    HELD = 2
    RELEASED = 3

class Button:
    state = ButtonState.UNPRESSED
    def press(self):
        self.state = ButtonState.PRESSED
    def hold(self):
        self.state = ButtonState.HELD
    def release(self):
        self.state = ButtonState.RELEASED
    def reset(self):
        self.state = ButtonState.RELEASED

tmp = Button()
states = [Button(), Button(), Button(), Button(), Button() ]
@buttonshim.on_press(allButtons)
def handle_button(button, state): # the state parameter is so you can reuse the same handler for press and release
    global states
    global tmp
    states[button].press()
    print("PRESS: Button {} ({}) is {}".format(button, buttonshim.NAMES[button], state))

@buttonshim.on_hold(allButtons)
def handle_hold(button):
    global states
    states[button].hold()
    # this is where we call the state handler
    print("HOLD: Button {} ({})".format(button, buttonshim.NAMES[button]))

@buttonshim.on_release(allButtons)
def handle_release(button, state):
    global states
    if states[button].state == ButtonState.PRESSED:
        # this is where we call the state handler, just before the press finishes....hmm
        a = 1
    states[button].release()
    print("RELEASE: Button {} ({}) is {}".format(button, buttonshim.NAMES[button], state))


# not happy with this I think newing up an iterator might be the go, but I 
# want to be able to break out... it's important to know when to confinue
# or  start again
class handler:
    # does the current state match this handler
    def match(self, state):
        return False
    # do the thing, return True if you have more to do 
    def do(self):
        pass
    def done(self):
        return True

class start_handler(handler):
    count = 0
    def match(self, state):
        return self.count == 0
    def do(self):
        self.count += 1
        return self.count < 100

class rainbow_handler(handler):
    pass



handlers = [
    start_handler(),
    rainbow_handler()
]



currentHandler = handler()
while True:
    for handler in handlers:
        if handler.match(states):
            currentHandler = handler
            break
    if not currentHandler.done():
        currentHandler.do()
    time.sleep(0.01)
