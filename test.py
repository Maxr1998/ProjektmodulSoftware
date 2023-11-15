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

from datetime import datetime, timedelta

import schedule

import calendar_helper
from config import TZ

current_time = datetime(2023, 11, 1, 5, 0, 0, tzinfo=TZ)


def mock_get_time():
    return current_time


def advance_time():
    global current_time
    delta = 15 if 7 <= current_time.hour <= 19 else 60
    current_time = current_time + timedelta(minutes=delta)
    print(f"Time advanced to {current_time}")


def test():
    # Patch calendar_helper.get_time
    calendar_helper.get_time = mock_get_time

    # Modify time on a given schedule
    schedule.every(1).second.do(advance_time)

    # Run original main function
    from main import main
    main()


if __name__ == '__main__':
    test()
