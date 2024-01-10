import threading

#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

import serial
import pygame
# ser = serial.Serial('COM4', 9600)

pygame.init()
joystick = pygame.joystick.Joystick(0)
# joystick.init()

# axis 0: left horizontal with right positive
# axis 1: left vertical with down positive
# axis 2: right horizontal with right positive
# axis 3: right vertical with down positive
# axis 4: left trigger with -1 unpressed and 1 fully pressed
# axis 5: right trigger with -1 unpressed and 1 fully pressed
# button 0: A
# button 1: B
# button 2: X
# button 3: Y
# button 4: LeftButton
# button 5: RightButton
# button 6: back
# button 7: start
# button 8: LeftStickPress
# button 9: RightStickPress

running = 1


def thread_input():
    global running
    input("Press enter to stop")
    running = 0

def thread_joystick():
    global button_state
    while running:
        pygame.init()
        joystick = pygame.joystick.Joystick(0)
        events = pygame.event.get()
        button_state = [0,0,0,0,0,0,0,0,0,0,0]
        button_state_temp = []
        axis_state = []
        for button in range(joystick.get_numbuttons()):
            button_state_temp.append(joystick.get_button(button))
        button_state=button_state_temp
        
        for axis in range(joystick.get_numaxes()):
            axis_state.append(joystick.get_axis(axis))
        
        leftStickHorizontal = axis_state[0]
        leftStickVertical = -axis_state[1]
        rightStickHorizontal = axis_state[2]
        rightStickVertical = -axis_state[3]
        state = [leftStickHorizontal,leftStickVertical,rightStickHorizontal,rightStickVertical,button_state[0]]
        # print(state)

        ## LOGIC FOR DIFFERENTIAL DRIVE
        motorLeft = leftStickVertical + leftStickHorizontal
        motorRight = leftStickVertical - leftStickHorizontal
        #normalize motors
        if motorRight > 1 or motorLeft > 1:
            motorLeft = motorLeft / max(motorLeft, motorRight)
            motorRight = motorRight / max(motorLeft, motorRight)

        # print(str([motorLeft, motorRight]))

        # ser.write(str([motorLeft, motorRight]).encode())     # write a string

def thread_eye_show():
    global button_state
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch28.LCD_1inch28()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    # disp.bl_DutyCycle(50)
    disp.bl_DutyCycle(100) #doesnt seem to affect anything
    im = Image.open('calm.gif')
    im.seek(1)

    while running:
        print(button_state)
        # button 0: A
        # button 1: B
        # button 2: X
        # button 3: Y
        if button_state[0] == 1:
            im = Image.open('sad.gif')
            im.seek(1)
            
        elif button_state[1] == 1:
            im = Image.open('angry.gif')
            im.seek(1)
        elif button_state[2] == 1:
            im = Image.open('calm.gif')
            im.seek(1)
        elif button_state[3] == 1:
            im = Image.open('scared.gif')
            im.seek(1)
        # else:
        # try:
        #     im.seek(im.tell() + 1)
        #     im_r=im.rotate(180)
        #     disp.ShowImage(im_r)
        #     time.sleep(0.01)
        #     # do something to im
        # except EOFError:
        #     pass  # end of sequence
        im.seek(im.tell() + 1)
        im_r=im.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(0.01)

        
if __name__ == "__main__":
    j = threading.Thread(target=thread_joystick)
    j.start()

    inp = threading.Thread(target=thread_input)
    inp.start()
    
    eye = threading.Thread(target=thread_eye_show)
    eye.start()