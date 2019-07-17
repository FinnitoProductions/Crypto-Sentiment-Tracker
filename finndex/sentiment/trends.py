import datetime

import numpy
from pytrends.request import TrendReq

from finndex.graphing import gauge
from finndex.util import mathutil

MIN_TRENDS_VAL = 0
MAX_TRENDS_VAL = 100

def getTrendsDataRaw(keyword, startDate, endDate):
   trends = TrendReq(hl='en-US', tz=0) # tz is timezone offset from UTC in minutes
   trend = trends.get_historical_interest([keyword], 
                                             year_start=startDate.year, month_start=startDate.month, 
                                             day_start=startDate.day, hour_start=startDate.hour, 
                                             year_end=endDate.year, month_end=endDate.month, 
                                             day_end=endDate.day, hour_end=endDate.hour, 
                                             cat=0, geo='', gprop='', sleep=0)[keyword]

   return trend
'''
From trends.google.com: 

Numbers represent search interest relative to the highest point on the chart for the given region and time. 
A value of 100 is the peak popularity for the term. 
A value of 50 means that the term is half as popular. 
A score of 0 means there was not enough data for this term.
'''
def getTrendsData(keyword, startDate, endDate):
   trend = getTrendsDataRaw(keyword, startDate, endDate)

   newDict = {}
   for date, val in trend.items():
      newDict[date] = mathutil.map(val, MIN_TRENDS_VAL, MAX_TRENDS_VAL, 0, 1)

   return newDict

'''
Determines the average trending data for a given keyword on each day within a given range of dates.
Because the Trends API posts multiple values per day, averages each of these results to find a single result
per day.

Returns a dictionary with key as date and value the trends data on that date.
'''
def getTrendsDateRange(startDate, endDate, keyword="Bitcoin"):
   trendsData = getTrendsData(keyword, startDate, endDate)

   dateDict = {}
   for date, value in trendsData.items():
      if not date in dateDict:
         dateDict[date] = [value]
      else:
         dateDict[date] += [value]
         
   return {date.date():numpy.average(vals) for date, vals in dateDict.items()}

# Determines the Google trends data on a given date.
def getTrendsDate(date=datetime.datetime.now(), keyword="Bitcoin"):
   startDate = datetime.datetime(year=date.year, month=date.month, day=date.day)
   trendsData = getTrendsDataRaw(keyword, startDate, startDate + datetime.timedelta(days=1))
   
   return numpy.average(trendsData)

def displayTrendsDate(date=datetime.datetime.now(), display=True, keyword="Bitcoin"):
   return gauge.displayNeutralGauge(getTrendsDate(date=date, keyword=keyword), MIN_TRENDS_VAL, MAX_TRENDS_VAL, "Google Trends", display=display)
