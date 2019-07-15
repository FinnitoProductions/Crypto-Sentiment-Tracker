import datetime
import functools
from enum import Enum

import ipywidgets as widgets
import numpy as np
from IPython.display import display

from finndex.aggregate import sliders
from finndex.fundamental import coinmetrics
from finndex.graphing import timeseries
from finndex.sentiment import fearandgreed, trends
from finndex.util import dateutil, mathutil


'''
Represents a piece of data with several values over time. 'values' is a dictionary with the date as the key
and the corresponding value on that date as the value. 'slider' is the slider modifying the weight of this reading.
'''
class HistoricalDataReading:
    def __init__(self, name, values, slider):
        self.name = name
        self.values = values
        self.slider = slider

class HistoricalMetricType(Enum):
   FEAR_AND_GREED = functools.partial(fearandgreed.getFearAndGreedDateRange)
   TRENDS = functools.partial(trends.getTrendsDateRange)
   BLOCK_COUNT = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.BLOCK_COUNT)
   TRANSACTION_CNT = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.TRANSACTION_CNT)
   DAILY_ADDRESSES = functools.partial(coinmetrics.getCoinMetricsDateRange, coinmetrics.CoinMetricsData.DAILY_ADDRESSES)

class HistoricalSentimentManager:
   def __init__(self, weightedKeywordsList, startDate = datetime.datetime.now() - datetime.timedelta(weeks=4), endDate = datetime.datetime.now(), weights = None, 
                unweightedKeywordsList = []):
      self.dataVals = []
      slidersList = []

      for idx, keyword in enumerate(weightedKeywordsList):
         dataReading = HistoricalDataReading(name=str(keyword), values=keyword.value(startDate=startDate, endDate=endDate), 
                                   slider=sliders.Slider(str(keyword), widgets.FloatSlider(min=0.0, max=sliders.MAX_VAL, 
                                                                                           step=sliders.STEP, 
                                                                                           value=weights[idx] if weights != None else 0.0)))
         self.dataVals += [dataReading]
         slidersList += [dataReading.slider]

      if weights == None:
         self.sliderManager = sliders.SliderManager(self.displayGraph, slidersList)
      else:
         self.sliderManager = None

      self.startDate = startDate
      self.endDate = endDate

      self.graph = None


   '''
   Computes the weighted historical sentiment with the date as the key and the historical sentiment on that date as the value.
   '''
   def getHistoricalSentiment(self):
      sentimentByDate = {}
   
      for date in dateutil.dateRange(self.startDate, self.endDate):
         sentimentByDate[date] = []

         for historicalReading in self.dataVals:
            convertedDate = date.strftime(dateutil.DESIRED_DATE_FORMAT)
            sentimentByDate[date] += [(historicalReading.values[convertedDate]
                                       if convertedDate in historicalReading.values
                                      else -float('inf'), historicalReading.slider.getReading())] # add tuple with value (-infinity if nothing provided) and weight

         values = sentimentByDate[date]
         values.sort() # place all values with -infinity first so they can be dealt with

         for i, (value, weight) in enumerate(values):
            if value == -float('inf'): # no value provided
               if i != len(values) - 1:
                  weightPerElement = weight / (len(values) - i - 1)
               values[i] = (0.0, 1.0)

               for j, val in enumerate(values[i+1:], start = i+1):
                  values[j] = (values[j][0], values[j][1] + weightPerElement)

         
         sentimentByDate[date] = 0
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

      if self.graph == None:
         self.graph = timeseries.TimeSeries(title = "Aggregate Sentiment", data=data, graphedDateFormat="%Y", yMin=0, yMax=1)

         if self.sliderManager != None:
            display(self.sliderManager.generateDisplayBox())
      else:
         self.graph.data = data
         self.graph.plotTimeSeries()

      return self.graph

   # valueDict = {'fearAndGreed': HistoricalDataReading(values=getAllFearAndGreed(), 
   #                               slider=Slider(obj=widgets.FloatSlider(min=0.0, max=MAX_VAL, step=STEP, value=0.0),
   #                                                       editedManually=False,
   #                                                       description="Fear and Greed Weight"), minVal = MIN_FEAR_AND_GREED,
   #                                                 maxVal = MAX_FEAR_AND_GREED),
   #             'trends': HistoricalDataReading(values=getTrendsDataByDay("Bitcoin", datetime.datetime.now() - datetime.timedelta(days=35), datetime.datetime.now()), 
   #                               slider=Slider(obj=widgets.FloatSlider(min=0.0, max=MAX_VAL, step=STEP, value=0.0),
   #                                                       editedManually=False,
   #                                                       description="Trends Weight")),
   #             'addresses': HistoricalDataReading(values=getAllCoinMetricsData(CoinMetricsData.DAILY_ADDRESSES),
   #                                              slider=Slider(obj=widgets.FloatSlider(min=0.0, max=MAX_VAL, step=STEP, value=0.0),
   #                                                       editedManually=False,
   #                                                       description="Addresses Weight")),
   #             'transactions': HistoricalDataReading(values=getAllCoinMetricsData(CoinMetricsData.TRANSACTION_CNT),
   #                                              slider=Slider(obj=widgets.FloatSlider(min=0.0, max=MAX_VAL, step=STEP, value=0.0),
   #                                                       editedManually=False,
   #                                                       description="Transaction Weight"))}


   # earliestDate, latestDate = getDateRange(valueDict)
   # priceData = getAllCoinMetricsData(CoinMetricsData.PRICE_USD)

   # newPriceData = {}
   # # Ensures that only elements within the computed date range can be added.
   # for date, val in priceData.items():
   #    convertedDate = datetime.datetime.strptime(date, DESIRED_DATE_FORMAT) 
   #    if convertedDate >= earliestDate and convertedDate <= latestDate:
   #       newPriceData[date] = val 

   # for valueType, data in valueDict.items():
   #    data.slider.initSliderValue(len(valueDict))

   # graph = updateGraph(valueDict, Price=newPriceData)

   # sliderManager = SliderManager(editedFunction=updateGraph, valueDict=valueDict, displayedObj=graph)
   # for valueType, data in valueDict.items():
   #    sliderManager.addSlider(name=valueType, slider=data.slider)

   # display(generateDisplayBox([data.slider for key, data in valueDict.items()]))
