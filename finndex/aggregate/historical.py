'''
Manages a set of historical data to plot the aggregate sentiment (with variable weight) relative to other values.
'''

import datetime
import functools
from enum import Enum

import ipywidgets as widgets
import numpy as np
import pandas as pd

from finndex.fundamental import coinmetrics
from finndex.sentiment import fearandgreed, trends
from finndex.util import cryptocurrencies, dateutil, mathutil
from IPython.display import display

from scipy.stats import pearsonr

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

'''
Represents a piece of data with several values over time. 'values' is a dictionary with the date as the key
and the corresponding value on that date as the value. 'slider' is the slider modifying the weight of this reading.
'''
class HistoricalDataReading:
   def __init__(self, values, slider):
      self.name = slider.description
      self.values = values
      self.slider = slider

'''
Represents all possible values that can be plotted historically. Each value corresponds to a standard data retrieval function.
'''
class HistoricalMetricType(Enum):
   FEAR_AND_GREED = functools.partial(fearandgreed.get_fg_dates)
   TRENDS = functools.partial(trends.get_trends_dates)
   BLOCK_COUNT = functools.partial(coinmetrics.get_coinmetrics_dates, [coinmetrics.CoinMetricsData.BLOCK_COUNT])
   TRANSACTION_CNT = functools.partial(coinmetrics.get_coinmetrics_dates, [coinmetrics.CoinMetricsData.TRANSACTION_CNT])
   DAILY_ADDRESSES = functools.partial(coinmetrics.get_coinmetrics_dates, [coinmetrics.CoinMetricsData.DAILY_ADDRESSES])
   MARKET_CAP = functools.partial(coinmetrics.get_coinmetrics_dates, [coinmetrics.CoinMetricsData.MARKET_CAP])
   PRICE_USD = functools.partial(coinmetrics.get_coinmetrics_dates, [coinmetrics.CoinMetricsData.PRICE_USD])

'''
Computes and plots a set of daily historical sentiment values given a set of keywords. Weights can be modified using sliders;
if weights are provided in the 'weights' parameter, presents a static graph using those weights.
'''
class HistoricalSentimentManager:
   def __init__(self, keywords_list, currencies_list, 
                        start_date = datetime.datetime.now() - datetime.timedelta(weeks=4), 
                        end_date = datetime.datetime.now(), weights = None):
      self.keywords_list = keywords_list
      self.currencies_list = currencies_list
      self.start_date = start_date
      self.end_date = end_date
      if weights != None:
         self.weights = weights
      else:
         self.weights = [1.0 / len(keywords_list) for keyword in keywords_list] # equal weighting for all values
      
      self.historical_sentiment = None

   '''
   Computes the weighted historical sentiment with the date as the key and the historical sentiment on that date as the value.
   '''
   def get_historical_sentiment(self): 
      return_frame = self.historical_sentiment

      if return_frame is None:
         frames = [metric.value(self.start_date, self.end_date, self.currencies_list) for metric in self.keywords_list]
         combined = pd.concat(frames, axis=1)
         
         return_frame = pd.DataFrame()
         for cryptocurrency in combined.columns.levels[0]:
            interp = combined[cryptocurrency].interpolate().interpolate(limit_direction='backward')
            weighted = interp.apply(lambda row: np.average(row, weights=self.weights), axis=1)
            return_frame[cryptocurrency] = weighted

      self.historical_sentiment = return_frame

      return return_frame

   def get_prices(self):
      return HistoricalMetricType.PRICE_USD.value(self.start_date, self.end_date, self.currencies_list, normalize = False)

   def get_price_correlation(self):
      historical = self.get_historical_sentiment()
      prices = self.get_prices()

      return {(currency, pearsonr(historical[currency].values[1:], prices[currency]['PriceUSD'].values)[0]) for currency in self.currencies_list}


   def get_index_sentiment(self, weights=None):
      if weights == None:
         weights = [1.0 / len(self.currencies_list) for currency in self.currencies_list]
      return self.get_historical_sentiment().apply(lambda row: np.average(row, weights=weights), axis=1)