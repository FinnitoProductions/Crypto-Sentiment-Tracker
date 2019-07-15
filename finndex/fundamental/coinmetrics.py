import datetime
import json
from enum import Enum

from finndex.graphing import timeseries
from finndex.util import dateutil, mathutil, webutil

COIN_METRICS_API_PREFIX = "https://community-api.coinmetrics.io/v2/"
NETWORK_METRIC_SUFFIX = "assets/%s/metricdata?metrics="
BITCOIN_ASSET_ID = "btc"
DAILY_ADDR_METRIC_ID = "AdrActCnt"

COIN_METRICS_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


# Represents an enum containing several possible keywords which can be used with the CoinMetrics API.
class CoinMetricsData(Enum):
    BLOCK_COUNT = "BlkCnt"
    MARKET_CAP = "CapRealUSD"
    PRICE_USD = "PriceUSD"
    TRANSACTION_CNT = "TxCnt"
    DAILY_ADDRESSES = "AdrActCnt"
    
'''
Retrieves a dictionary containing the CoinMetrics data across all time for a given set of statistics.

Valid and retrievable statistics are listed in the CoinMetricsData class.

Returns a dictionary containing a key 'metrics' pointing to all statistics which were retrieved and a key 'series' 
which points to an list of dictionaries. Each dictionary in this list contains a timestamp (key 'time') formatted to
the microsecond and a key 'values' pointing to a list of string values. The list is ordered in the same fashion
as the 'metrics' list.
'''
def getCoinMetricsDict(*keywords):
    desiredMetrics = COIN_METRICS_API_PREFIX + NETWORK_METRIC_SUFFIX % BITCOIN_ASSET_ID
    for keyword in keywords:
        desiredMetrics += keyword.value + ","
    desiredMetrics = desiredMetrics[:-1] # remove final comma
    
    return json.loads(webutil.getPageContent(desiredMetrics))['metricData']

# Retrieves from CoinMetrics a metric of a given keyword 'desiredData' (type CoinMetricsData) from a given date.
def getCoinMetricsData(desiredData, date):
    dataDict = getCoinMetricsDict(desiredData)
    
    timestampFormatted = "%04d-%02d-%02d" % (date.year, date.month, date.day)

    return [singleDay['values'][0] for singleDay in dataDict['series'] 
            if timestampFormatted in singleDay['time']][0]

# Retrieves from CoinMetrics a metric (from [0, 1]) of a given keyword 'desiredData' (type CoinMetricsData) from a given date range.
def getCoinMetricsDateRange(desiredData, startDate, endDate):
    dataDict = getCoinMetricsDict(desiredData)

    minVal = min(float(singleDay['values'][0]) for singleDay in dataDict['series'])
    maxVal = max(float(singleDay['values'][0]) for singleDay in dataDict['series'])

    valueDict = {}
    for singleDay in dataDict['series']:
        timestampDate = datetime.datetime.strptime(singleDay['time'], "%Y-%m-%dT%H:%M:%S.%fZ")

        if timestampDate.date() >= startDate.date() and timestampDate.date() <= endDate.date():
            valueDict[timestampDate.strftime(dateutil.DESIRED_DATE_FORMAT)] = mathutil.map(float(singleDay['values'][0]), minVal, maxVal, 0, 1)

    return valueDict
    

# Retrieves from CoinMetrics a metric of a given keyword 'desiredData' (type CoinMetricsData) across all time.
def getAllCoinMetricsData(keyword):
    data = getCoinMetricsDict(keyword)['series']
    return {dateutil.convertTimestamp(singleDay['time'], COIN_METRICS_TIMESTAMP_FORMAT, dateutil.DESIRED_DATE_FORMAT):float(singleDay['values'][0]) for singleDay in data}

# Plots all data available from CoinMetrics across time.
def plotAllCoinMetricsData():
   for dataKey in list(CoinMetricsData):
      data = getAllCoinMetricsData(dataKey)

      timeseries.plotTimeSeries({dataKey: {'x': list(data.keys()), 'y': list(data.values())}}, title=dataKey.value, dateFormat=dateutil.DESIRED_DATE_FORMAT)
