'''
Contains utility functions providing an extension to Python's datetime.
'''

import datetime

import pytz

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

DESIRED_DATE_FORMAT = "%Y-%m-%d"
DESIRED_TIME_ZONE = pytz.timezone("US/Pacific")

'''
Converts a timestamp (represented as a string) in one date format into another date format. Returns
the newly formatted date as a string.

A list of acceptable date format characters can be found at the following link.
https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
'''
def convertTimestamp(timestamp, initialFormat, desiredFormat):
    return datetime.datetime.strptime(timestamp, initialFormat).strftime(desiredFormat)

'''
A generator function (inclusive on both endpoints) to iterate through every date or datetime in a given range.
'''
def dateRange(startDate, endDate):
   for i in range(int((endDate - startDate).days) + 1):
      yield startDate + datetime.timedelta(i)

'''
Retrieves the current time and date in Pacific time.
'''
def getCurrentDateTime():
   return datetime.datetime.now(DESIRED_TIME_ZONE)
