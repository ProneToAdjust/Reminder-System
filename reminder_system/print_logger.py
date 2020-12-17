import datetime as dt


def log(log_message):
    time_now = dt.datetime.now()
    h_m_s = f'[{time_now.hour}:{time_now.minute}:{time_now.second}]'
    print(f"{h_m_s} LOG: {log_message}")


if __name__ == '__main__':
    log("test message")
