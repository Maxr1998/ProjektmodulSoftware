from datetime import datetime, timedelta

import schedule

import calendar_helper
from config import TZ

current_time = datetime(2023, 10, 18, 8, 0, 0, tzinfo=TZ)


def mock_get_time():
    return current_time


def advance_time():
    global current_time
    delta = 15 if 8 <= current_time.hour < 19 else 60
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
