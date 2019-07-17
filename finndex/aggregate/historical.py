'''
Manages a set of historical data to plot the aggregate sentiment (with variable weight) relative to other values.
'''

import datetime
import functools
from enum import Enum

import ipywidgets as widgets
import numpy as np
from finndex.aggregate import sliders
from finndex.fundamental import coinmetrics
from finndex.graphing import timeseries
from finndex.sentiment import fearandgreed, trends
from finndex.util import dateutil, mathutil
from IPython.display import display

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"


'''
Represents a piece of data with several values over time. 'values' is a dictionary with the date as the key
and the corresponding value on that date as the value. 'slider' is the slider modifying the weight of this reading.
'''
class HistoricalDataReading:
    def __init__(self, name, values, slider):
        self.name = name
        self.values = values
        self.slider = slider

'''
Represents all possible values that can be plotted historically. Each value corresponds to a standard data retrieval function.
'''
class HistoricalMetricType(Enum):
   FEAR_AND_GREED = functools.partial(fearandgreed.getFearAndGreedDateRange)
   TRENDS = functools.partial(trends.getTrendsDateRange)
   BLOCK_COUNT = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.BLOCK_COUNT)
   TRANSACTION_CNT = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.TRANSACTION_CNT)
   DAILY_ADDRESSES = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.DAILY_ADDRESSES)
   MARKET_CAP = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.MARKET_CAP)
   PRICE_USD = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.PRICE_USD)

'''
Computes and plots a set of daily historical sentiment values given a set of keywords. Weights can be modified using sliders;
if weights are provided in the 'weights' parameter, presents a static graph using those weights.
'''
class HistoricalSentimentManager:
   def __init__(self, weightedKeywordsList, startDate = dateutil.getCurrentDateTime() - datetime.timedelta(weeks=4), endDate = dateutil.getCurrentDateTime(), weights = None, 
                unweightedKeywordsList = []):
      self.dataVals = []

      self.startDate = startDate
      self.endDate = endDate
      self.weights=weights
      self.unweightedKeywordsList = unweightedKeywordsList
      self.weightedKeywordsList = weightedKeywordsList

      slidersList = self.computeDataVals()

      if weights == None:
         self.sliderManager = sliders.SliderManager(self.displayGraph, slidersList)
      else:
         self.sliderManager = None

      self.graph = None

   '''
   Generates a list of sliders for and computes the historical values of all desired keywords.
   '''
   def computeDataVals(self):
      slidersList = []
      for idx, keyword in enumerate(self.weightedKeywordsList):
         dataReading = HistoricalDataReading(name=str(keyword), values=keyword.value(startDate=self.startDate, endDate=self.endDate), 
                                   slider=sliders.Slider(str(keyword), widgets.FloatSlider(min=0.0, max=sliders.MAX_VAL, 
                                                                                           step=sliders.STEP, 
                                                                                           value=self.weights[idx] if self.weights != None else 0.0)))
         self.dataVals += [dataReading]
         slidersList += [dataReading.slider]

      return slidersList

   '''
   Removes any missing data from a weighted dataset by distributing the weight of any missing values (represented by negative infinity)
   to all subsequent values. Does not modify the passed-in list; returns a modified shallow copy.
   '''
   @staticmethod
   def removeGaps(values):
      values = values.copy()
      values.sort() # place all values with -infinity first so they can be dealt with

      # Account for any gaps in the data
      for i, (value, weight) in enumerate(values):
         if value == -float('inf'): # no value provided
            # As long as the last value isn't -infinity (this would mean no data is provided), distribute the
            # weight of the missing data set to all subsequent values
            if i != len(values) - 1:
               weightPerElement = weight / (len(values) - i - 1)
            values[i] = (0.0, 1.0)

            for j, val in enumerate(values[i+1:], start = i+1):
               values[j] = (values[j][0], values[j][1] + weightPerElement)

      return values

   '''
   Computes the weighted historical sentiment with the date as the key and the historical sentiment on that date as the value.
   '''
   def getHistoricalSentiment(self):
      sentimentByDate = {}
   
      for date in dateutil.dateRange(self.startDate.date(), self.endDate.date()):
         sentimentByDate[date] = []

         # Populate the sentiment dictionary with date pointing to a list of every corresponding historical sentiment value
         for historicalReading in self.dataVals:
            sentimentByDate[date] += [(historicalReading.values[date]
                                       if date in historicalReading.values
                                      else -float('inf'), historicalReading.slider.getReading())] # add tuple with value (-infinity if nothing provided) and weight

         values = HistoricalSentimentManager.removeGaps(sentimentByDate[date])

         sentimentByDate[date] = 0

         # Find the weighted average of sentiment on a given day
         for value, weight in values:
            sentimentByDate[date] += value * weight

      return sentimentByDate

   '''
   Displays/updates a graph given a dictionary of values 'valueDict' (value type as key and HistoricalDataReading as value).
   If there is no existing graph, generates a new one based on this dictionary. Overlays any additional data specified
   as keyworded-arguments with date as key and the value on that date as the value.

   The values within valueDict are the ones which can be modified in the future. All additional values as keyworded-arguments
   will remain static when plotted and cannot be removed.
   '''
   def displayGraph(self):
      data = {'aggregateSentiment': self.getHistoricalSentiment()}

      # Overlay any additional keywords provided
      for additionalKeyword in self.unweightedKeywordsList:
         value = additionalKeyword.value(startDate = self.startDate, endDate = self.endDate)
         if len(self.unweightedKeywordsList) == 1:
            data[additionalKeyword] = value # If there is only one keyword, the y-axis will be labeled with that keyword
         else:
            ADDITIONAL_DATA_KEY = 'Additional Data' # If there are multiple terms, use a more general term
            if not ADDITIONAL_DATA_KEY in data:
               data[ADDITIONAL_DATA_KEY] = [value]
            else:
               data[ADDITIONAL_DATA_KEY] += [value]
      

      if self.graph == None:
         self.graph = timeseries.TimeSeries(title = "Aggregate Sentiment", data=data, yMin=0, yMax=1)

         if self.sliderManager != None:
            display(self.sliderManager.generateDisplayBox())
      else:
         self.graph.data = data
         self.graph.plotTimeSeries() # updates the graph

      return self.graph
