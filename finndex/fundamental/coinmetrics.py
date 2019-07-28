'''
Uses the CoinMetrics API to retrieve several useful pieces of fundamental data on cryptocurrencies.
'''

import datetime
import json
from enum import Enum

from finndex.graphing import timeseries
from finndex.util import cryptocurrencies, dateutil, mathutil, webutil

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

COIN_METRICS_API_PREFIX = "https://community-api.coinmetrics.io/v2/"
NETWORK_METRIC_SUFFIX = "assets/{}/metricdata?metrics="

COIN_METRICS_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Represents an enum containing several possible keywords which can be used with the CoinMetrics API.
class CoinMetricsData(Enum):
    BLOCK_COUNT = "BlkCnt"
    MARKET_CAP = "CapRealUSD"
    PRICE_USD = "PriceUSD"
    TRANSACTION_CNT = "TxCnt"
    DAILY_ADDRESSES = "AdrActCnt"
    
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
        dataSet = loadedPageData['series']
        
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
