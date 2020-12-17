from .google_calendar import GoogleCalendar
import datetime
from . import utils

class EventManager(GoogleCalendar):
	def __init__(self, service_account_file):
		super().__init__(service_account_file)

		self.upcoming_events = []
		self.unconfirmed_events = []
		self.confirmed_events = []

	def get_events_to_be_reminded(self):
		upcoming_events = self.check_for_upcoming_events()
		unconfirmed_events = self.unconfirmed_events

		return upcoming_events, unconfirmed_events

	def check_for_upcoming_events(self):
		events = self.get_events()

		# iterate through the events to add the events due to be reminded into the upcoming events list
		for event in events:
			mins_to_event = utils.get_mins_between_now_and_event(event)
			
			# if the event is using the default reminder time
			if(event['reminders']['useDefault']):
				# default reminder time is 30 minutes
				reminder_mins = 30
				
			else:
				reminder_mins = event['reminders']['overrides'][0]['minutes']

			# check if the event is ready to be in a reminder
			if (mins_to_event < reminder_mins) and (mins_to_event > 0):
				if (event not in self.unconfirmed_events) and (event not in self.confirmed_events):
					self.upcoming_events.append(event)

		return self.upcoming_events

	def move_upcoming_events_to_confirmed_events(self):
		self.confirmed_events.extend(self.upcoming_events)
		self.upcoming_events.clear()
		pass

	def move_unconfirmed_events_to_confirmed_events(self):
		self.confirmed_events.extend(self.unconfirmed_events)
		self.unconfirmed_events.clear()
		pass

	def move_upcoming_events_to_unconfirmed_events(self):
		self.unconfirmed_events.extend(self.upcoming_events)
		self.upcoming_events.clear()
		pass

	def clear_confirmed_list_of_past(self):
		for event in self.confirmed_events:
			time_difference_mins = utils.get_mins_between_now_and_event(event)

			if time_difference_mins < 0:
				self.confirmed_events.remove(event)

if __name__ == "__main__":
	event_manager = EventManager(service_account_file='credentials.json')
	print(event_manager.check_for_upcoming_events())
	pass