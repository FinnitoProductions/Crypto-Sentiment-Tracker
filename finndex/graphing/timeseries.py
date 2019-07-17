'''
Contains a TimeSeries class allowing for a set of historical data to be plotted over time.
'''

import datetime

import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt

from finndex.util import dateutil

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"


'''
Represents an easily modifiable time series. 

The data is provided in 'data', where each key (string) represents the type of value stored (like 'price' or 'sentiment')
and the corresponding value is an list of dictionaries where the key is date and the value is the corresponding value on that day.
Each list represents a single axis, thus all the data in a list will be plotted on the same axis. Up to 2 axes are supported.

dataDateFormat (string) represents the format of all the incoming x-values. graphDateFormat (string) represents the format in which the given
dates will be displayed on the x-axis. 
'''
class TimeSeries:
    def __init__(self, title, data, colors=['tab:red', 'tab:blue', 'tab:green'], dataDateFormat=dateutil.DESIRED_DATE_FORMAT, graphedDateFormat = None, yMin=None, yMax=None):
        self.title = title
        self.data = data
        self.dataDateFormat = dataDateFormat

        if graphedDateFormat == None:
            timeDifference = max(data[list(data.keys())[0]]) - min(data[list(data.keys())[0]])

            if timeDifference <= datetime.timedelta(days=30*6):
                graphedDateFormat = "%m-%d"
            elif timeDifference <= datetime.timedelta(days=30*12):
                graphedDateFormat = "%Y-%m"
            else:
                graphedDateFormat = "%Y"

        self.graphedDateFormat = graphedDateFormat
        self.yMin = yMin
        self.yMax = yMax
        self.colors=colors

        self.fig = None
        self.axes = []
        
        self.plotTimeSeries()
    
    '''
    Generates the graph using the data specified in the constructor, or, if already generated, updates it to a new data set.
    '''
    def plotTimeSeries(self):
        if self.fig == None: # generating the graph for the first time
            self.fig, baseAxis = plt.subplots()
            firstExecution = True
        else:
            baseAxis = self.axes[0]
            firstExecution = False
        
        for idx, (valueType, valDictList) in enumerate(self.data.items()):
            if not isinstance(valDictList, list):
                valDictList = [valDictList]

            if not firstExecution:
                desiredAxes = self.axes[idx]
            else:
                if idx == 0:
                    desiredAxes = baseAxis
                else:
                    desiredAxes = baseAxis.twinx()
                self.axes += [desiredAxes]
                
            
            desiredAxes.clear()

            desiredAxes.set_ylabel(valueType, color=self.colors[idx])

            for valDict in valDictList:
                dates = [date for date in valDict]
                values = [val for val in valDict.values()]

                formattedDates = []
                for date in dates:
                    if isinstance(date, str):
                        formattedDates += [datetime.datetime.strptime(date, self.dataDateFormat)]
                    elif isinstance(date, datetime.date):
                        formattedDates += [datetime.datetime.combine(date, datetime.time())]
                    else:
                        formattedDates += [date]
                    
                dates = matplotlib.dates.date2num(formattedDates)
                desiredAxes.plot(formattedDates, values, color = self.colors[idx])
            desiredAxes.set_title(self.title)
            desiredAxes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(self.graphedDateFormat))
            
            if self.yMin != None:
                desiredAxes.set_ylim(ymin=self.yMin)
            if self.yMax != None:
                desiredAxes.set_ylim(ymax=self.yMax)
            
        self.fig.tight_layout()
        plt.show()
