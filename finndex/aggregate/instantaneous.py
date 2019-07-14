import datetime
from enum import Enum

import ipywidgets as widgets
import numpy as np
from IPython.display import display

from finndex.aggregate import sliders
from finndex.graphing import gauge
from finndex.sentiment import fearandgreed, nlp, trends
from finndex.util import dateutil, mathutil, webutil


# Represents a static data reading represented by a single gauge and weighted by a slider.
class DataReading:
   def __init__(self, name, gauge, slider):
      self.name = name
      self.gauge = gauge
      self.slider = slider

class StaticMetricType(Enum):
   FEAR_AND_GREED = fearandgreed.displayFearAndGreedDate
   TRENDS = trends.displayTrendsDate

class InstantaneousSentimentManager:
   def __init__(self, keywordsList, date=datetime.datetime.now(), weights=None, displayIntermediates=False):
      self.dataVals = []
      slidersList = []

      for idx, keyword in enumerate(keywordsList):
         dataReading = DataReading(name=str(keyword), gauge=keyword(date=date, display=displayIntermediates), 
                                   slider=sliders.Slider(str(keyword), widgets.FloatSlider(min=0.0, max=sliders.MAX_VAL, 
                                                                                           step=sliders.STEP, 
                                                                                           value=weights[idx] if weights != None else 0.0)))
         self.dataVals += [dataReading]
         slidersList += [dataReading.slider]



      self.gauge = None


      if weights == None:
         self.sliderManager = sliders.SliderManager(self.updateGauge, slidersList)
      else:
         self.sliderManager = None

   def getDataReading(self, name):
      return [reading for reading in self.dataVals if reading.name == name][0]

   '''
   Computes the aggregate sentiment based on a dictionary of values where a given value corresponds to a dictionary containing 
   the value's weight (with key 'weight'), the minimum possible value the value can take on (with key 'minVal'), and the 
   maximum possible value the value can take on (with key 'maxVal').

   Returns a tuple containing (in the following order) the aggregate value, the minimum value for this aggregate, 
   and the maximum value for this aggregate.
   '''
   def computeAggregateSentiment(self):
      aggregateVal = 0
      minVal = 0
      maxVal = 1

      for data in self.dataVals:
         weight = data.slider.getReading()
         scaledValue = mathutil.map(data.gauge.currentVal, data.gauge.minVal, data.gauge.maxVal, 0, 1)
         aggregateVal += scaledValue * weight
         
      return (aggregateVal, minVal, maxVal)

   '''
   Displays the aggregate sentiment meter based on a dictionary of values. See computeAggregateSentiment for a complete
   description of this parameter.
   '''
   def displayGauge(self):
      aggregateVal, minVal, maxVal = self.computeAggregateSentiment()
      
      self.gauge = gauge.Gauge(labels=['—','0','+'], 
                  colors=['#c80000', '#646400', '#00c800'], currentVal=aggregateVal, 
                  minVal = minVal,
                  maxVal = maxVal, title='Aggregate Sentiment')

      if self.sliderManager != None:
         display(self.sliderManager.generateDisplayBox())

      return self.gauge

   # Updates the corresponding gauge given a new set of values and the existing gauge.
   def updateGauge(self):
      self.gauge.currentVal, self.gauge.minVal, self.gauge.maxVal = self.computeAggregateSentiment()
      self.gauge.generateGauge()

   # Retrieves the aggregate sentiment value as a float.
   def getReading(self):
      return self.computeAggregateSentiment()
