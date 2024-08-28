import imrt_robot_serial
import imrt_xbox
import time

# Initialiser robottilkobling
robot = imrt_robot_serial.IMRTRobotSerial()
robot.connect()

# Initialiser Xbox-kontrolleren
controller = imrt_xbox.IMRTxbox()

# Sett standard hastighet
speed = 0.5

try:
    while True:
        # Oppdater kontrollerens tilstand
        #controller.update()
        
        # Hent input fra kontrolleren for å justere hastigheten
        if controller.A():  # Øk hastigheten med A-knappen
            speed += 0.1
        if controller.B():  # Senk hastigheten med B-knappen
            speed -= 0.1
        
        # Begrens hastigheten til mellom 0 og 1
        speed = max(0, min(speed, 1))

        # Hent input fra joystick for å styre roboten
        left_stick_x = controller.leftX()
        left_stick_y = controller.leftY()

        # Beregn hastighetskomponentene basert på joystickens posisjon
        motor_speed_left = speed * (left_stick_y + left_stick_x)
        motor_speed_right = speed * (left_stick_y - left_stick_x)

        # Send kommandoer til roboten
        robot.set_left_motor_speed(motor_speed_left)
        robot.set_right_motor_speed(motor_speed_right)

        # Legg til en liten forsinkelse for å unngå for mange oppdateringer
        time.sleep(0.1)

except KeyboardInterrupt:
    # Stopp roboten når programmet avsluttes
    robot.set_left_motor_speed(0)
    robot.set_right_motor_speed(0)
    robot.disconnect()
    print("Programmet er avsluttet.")