'''
Uses the CoinMetrics API to retrieve several useful pieces of fundamental data on cryptocurrencies.
'''

import datetime
import json
from enum import Enum

from finndex.util import cryptocurrencies, dateutil, mathutil, webutil
import pandas as pd

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

COIN_METRICS_API_PREFIX = "https://community-api.coinmetrics.io/v2/"
NETWORK_METRIC_SUFFIX = "assets/{}/metricdata?metrics="

COIN_METRICS_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Represents an enum containing several possible keywords which can be used with the CoinMetrics API.
class CoinMetricsData(Enum):
    BLOCK_COUNT = "BlkCnt"
    MARKET_CAP = "CapMrktCurUSD"
    PRICE_USD = "PriceUSD"
    TRANSACTION_CNT = "TxCnt"
    DAILY_ADDRESSES = "AdrActCnt"

def normalize_col(col):
   '''
   ' Linearly normalizes a column within a pandas DataFrame by dividing each entry by the maximum value in the column.
   ' Returns the resultant column.
   ' 
   ' col (Series): the column of a given pandas data frame 
   '''
   return col / (col.loc[col.idxmax()])
   
def get_coinmetrics_dates(metrics_list, start_date, end_date, currencies_list, normalize = True, normalize_all_time = True):
   '''
   ' Retrieves a multi-layered data frame containing a list of metrics corresponding to a list of cryptocurrencies.
   ' The outer columns of the frame represent the cryptocurrencies, and the inner columns represent the retrieved metrics.
   ' 
   ' metrics_list (list<CoinMetricsData>): the list of metrics to be retrieved
   ' start_date (datetime) - the start date, with month, day, and year provided
   ' end_date (datetime) - the end date, with month, day, and year provided
   ' currencies_list (list<Cryptocurrencies>): the list of cryptocurrencies to be retrieved
   '''
   col_index = pd.MultiIndex.from_product([currencies_list, [metric.value for metric in metrics_list]])
   return_frame = pd.DataFrame(columns = col_index)
   
   for currency in currencies_list:
     desired_metrics = COIN_METRICS_API_PREFIX + NETWORK_METRIC_SUFFIX.format(currency.value.ticker.lower())
     for keyword in metrics_list:
         desired_metrics += keyword.value + ","
     desired_metrics = desired_metrics[:-1] # remove final comma
      
     page_content = json.loads(webutil.getPageContent(desired_metrics))['metricData']
     metrics_list_retrieved = page_content['metrics']
   
     metrics_frame = pd.DataFrame(page_content['series'])
     # retrieved API data contains "values" column with list of values, so explode into individual columns
     metrics_frame = pd.concat([metrics_frame.drop('values',axis=1), metrics_frame['values'].apply(pd.Series)],axis=1)
     # individual exploded columns are named with sequential natural numbers, so rename with corresponding metric
     metrics_frame = metrics_frame.rename({i:metric for (i, metric) in enumerate(metrics_list_retrieved)}, axis=1)
     metrics_frame = metrics_frame.rename({'time':'date'}, axis=1)
     metrics_frame.index = pd.to_datetime(metrics_frame['date'])
     metrics_frame.index = metrics_frame.index.tz_localize(None)
     metrics_frame.index = metrics_frame.index.floor('d')
   
     for metric in metrics_list_retrieved:
        metrics_frame[metric] = metrics_frame.apply(lambda row: float(row[metric]) if row[metric] != None else None, axis=1)
        return_frame[currency, metric] = metrics_frame[metric]

   return_frame = return_frame.astype('float')

   # linearly normalize data between 0-1 based on maximum in non-date-filtered frame
   if normalize and normalize_all_time:
      return_frame = return_frame.apply(normalize_col)

   # fill in missing entries, filter by date
   return_frame = return_frame.interpolate().loc[(return_frame.index >= start_date) & (return_frame.index < end_date)]

   # linearly normalize data between 0-1 based on maximum in date-filtered frame
   if normalize and not normalize_all_time:
      return_frame = return_frame.apply(normalize_col)

   return return_frame

   
'''
Retrieves a dictionary containing the CoinMetrics data across all time for a given set of statistics for a given
set of cryptocurrencies. 

Valid and retrievable statistics are listed in the CoinMetricsData class.

Returns a dictionary containing a key 'metrics' pointing to all statistics which were retrieved and a key 'series' 
which points to an list of dictionaries. Each dictionary in this list contains a timestamp (key 'time') formatted to
the microsecond and a key 'values' pointing to a list of string values. The list is ordered in the same fashion
as the 'metrics' list.
'''
def getCoinMetricsDict(currenciesList, metricsList):
    returnDict = {}

    for currency in currenciesList:
        returnDict[currency] = {}
        
        desiredMetrics = COIN_METRICS_API_PREFIX + NETWORK_METRIC_SUFFIX.format(currency.value.lower())
        for keyword in metricsList:
            desiredMetrics += keyword.value + ","
        desiredMetrics = desiredMetrics[:-1] # remove final comma
        
        loadedPageData = json.loads(webutil.getPageContent(desiredMetrics))['metricData']
        metricsListRetrieved = loadedPageData['metrics']
        dataSet = pd.DataFrame(loadedPageData['series'])
        
        for dataDict in dataSet:
            valueDict = {CoinMetricsData(metricsListRetrieved[idx]):float(value) 
                     for idx, value in enumerate(dataDict['values'])}
            returnDict[currency][datetime.datetime.strptime(dataDict['time'], 
                                                                  COIN_METRICS_TIMESTAMP_FORMAT)] = valueDict
    return returnDict

'''
Retrieves from CoinMetrics a set of metrics (from [0, 1]) of a given set of currencies (type Cryptocurrencies) 
from a given date range.
'''
def getCoinMetricsDateRange(metric, startDate, endDate, currenciesList):
    dataDict = getCoinMetricsDict(currenciesList, [metric])
    
    newDict = {}
    for currency, values in dataDict.items():
        numMetrics = len(values[list(values.keys())[0]])
        
        minVal = min(val[metric] for val in values.values()) 
        maxVal = max(val[metric] for val in values.values())
            
        newDict[currency] = {}
        
        for date, metricsDict in values.items():
            if date.date() >= startDate.date() and date.date() <= endDate.date():
                newDict[currency][date] = mathutil.map(metricsDict[metric], minVal, maxVal, 0, 1) 
                
    return newDict
    
# Plots all data available from CoinMetrics across time for a given currency.
def plotAllCoinMetricsData(currency, startDate=dateutil.getCurrentDateTime() - datetime.timedelta(days=1000), endDate=dateutil.getCurrentDateTime()):
    for dataKey in list(CoinMetricsData):
        data = getCoinMetricsDateRange(dataKey, startDate, endDate, [currency])

        timeseries.TimeSeries("{}: {}".format(str(currency), str(dataKey)), {dataKey: data})
