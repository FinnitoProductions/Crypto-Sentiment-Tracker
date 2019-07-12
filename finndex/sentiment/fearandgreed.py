import datetime
import json

from finndex.graphing import gauge
from finndex.util import dateutil, webutil

FEAR_AND_GREED_ADDRESS = "https://api.alternative.me/fng/?limit=0&date_format=us"
    
MIN_FEAR_AND_GREED = 0
MAX_FEAR_AND_GREED = 100

# Uses the Fear and Greed API to extract the Fear and Greed value from any given date.
def getFearAndGreed(date):
    timestampFormatted = date.strftime(dateutil.DESIRED_DATE_FORMAT) 
    
    return getAllFearAndGreed()[timestampFormatted]
   
'''
Uses the Fear and Greed API to extract all Fear and Greed values available. Returns a dictionary with key as date
and value the Fear and Greed value on that date.
'''
def getAllFearAndGreed():
    fearAndGreedVals = webutil.getPageContent(FEAR_AND_GREED_ADDRESS)
    jsonUnpacked = json.loads(fearAndGreedVals)
    dataArr = jsonUnpacked['data']
    dataDict = {}
    for singleDay in dataArr:
        timestampFormatted = dateutil.convertTimestamp(singleDay['timestamp'], '%m-%d-%Y', dateutil.DESIRED_DATE_FORMAT)
        dataDict[timestampFormatted] = int(singleDay['value'])
        
    return dataDict

# Displays a given Fear and Greed value (0-100) in a convenient gauge format.
def displayFearAndGreedNum(val):
    return gauge.Gauge(labels=['Extreme Fear','Fear','Greed','Extreme Greed'], 
      colors=['#c80000','#c84b00','#64a000', '#00c800'], currentVal=val, minVal = MIN_FEAR_AND_GREED,
                 maxVal = MAX_FEAR_AND_GREED, title='Fear and Greed')

# Displays the Fear and Greed value from a given date in a convenient gauge format.
def displayFearAndGreedDate(date):
    return displayFearAndGreedNum(getFearAndGreed(date))
