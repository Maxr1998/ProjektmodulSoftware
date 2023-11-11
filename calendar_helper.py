import os
from datetime import datetime

from dateutil.rrule import rrulestr
from dateutil.tz import tzlocal
from icalendar import Calendar


class Event:
    def __init__(self, start: datetime, end: datetime, summary: str, location: str):
        self.start = start
        self.end = end
        self.summary = summary
        self.location = location


def get_time() -> datetime:
    """
    Returns the current time. Used for mocking.
    """
    return datetime.now(tz=tzlocal())


def load_calendar(user_num: int) -> Calendar | None:
    """
    Loads a calendar from disk.
    """
    filename = f'{user_num + 1}.ics'
    if not os.path.exists(filename):
        return None

    with open(filename, 'rb') as f:
        calendar_content = f.read()

    return Calendar.from_ical(calendar_content)


def get_current_events(calendar: Calendar) -> list[Event]:
    """
    Returns the current event for the given user.
    """
    current_events: list[Event] = []
    for calendar_event in calendar.walk(name='VEVENT'):
        start = calendar_event['DTSTART'].dt
        end = calendar_event['DTEND'].dt

        # Handle all-day events by converting the date objects to datetime
        if not isinstance(start, datetime):
            start = datetime.combine(start, datetime.min.time(), tzinfo=tzlocal())
        if not isinstance(end, datetime):
            end = datetime.combine(end, datetime.min.time(), tzinfo=tzlocal())

        # Stack of event times to check
        stack = [(start, end)]

        # Handle recurring events
        if 'RRULE' in calendar_event:
            rrule_str = calendar_event['RRULE'].to_ical().decode('utf-8')
            rrule = rrulestr(rrule_str, dtstart=start)
            duration = end - start
            for recurrence in rrule:
                stack.append((recurrence, recurrence + duration))

        # Check for current events in stack
        for start, end in stack:
            if start <= get_time() <= end:
                event = Event(start, end, calendar_event.get('SUMMARY', ''), calendar_event.get('LOCATION'))
                print(f'Found current event "{event.summary} from {event.start} to {event.end}"')
                current_events.append(event)

    return current_events
