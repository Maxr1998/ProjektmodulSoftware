from RpiMotorLib import RpiMotorLib
from config import MOTOR_PINS, SENSOR_PINS
import RPi.GPIO as GPIO

# Setup motor
motors = RpiMotorLib.BYJMotor("Motors", "28BYJ")


def motor_clockwise(motor_num, steps=512):
    motors.motor_run(MOTOR_PINS[motor_num], wait=.001, steps=steps)


def reset_motors():
    for motor_num in range(3):
        GPIO.setup(SENSOR_PINS[motor_num], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        steps = 0
        while GPIO.input(SENSOR_PINS[motor_num]) and steps < 512:
            motor_clockwise(motor_num=motor_num, steps=1)
            steps += 1

        if steps == 512:  # one full revolution without finding the sensor
            raise Exception(f"Motor {motor_num} could not be reset to default position")

    print(f"All motors reset to default position")
