import time

import schedule
from icalendar import Calendar

import calendar_helper
import motor

calendars: list[Calendar | None] = [None, None, None]


def refresh_calendars():
    for i in range(3):
        calendars[i] = calendar_helper.load_calendar(i)


if __name__ == '__main__':
    refresh_calendars()
    motor.reset_motors()

    schedule.every(10).minutes.do(refresh_calendars)

    while True:
        schedule.run_pending()
        time.sleep(1)
