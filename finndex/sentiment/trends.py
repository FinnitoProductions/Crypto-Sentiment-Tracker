import datetime

import numpy
from finndex.util import cryptocurrencies, dateutil, mathutil
from pytrends.request import TrendReq
import pandas as pd

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
def get_trends_dates(start_date, end_date, currencies_list):
    '''
    ' Retrieves the Google Trends values (mapped into a range between 0 and 1) between two dates,
    ' inclusive. The values represent search interest relative to the peak over the provided time interval,
    ' where a higher value suggests more popularity. The outer column of the returned data frame represents the 
    ' retrieved cryptocurrencies while the inner columns represents the retrieved metric (only "Trends", in this case).
    ' 
    ' start_date (datetime) - the start date, with month, day, and year provided
    ' end_date (datetime) - the end date, with month, day, and year provided
    ' currencies_list (list) - the list of currencies to associate with the given fear and greed values
    '''
    trends = TrendReq(hl='en-US', tz=0) # tz is timezone offset from UTC in minutes
    
    trends_data_frame = pd.DataFrame()
    for currency in currencies_list:
        trend = trends.get_historical_interest([currency.value.name], 
                                         year_start=start_date.year, month_start=start_date.month, 
                                         day_start=start_date.day, hour_start=start_date.hour, 
                                         year_end=end_date.year, month_end=end_date.month, 
                                         day_end=end_date.day, hour_end=end_date.hour, 
                                         cat=0, geo='', gprop='', sleep=0)
        trend.index = trend.index.floor('d')
        trend = trend.drop('isPartial', axis=1)
        trend.columns = pd.MultiIndex.from_product([[currency], ["Trends"]])
        trend = trend.groupby("date").mean()
        trends_data_frame = pd.concat([trend, trends_data_frame], axis=1)


    
    trends_data_frame = trends_data_frame.apply(lambda val: mathutil.map(val, 
                                                                        MIN_TRENDS_VAL, 
                                                                        MAX_TRENDS_VAL, 
                                                                        0, 
                                                                        1))

    return trends_data_frame

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
Determines the average trending data for a given keyword on each day within a given range of dates.
Because the Trends API posts multiple values per day, averages each of these results to find a single result
per day.

Returns a dictionary with key as date and value the trends data on that date.
'''
def getTrendsDateRange(startDate, endDate, currenciesList=[cryptocurrencies.Cryptocurrencies.BITCOIN]):
   currenciesDict = {}
   for currency in currenciesList:
      trendsData = getTrendsData(currency.value, startDate, endDate)

      dateDict = {}
      for date, value in trendsData.items():
         if not date in dateDict:
            dateDict[date] = [value]
         else:
            dateDict[date] += [value]
            
      currenciesDict[currency] = {date.date():numpy.average(vals) for date, vals in dateDict.items()}

   return currenciesDict

# Determines the Google trends data on a given date.
def getTrendsDate(date=dateutil.getCurrentDateTime(), keyword="Bitcoin"):
   startDate = datetime.datetime(year=date.year, month=date.month, day=date.day)
   trendsData = getTrendsDataRaw(keyword, startDate, startDate + datetime.timedelta(days=1))
   
   return numpy.average(trendsData)

def displayTrendsDate(date=dateutil.getCurrentDateTime(), display=True, keyword="Bitcoin"):
   return gauge.displayNeutralGauge(getTrendsDate(date=date, keyword=keyword), MIN_TRENDS_VAL, MAX_TRENDS_VAL, "Google Trends", display=display)
