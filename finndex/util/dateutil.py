import datetime

DESIRED_DATE_FORMAT = "%Y-%m-%d"

'''
Converts a timestamp (represented as a string) in one date format into another date format. Returns
the newly formatted date as a string.

A list of acceptable date format characters can be found at the following link.
https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
'''
def convertTimestamp(timestamp, initialFormat, desiredFormat):
    return datetime.datetime.strptime(timestamp, initialFormat).strftime(desiredFormat)
