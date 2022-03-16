#!/usr/bin/env python

#basically working, but arming etc should happen on release
import signal
import buttonshim
import time
import subprocess

button_state = "waiting"
show_pixel = 0
heldD = False
heldE = False

@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=2)
def arm(button):
    global button_state
    global heldE
    heldE = True
    print (f"E Hold {button_state}")
    if button_state == "armed": 
        button_state = "waiting"
        return
    button_state = "armed"
    for i in range(12):
        buttonshim.set_pixel(0xFF * (not i%2), 0xFF * (i%2), 0xFF * (i%2))
        time.sleep(0.5)
        if button_state != "armed": break

    button_state = "waiting"
    print("disarmed")
    buttonshim.set_pixel(0x00, 0x00, 0x00)

@buttonshim.on_release(buttonshim.BUTTON_E)
def reboot(button, pressed):
    global button_state
    global heldE
    print (f"E Release {button_state} held {heldE}")
    if heldE or button_state != "armed": 
        heldE = False
        return
    button_state = "waiting"
    buttonshim.set_pixel(0x00, 0xFF, 0x00)
    print("rebooting")
    time.sleep(0.2)
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)

@buttonshim.on_hold(buttonshim.BUTTON_D, hold_time=2)
def d_disarm(button):
    global button_state
    global heldD
    heldD = True
    print (f"D Hold {button_state}")
    if button_state == "armed": 
        button_state = "waiting"
 
@buttonshim.on_release(buttonshim.BUTTON_D)
def shutdown(button, pressed):
    global button_state
    global heldD
    print (f"D Release {button_state} held {heldD}")
    if heldD or button_state != "armed": 
        heldD = False
        return
    button_state = "waiting"
    buttonshim.set_pixel(0x00, 0x00, 0xFF)
    time.sleep(0.2)
    command = "/usr/bin/sudo /sbin/shutdown now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)
    

signal.pause()