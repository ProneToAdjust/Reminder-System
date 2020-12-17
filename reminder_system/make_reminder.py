import datetime
from . import utils

def make_reminder(upcoming_events = [], unconfirmed_events = []):
    """ Collates the upcoming events list and unconfirmed events list
    and returns the result as a readable string

    Returns:
        str: a readable version of the alert and unconfirmed event lists
    """		
    reminder_string = ''

    if upcoming_events or unconfirmed_events:
        if upcoming_events:
            reminder_string = 'You have.\n'

            for event in upcoming_events:
                event_alert = make_event_alert(event)

                reminder_string += f'{event_alert}\n'

        if unconfirmed_events:
            reminder_string += 'For unconfirmed events, you have.\n'

            for event in unconfirmed_events:
                event_alert = make_event_alert(event)

                reminder_string += f'{event_alert}\n'

        reminder_string += 'Please confirm.\n'

    return reminder_string

def make_event_alert(event):
    """Creates and returns a readable event alert from the inputted event 
    containing the event summary and time remaining to the event.

    Args:
        event {dict}: an single event from the event list returned from google_calendar's GoogleCalendar class method get_events

    Returns:
        str: a readable event alert for the inputted event
    """		
    event_alert = ''
    summary = event['summary']
    
    # get the minuetes remaining to the start of the event
    mins_remaining = utils.get_mins_between_now_and_event(event)

    # check if the event has been missed
    if mins_remaining < 0:
        event_alert = f'{summary} passed by {abs(mins_remaining)} minutes.'

    else:
        event_alert = f'{summary} in {mins_remaining} minutes.'

    return event_alert

if __name__ == "__main__":
    mock_event = [{'created': '2020-07-20T13:56:32.000Z',
            'end': {'dateTime': '2020-07-20T22:56:31+08:00', 'timeZone': 'Asia/Singapore'},
            'reminders': {'overrides': [{'method': 'popup', 'minutes': 60}],
                        'useDefault': False},
            'sequence': 0,
            'start': {'dateTime': '2020-07-20T22:56:31+08:00',
                    'timeZone': 'Asia/Singapore'},
            'status': 'confirmed',
            'summary': 'test event',
            'updated': '2020-07-20T13:56:32.984Z'}]
    print(make_reminder(mock_event))
    pass