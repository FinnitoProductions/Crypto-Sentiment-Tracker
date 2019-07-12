import datetime

import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt


class TimeSeries:
    def __init__(self, fig=None, ax=None):
        self.fig = fig
        self.ax = ax

'''
Plots an easily modifiable time series. 

The data is provided in xyDict, where each key (string) represents the type of value stored (like 'price' or 'sentiment')
and the corresponding value is a dictionary containing two keys: 'x' and 'y'. 'x' points to a list of the x-values of all
the desired points (must be in a date format) and 'y' points to a list of the y-values of the desired points. The first key in the dictionary is
the only data that can be modified.

dateFormat (string) represents the format of all the incoming x-values. graphDateFormat (string) represents the format in which the given
dates will be displayed on the x-axis. 

If seeking to modify an existing graph, existingGraph represents the TimeSeries which was already produced by this function.
'''
def plotTimeSeries(xyDict, title="",dateFormat="%Y-%m-%dT%H:%M:%S.%fZ", graphDateFormat="%Y", existingGraph=None, 
                   yMin=None, yMax=None):
    if existingGraph == None:
        fig, ax = plt.subplots()
    else:
        fig, ax = existingGraph.fig, existingGraph.ax
    
    colors = ['tab:red', 'tab:blue', 'tab:green']
    i = 0
    for valueType, xyVals in xyDict.items():
        formattedDates = []
        for date in xyVals['x']:
            if not isinstance(date, datetime.datetime):
                formattedDates += [datetime.datetime.strptime(date, dateFormat)]
            else:
                formattedDates += [date]
            
        dates = matplotlib.dates.date2num(formattedDates)

        if i == 0:
            desiredAxes = ax
        else:
            desiredAxes = ax.twinx()
            
        desiredAxes.set_ylabel(valueType, color=colors[i])
        desiredAxes.plot(formattedDates, xyVals['y'], color = colors[i])
        desiredAxes.set_title(title)
        desiredAxes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(graphDateFormat))
        
        if yMin != None:
            ax.set_ylim(ymin=yMin)
        if yMax != None:
            ax.set_ylim(ymax=yMax)
            
        i += 1
    fig.tight_layout()
    plt.show()
    
    return TimeSeries(fig, ax)
