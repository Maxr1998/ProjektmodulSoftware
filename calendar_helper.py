import os
from datetime import date, datetime

from dateutil.tz import tzlocal
from icalendar import Calendar

_loaded_calendars = False
calendars: list[Calendar | None] = [None, None, None]


def get_time() -> datetime:
    """
    Returns the current time. Used for mocking.
    """
    return datetime.now(tz=tzlocal())


def load_calendars():
    """
    Loads all calendars from disk.
    """
    for i in range(3):
        filename = f'{i + 1}.ics'
        if not os.path.exists(filename):
            calendars[i] = None
            continue

        with open(filename, 'rb') as f:
            calendar_content = f.read()
        calendars[i] = Calendar().from_ical(calendar_content)


def get_current_event(user_num: int):
    """
    Returns the current event for the given user.
    """
    global _loaded_calendars
    if not _loaded_calendars:
        load_calendars()
        _loaded_calendars = True

    calendar = calendars[user_num]
    if calendar is None:
        print(f'No calendar found for user {user_num}')
        return None

    current_events = []
    for event in calendar.walk(name='VEVENT'):
        start = event['DTSTART'].dt
        end = event['DTEND'].dt

        # Handle all-day events by converting them to datetime objects
        if isinstance(start, date):
            start = datetime.combine(start, datetime.min.time(), tzinfo=tzlocal())
        if isinstance(end, date):
            end = datetime.combine(end, datetime.min.time(), tzinfo=tzlocal())

        if start <= get_time() <= end:
            current_events.append(event)

    for event in current_events:
        summary = event.get('SUMMARY', default='<untitled>')
        print(f'Found current event "{summary}"')

    return None
