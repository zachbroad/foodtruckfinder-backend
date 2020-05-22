from datetime import datetime


def juxtapose(dt):
    return dt.year * 10000000000 + dt.month * 100000000 + dt.day * 1000000 + 10000 * dt.hour + 100 * dt.minute + 1 * dt.second


def datetimefield_to_datetime(dtf):
    return datetime(year=dtf.year, month=dtf.month, day=dtf.day, hour=dtf.hour, minute=dtf.minute, second=dtf.second)

