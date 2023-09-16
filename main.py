import time

import requests
import schedule
from icalendar import Calendar

import motor

CAL_URL = 'https://calendar.google.com/calendar/ical/max.rumpf1998%40gmail.com/' \
          'private-e8e7fc0a4b4f88e6e2829f65b441347a/basic.ics'


def sync_calendar():
    resp = requests.get(CAL_URL)
    with open('calendar.ics', 'wb') as f:
        f.write(resp.content)


def job():
    try:
        calendar_content = open('calendar.ics', 'rb').read()
    except FileNotFoundError:
        # Calendar not synced yet
        return

    calendar = Calendar()
    print(calendar.from_ical(calendar_content, multiple=True))
    # print(calendar.to_ical().decode("utf-8").replace('\r\n', '\n').strip())


def motors_clockwise():
    motor.motor_clockwise(motor_num=1, steps=512)
    motor.motor_clockwise(motor_num=2, steps=512)


if __name__ == '__main__':

    sync_calendar()
    schedule.every(5).minutes.do(sync_calendar)
    schedule.every(5).seconds.do(motors_clockwise)
    while True:
        schedule.run_pending()
        time.sleep(1)
