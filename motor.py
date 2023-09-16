from RpiMotorLib import RpiMotorLib
from config import MOTOR_PINS

# Setup motor
motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")


def motor_clockwise(motor_num, steps=512):
    motor.motor_run(MOTOR_PINS[motor_num], wait=.001, steps=steps)
