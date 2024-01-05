#test
#moretest
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

while True:
    events = pygame.event.get()
    button_state = []
    axis_state = []
    for button in range(joystick.get_numbuttons()):
        button_state.append(joystick.get_button(button))
    
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

    print(str([motorLeft, motorRight]))
    
    # ser.write(str([motorLeft, motorRight]).encode())     # write a string

    
# try:
#     while True:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.JOYBUTTONDOWN:
#                 print("Button Pressed")
#                 if joystick.get_button(6):
#                     # Control Left Motor using L2
#                     print('L2 pressed')
#                 elif joystick.get_button(7):
#                     # Control Right Motor using R2
#                     print('R2 pressed')
#             elif event.type == pygame.JOYBUTTONUP:
#                 print("Button Released")

# except KeyboardInterrupt:
#     print("EXITING NOW")
#     joystick.quit()