import pygame

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Get count of joysticks
joystick_count = pygame.joystick.get_count()

if joystick_count > 0:
    # Use the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Get inputs from the joystick

ch2 = 0
ch3 = 0
def getjoystick():
    global ch2,ch3
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Axis motion is JOYAXISMOTION
            axis = event.axis
            value = joystick.get_axis(axis)
            if axis == 2:
                ch2 = value
            elif axis == 3:
                ch3 = value
            #print(f"Axis {axis} value: {value}")
        elif event.type == pygame.JOYBUTTONDOWN:
            # Button press is JOYBUTTONDOWN
            button = event.button
            #print(f"Button {button} pressed")
    return ch2,ch3