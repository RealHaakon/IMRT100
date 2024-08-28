import imrt_robot_serial
import signal
import time
import sys

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 150  # Hastighet for å kjøre fremover
TURNING_SPEED = 75  # Hastighet for å svinge
DESIRED_DISTANCE = 30  # Ønsket avstand fra veggen i cm
STOP_MAIN = 35  # Terskel for å stoppe hvis noe er rett foran
STOP_SIDE = 15  # Terskel for å unngå hindringer på sidene

def stop_robot(duration):
    motor_serial.send_command(0, 0)
    time.sleep(duration)

def drive_robot(direction, duration):
    speed = DRIVING_SPEED * direction
    motor_serial.send_command(speed, speed)
    time.sleep(duration)

def right_turn(duration):
    motor_serial.send_command(-TURNING_SPEED, TURNING_SPEED)
    time.sleep(duration)

def left_turn(duration):
    motor_serial.send_command(TURNING_SPEED, -TURNING_SPEED)
    time.sleep(duration)

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

    # Hent avstandsmålinger fra sensorer
    dist_front = motor_serial.get_dist_1()
    dist_left = motor_serial.get_dist_4()
    dist_right = motor_serial.get_dist_3()

    print("Dist 1:", dist_front, "   Dist 2:", dist_left, "Dist 3:", dist_right)

    # Hvis noe er rett foran, stopp og sving til høyre
    if dist_front < STOP_MAIN:
        stop_robot(0.1)
        right_turn(0.1)

    # Hvis roboten er for langt fra venstre vegg, sving til venstre
    elif dist_left < STOP_SIDE:
        right_turn(0.3)

    # Hvis roboten er for nær venstre vegg, sving til høyre
    elif dist_left > DESIRED_DISTANCE:
        left_turn(0.3)

    # Hvis ingenting er i veien, kjør rett frem
    else:
        drive_robot(FORWARDS, 0.1)

print("Goodbye")
