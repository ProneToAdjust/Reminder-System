import datetime

def get_mins_between_now_and_event(event):
    """Returns the minutes between the current time and the start time of the inputted event

    Args:
        event (dict): an single event from the event list returned from google_calendar's GoogleCalendar class method get_events

    Returns:
        int: minutes between the current time and the start time of the inputted event
    """
    time_difference_timedelta = get_timedelta_between_now_and_event(event)
    time_difference_mins = convert_timedelta_to_mins(time_difference_timedelta)

    return time_difference_mins

def get_timedelta_between_now_and_event(event):
    """Returns the time difference between the current time and the start time of the event

    Arguments:
        event {dict} -- an single event from the event list returned from google_calendar's GoogleCalendar class method get_events

    Returns:
        datetime.timedelta -- the time difference between the event's start time and the current time
    """

    # seperate the date and time from the event's start dateTime
    date, time = event['start']['dateTime'].split('T')

    # remove the time zone offset
    time = time.split('+')

    # convert and combine the date and time to a datetime object
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
    time_object = datetime.datetime.strptime(time[0], '%H:%M:%S')
    datetime_object = datetime.datetime.combine(date_object, time_object.time())

    # get the time difference between the event's datetime object and now
    datetime_now = datetime.datetime.now()
    time_difference = datetime_object - datetime_now

    return time_difference

def convert_timedelta_to_mins(timedelta):
    """Calculates and returns the minuetes from the inputted timedelta

    Args:
        timedelta (datetime.timedelta): the timedelta to calculate the minuetes from

    Returns:
        int: the minuetes calculated from the inputted timedelta
    """		
    return int(round(timedelta.total_seconds() / 60))

if __name__ == "__main__":
    mock_event = {'created': '2020-07-20T13:56:32.000Z',
            'end': {'dateTime': '2020-07-20T22:56:31+08:00', 'timeZone': 'Asia/Singapore'},
            'reminders': {'overrides': [{'method': 'popup', 'minutes': 60}],
                        'useDefault': False},
            'sequence': 0,
            'start': {'dateTime': '2020-07-20T22:56:31+08:00',
                    'timeZone': 'Asia/Singapore'},
            'status': 'confirmed',
            'summary': 'test event',
            'updated': '2020-07-20T13:56:32.984Z'}

    print(get_mins_between_now_and_event(mock_event))
    print(get_timedelta_between_now_and_event(mock_event))

    timedelta = datetime.timedelta(seconds = 60)
    print(convert_timedelta_to_mins(timedelta))
    pass