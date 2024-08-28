# Example code for IMRT100 robot project

import imrt_robot_serial
import signal
import time
import sys
import random

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 200
TURNING_SPEED = 100  # Justerbar for bedre sving
STOP_MAIN = 35
STOP_SIDE = 30
SWING_FULL = 45

stuck_timer, stuck_treshold = 0, 2

retning = random.randint(1,2)
def stop_robot(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)

def drive_robot(direction, duration):
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)

def right_turn(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(int(DRIVING_SPEED * 0.4), DRIVING_SPEED)  # Forbedret sving
        time.sleep(0.10)

def full_right(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED, -TURNING_SPEED)
        time.sleep(0.10)

def left_turn(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(DRIVING_SPEED, int(DRIVING_SPEED * 0.4))  # Forbedret sving
        time.sleep(0.10)

def full_left(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(-TURNING_SPEED, TURNING_SPEED)
        time.sleep(0.10)

def turn_around(duration):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED, -TURNING_SPEED)
        time.sleep(0.10)

# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds

# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()

# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

# Start serial receive thread
motor_serial.run()

print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now:

    # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()
    print("Front:", dist_1, "RIGHT:", dist_3, "LEFT:", dist_4)


##    # Kontrolllogikk for å bestemme robotens bevegelser
    if dist_1 < STOP_MAIN:
        if dist_3 < STOP_SIDE:
            stop_robot (0.1)  # Øk varigheten for bedre sving
            drive_robot (BACKWARDS, .15)
            full_left (0.3)
        elif dist_4 < STOP_SIDE:
            stop_robot (0.15)
            drive_robot (BACKWARDS, 0.15)
            full_right(0.3)  # Øk varigheten for bedre sving
            
        else:
            full_right (4)
    elif dist_3 < SWING_FULL and dist_4 < SWING_FULL:
        if dist_3 < SWING_FULL:
            right_turn(0.25)
        elif dist_4 < SWING_FULL:
            left_turn(0.2)
    else:
        drive_robot(FORWARDS, 0.1)

print("Goodbye")
