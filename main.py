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

import time

import schedule
from icalendar import Calendar

import calendar_helper
import motor
from calendar_helper import Event
from config import USER_COUNT, LOCATION_POSITIONS
from user_configuration import UserConfiguration, LocationKeywords

configurations: list[UserConfiguration | None] = [None, None, None]
calendars: list[Calendar | None] = [None, None, None]


def refresh_configurations():
    for i in range(USER_COUNT):
        configurations[i] = UserConfiguration.load_configuration(i)


def refresh_calendars():
    for i in range(USER_COUNT):
        calendars[i] = calendar_helper.load_calendar(i)


def calculate_location(configuration: UserConfiguration, events: list[Event]) -> str:
    locations = list(filter(None, map(lambda event: configuration.map_location(event), events)))
    locations = sorted(locations, key=LocationKeywords.priority, reverse=True)  # sort locations by priority

    # Return the highest priority location if available, otherwise fall back to location based on working hours
    return locations[0] if locations else configuration.calculate_fallback_location()


def update_locations():
    for i in range(USER_COUNT):
        configuration = configurations[i]
        calendar = calendars[i]
        if not configuration or not calendar:
            continue
        current_events = calendar_helper.get_current_events(calendar)
        location = calculate_location(configuration, current_events)
        print(f'User {i + 1} is currently at {location}')

        # Update motor position
        motor.motor_go_to_position(i, LOCATION_POSITIONS[location])


def main():
    refresh_configurations()
    refresh_calendars()
    motor.reset_motors()
    update_locations()

    schedule.every(10).minutes.do(refresh_calendars)
    schedule.every(1).minute.do(update_locations)

    while True:
        schedule.run_pending()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
