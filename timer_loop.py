from threading import Timer


class TimerLoop:
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.timer_thread = None

    def start(self):
        self.__create_new_timer_thread()
        self.__start_timer_thread()

    def stop(self):
        self.__stop_timer_thread()

    def isAlive(self):
        return self.timer_thread.isAlive()

    def __on_timeout(self):
        self.__restart_timer_thread()
        self.__call_function()

    def __create_new_timer_thread(self):
        self.timer_thread = Timer(interval=self.interval, function=self.__on_timeout)
        self.timer_thread.daemon = True

    def __start_timer_thread(self):
        self.timer_thread.start()

    def __stop_timer_thread(self):
        self.timer_thread.cancel()

    def __restart_timer_thread(self):
        self.__create_new_timer_thread()
        self.__start_timer_thread()

    def __call_function(self):
        self.function()


if __name__ == '__main__':
    timer_loop = TimerLoop(interval=2, function=lambda: print('function called'))
    timer_loop.start()

    from time import sleep

    sleep(5)

    timer_loop.stop()

    while True:
        pass
