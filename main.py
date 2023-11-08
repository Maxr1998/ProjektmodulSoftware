import time

import schedule
from icalendar import Calendar

import calendar_helper
from config import USER_COUNT
import motor
from user_configuration import UserConfiguration

configurations: list[UserConfiguration | None] = [None, None, None]
calendars: list[Calendar | None] = [None, None, None]


def refresh_configurations():
    for i in range(USER_COUNT):
        configurations[i] = UserConfiguration.load_configuration(i)


def refresh_calendars():
    for i in range(USER_COUNT):
        calendars[i] = calendar_helper.load_calendar(i)


if __name__ == '__main__':
    refresh_configurations()
    refresh_calendars()
    motor.reset_motors()

    schedule.every(10).minutes.do(refresh_calendars)

    while True:
        schedule.run_pending()
        time.sleep(1)
