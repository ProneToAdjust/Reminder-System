import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

from .print_logger import log

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendar:

    def __init__(self, service_account_file):
        self.service_account_file = service_account_file

        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=SCOPES)

        self.service = build('calendar', 'v3', credentials=self.credentials)
        log("service build completed")

    def add_event(
        self,
        summary,
        start_date,
        end_date,
        start_time,
        end_time,
        gmt_off='+08:00',
        timezone='Asia/Singapore',
        recur_freq=None,
        recur_until=None,
        reminder_min=None
    ):

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_date + 'T' + start_time + gmt_off,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_date + 'T' + end_time + gmt_off,
                'timeZone': timezone,
            },
        }

        if recur_freq and recur_until:
            if recur_until:
                event['recurrence'] = [
                    'RRULE:FREQ=' + recur_freq + ';UNTIL=' + recur_until
                ]

                log("Recurrance added")

            else:
                log("recur_until parameter is required")

        else:
            log("No reccurance")

        if reminder_min:
            event['reminders'] = {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': reminder_min}
                ],
            }

        else:
            event['reminders'] = {
                'useDefault': True
            }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        log('Event created:\nstart: {}\nend: {}'.format(
            event['start'], event['end']))

    def get_events(self):

        # Call the GoogleCalendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        log('Getting events')
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime',
            timeZone='GMT+8:00'
        ).execute()
        events = events_result.get('items')

        if not events:
            log('No upcoming events found.')

        return events


if __name__ == '__main__':
    # Create an event that starts and ends 60 mins after the current time
    # Reminder time is set to 60 mins
    now_datetime = datetime.datetime.now()
    one_hour_from_now = now_datetime + datetime.timedelta(minutes=60)

    event_date = one_hour_from_now.strftime("%Y-%m-%d")
    event_time = one_hour_from_now.strftime("%H:%M:%S")

    calendar = GoogleCalendar(service_account_file='credentials.json')
    calendar.add_event(
        summary='test event',
        start_date=event_date,
        end_date=event_date,
        start_time=event_time,
        end_time=event_time,
        # recur_freq = 'DAILY',
        # recur_until ='20190505T000000Z',
        reminder_min=60
    )
    events = calendar.get_events()
