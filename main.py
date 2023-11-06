import time

import schedule

import calendar_helper
import motor


def motors_clockwise():
    motor.motor_clockwise(motor_num=0, steps=256)
    motor.motor_clockwise(motor_num=1, steps=256)
    motor.motor_clockwise(motor_num=2, steps=256)


if __name__ == '__main__':
    calendar_helper.load_calendars()
    motor.reset_motors()

    schedule.every(10).minutes.do(calendar_helper.load_calendars)

    while True:
        schedule.run_pending()
        time.sleep(1)
