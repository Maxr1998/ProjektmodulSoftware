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

from zoneinfo import ZoneInfo

TZ = ZoneInfo('Europe/Berlin')  # hardcoded because otherwise things would get ugly

USER_COUNT = 3

MOTOR_PINS = [
    [9, 11, 8, 7],
    [16, 19, 20, 21],
    [5, 6, 12, 13],
]

SENSOR_PINS = [4, 18, 17]

STEPS_PER_REVOLUTION = 512

LOCATION_POSITIONS = {
    'home': 0,
    'work': STEPS_PER_REVOLUTION // 6,
    'lecture': STEPS_PER_REVOLUTION // 3,
    'meeting': STEPS_PER_REVOLUTION // 2,
    'conference': STEPS_PER_REVOLUTION // 3 * 2,
    'vacation': STEPS_PER_REVOLUTION // 6 * 5,
}
