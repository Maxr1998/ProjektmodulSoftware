# Copyright 2023 Max Rumpf
#
# This file is part of Weasley Clock.
#
# Weasley Clock is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this software.
# If not, see <https://www.gnu.org/licenses/>.

try:
    import RPi.GPIO as GPIO
    from RpiMotorLib import RpiMotorLib

    # Setup motors
    motors = RpiMotorLib.BYJMotor("Motors", "28BYJ")
    GPIO_IMPORTED = True
except RuntimeError:
    GPIO_IMPORTED = False

from config import MOTOR_PINS, SENSOR_PINS, STEPS_PER_REVOLUTION

motor_positions = [0, 0, 0]


def setup_sensor(sensor_num):
    """
    Sets up the sensor as an input with pull-up resistor, thus bringing the pin to LOW when the sensor is triggered.
    """
    GPIO.setup(SENSOR_PINS[sensor_num], GPIO.IN, pull_up_down=GPIO.PUD_UP)


def sensor_status(sensor_num):
    """
    Returns the status of the sensor.
    :return: True if the sensor is triggered, False otherwise.
    """
    return GPIO.input(SENSOR_PINS[sensor_num])


def motor_clockwise(motor_num, steps=STEPS_PER_REVOLUTION):
    """
    Moves the motor clockwise by the given number of steps.
    """
    if not GPIO_IMPORTED:
        print("GPIO not imported, skipping motor movement")
        return

    motors.motor_run(MOTOR_PINS[motor_num], wait=.001, steps=steps)
    motor_positions[motor_num] += steps
    motor_positions[motor_num] %= STEPS_PER_REVOLUTION


def reset_motors():
    """
    Resets all motors to their default position.
    """
    global motor_positions

    if not GPIO_IMPORTED:
        print("GPIO not imported, skipping motor reset")
        motor_positions = [0, 0, 0]
        return

    for motor_num in range(3):
        setup_sensor(motor_num)

        steps = 0
        while sensor_status(motor_num) and steps < STEPS_PER_REVOLUTION:
            motor_clockwise(motor_num=motor_num, steps=1)
            steps += 1

        if steps == STEPS_PER_REVOLUTION:  # one full revolution without finding the sensor
            raise Exception(f"Motor {motor_num} could not be reset to default position")

    print(f"All motors reset to default position")
    motor_positions = [0, 0, 0]


def motor_go_to_position(motor_num, target_position):
    """
    Moves the motor to the target position, always going clockwise.
    """
    if target_position < 0 or target_position >= STEPS_PER_REVOLUTION:
        raise ValueError(f"Invalid target position: {target_position}")

    current_position = motor_positions[motor_num]

    # No-op if already at target position
    if current_position == target_position:
        return

    print(f"Moving motor {motor_num} to position {target_position}")

    # Always go clockwise, even if the target position is behind the current position
    steps = (target_position - current_position) % STEPS_PER_REVOLUTION

    motor_clockwise(motor_num=motor_num, steps=steps)
    print(f"Motor {motor_num} moved to position {target_position}")
