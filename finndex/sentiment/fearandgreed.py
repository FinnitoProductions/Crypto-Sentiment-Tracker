'''
Extracts data from the Fear and Greed API and displays it instantaneously and provides a historical representation in a dictionary.
'''

import datetime
import json

from finndex.graphing import gauge
from finndex.util import dateutil, mathutil, webutil

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

FEAR_AND_GREED_ADDRESS = "https://api.alternative.me/fng/?limit=0&date_format=us"
    
MIN_FEAR_AND_GREED = 0
MAX_FEAR_AND_GREED = 100

# Uses the Fear and Greed API to extract the Fear and Greed value from any given date.
def getFearAndGreed(date):
    timestampFormatted = date.strftime(dateutil.DESIRED_DATE_FORMAT) 
    
    return getAllFearAndGreed()[timestampFormatted]
   
'''
Uses the Fear and Greed API to extract all Fear and Greed values available as a range from 0-1. Returns a dictionary with key as date
and value the Fear and Greed value on that date.
'''
def getAllFearAndGreed():
    fearAndGreedVals = webutil.getPageContent(FEAR_AND_GREED_ADDRESS)
    jsonUnpacked = json.loads(fearAndGreedVals)
    dataArr = jsonUnpacked['data']
    dataDict = {}
    for singleDay in dataArr:
        timestampFormatted = dateutil.convertTimestamp(singleDay['timestamp'], '%m-%d-%Y', dateutil.DESIRED_DATE_FORMAT)
        dataDict[timestampFormatted] = mathutil.map(int(singleDay['value']), MIN_FEAR_AND_GREED, MAX_FEAR_AND_GREED, 0, 1)
        
    return dataDict

'''
Uses the Fear and Greed API to extract all Fear and Greed values available in a given date range. Returns a dictionary with key as date
and value the Fear and Greed value on that date.
'''
def getFearAndGreedDateRange(startDate, endDate):
    fearAndGreedVals = getAllFearAndGreed()
    dataDict = {}

    for date, data in fearAndGreedVals.items():
        timestampDate = datetime.datetime.strptime(date, '%Y-%m-%d')

        if timestampDate.date() >= startDate.date() and timestampDate.date() <= endDate.date(): # only consider year, month, and day
            dataDict[timestampDate.date()] = data
        
    return dataDict

# Displays a given Fear and Greed value (0-100) in a convenient gauge format.
def displayFearAndGreedNum(val, display=True):
    return gauge.Gauge(labels=['Extreme Fear','Fear','Greed','Extreme Greed'], 
      colors=['#c80000','#c84b00','#64a000', '#00c800'], currentVal=val, minVal = 0,
                 maxVal = 1, title='Fear and Greed', displayGauge=display)

# Displays the Fear and Greed value from a given date in a convenient gauge format.
def displayFearAndGreedDate(date=datetime.datetime.now(), display=True):
    return displayFearAndGreedNum(getFearAndGreed(date), display)
