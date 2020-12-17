from threading import Timer
from .timer_loop import TimerLoop
from .event_manager import EventManager
from .make_reminder import make_reminder


class ReminderSystem(EventManager):
    def __init__(
        self, 
        service_account_file, 
        interval, 
        confirmation_time, 
        on_reminder=None, 
        on_confirmation_timeout=None
    ):
        super().__init__(service_account_file)
        self.interval = interval
        self.confirmation_time = confirmation_time

        self.on_reminder_callback = on_reminder
        self.confirmation_timeout_callback = on_confirmation_timeout

        self.timer_loop = None
        self.confirmation_timer = None

    def start(self):
        self.timer_loop = TimerLoop(self.interval, self.check_events)
        self.confirmation_timer = self.__init_confirmation_timer(self.confirmation_time)

        self.timer_loop.start()
        pass

    def stop(self):
        self.timer_loop.stop()
        pass

    def check_events(self):
        upcoming_events, unconfirmed_events = self.get_events_to_be_reminded()

        if upcoming_events or unconfirmed_events:
            reminder = make_reminder(upcoming_events, unconfirmed_events)
            
            if self.on_reminder_callback is not None:
                self.timer_loop.stop()
                self.on_reminder_callback(reminder)

                self.confirmation_timer = self.__init_confirmation_timer(self.confirmation_time)
                self.confirmation_timer.start()
        pass

    def confirm_reminder(self):
        if self.confirmation_timer.isAlive():
            self.confirmation_timer.cancel()

        self.move_upcoming_events_to_confirmed_events()
        self.move_unconfirmed_events_to_confirmed_events()
        
        if not self.timer_loop.isAlive():
            self.timer_loop.start()

    def get_unconfirmed_reminders(self):
        unconfirmed_events = self.unconfirmed_events
        unconfirmed_reminder = make_reminder([], unconfirmed_events)
        
        return unconfirmed_reminder

    def confirm_unconfirmed_reminders(self):
        self.move_unconfirmed_events_to_confirmed_events()

    def set_on_reminder_callback(self, callback):
        self.on_reminder_callback = callback

    def set_timeout_callback(self, callback):
        self.confirmation_timeout_callback = callback

    def __init_confirmation_timer(self, confirmation_time):
        confirmation_timer = Timer(confirmation_time, self.__confirmation_timeout)
        confirmation_timer.daemon = True
        
        return confirmation_timer

    def __confirmation_timeout(self):
        self.move_upcoming_events_to_unconfirmed_events()
        self.timer_loop.start()
        
        if self.confirmation_timeout_callback is not None:
            self.confirmation_timeout_callback()
        pass


if __name__ == "__main__":
    from time import sleep

    service_account_file = 'credentials.json'
    interval = 5
    confirmation_timer = 5

    reminder_system = ReminderSystem(service_account_file, interval, confirmation_timer)

    def on_reminder(reminder):
        print(reminder)
        pass

    def on_confirm_timeout():
        print('confirmation timed out')
        pass

    reminder_system.set_on_reminder_callback(on_reminder)
    reminder_system.set_timeout_callback(on_confirm_timeout)

    reminder_system.start()

    sleep(interval + confirmation_timer)
    sleep(interval + confirmation_timer/2)

    reminder_system.confirm_reminder()
    print('reminder confirmed')

    while True:
        pass
