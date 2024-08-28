import imrt_robot_serial
import signal
import time
import sys
import random

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 150  # Redusert for bedre kontroll
TURNING_SPEED = 75  # Justert for bedre svinger
STOP_MAIN = 35      # Økt for tidligere svinger
STOP_SIDE = 60      # Økt for tidligere side-deteksjon
SWING_FULL = 55     # Økt for tidligere svinger

def stop_robot(duration):
    motor_serial.send_command(0, 0)
    time.sleep(duration)

def drive_robot(direction, duration):
    speed = DRIVING_SPEED * direction
    motor_serial.send_command(speed, speed)
    time.sleep(duration)

def right_turn(duration):
    motor_serial.send_command(int(DRIVING_SPEED * 0.4), DRIVING_SPEED)
    time.sleep(duration)

def full_right(duration):
    motor_serial.send_command(TURNING_SPEED, -TURNING_SPEED)
    time.sleep(duration)

def left_turn(duration):
    motor_serial.send_command(DRIVING_SPEED, int(DRIVING_SPEED * 0.4))
    time.sleep(duration)

def full_left(duration):
    motor_serial.send_command(-TURNING_SPEED, TURNING_SPEED)
    time.sleep(duration)

def turn_around():
    # Funksjon for å snu roboten 180 grader
    motor_serial.send_command(TURNING_SPEED, -TURNING_SPEED)
    time.sleep(1.0)  # Juster varigheten basert på behov

def is_stuck(dist_1, dist_3, dist_4):
    # Hvis roboten har hindringer både foran og på begge sider, er den sannsynligvis fast
    return dist_1 < STOP_MAIN and dist_3 < STOP_SIDE and dist_4 < STOP_SIDE

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
    print("Dist 1:", dist_1, "   Dist 2:", dist_2, "Dist 3:", dist_3, "Dist 4:", dist_4)

    # Kontrolllogikk for å bestemme robotens bevegelser
    if is_stuck(dist_1, dist_3, dist_4):
        stop_robot(0.1)
        turn_around()
    elif dist_1 < STOP_MAIN:
        if dist_3 < STOP_SIDE:
            stop_robot(0.1)
            drive_robot(BACKWARDS, 0.15)
            full_left(0.5)
        elif dist_4 < STOP_SIDE:
            stop_robot(0.1)
            drive_robot(BACKWARDS, 0.15)
            full_right(0.45)
        else:
            full_right(0.3)
    elif dist_3 < SWING_FULL:
        right_turn(0.25)
    elif dist_4 < SWING_FULL:
        left_turn(0.2)
    else:
        drive_robot(FORWARDS, 0.1)

print("Goodbye")
