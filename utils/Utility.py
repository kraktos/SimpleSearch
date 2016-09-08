import datetime
import time


def begin_time(message):
    print "\n{} started..".format(message)
    return time.time()


def end_time(message, start_time):
    duration = round(float(time.time() - start_time), 4)
    print "{} completed in {} secds \n".format(message, duration)


def get_date_time(x):
    return datetime.datetime.fromtimestamp(
        int(x)
    ).strftime('%Y-%m-%d_%H:%M:%S')
