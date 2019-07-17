'''
Uses MatPlotLib to display a gauge which plots a piece of data with a set minimum and maximum.
'''

import os
import sys

import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge

from finndex.util import mathutil

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

ARROW_TAIL_RADIUS = 0.015

# Determines the range of angles which represent each portion of a gauge with n items.
def degreeRange(n): 
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = (start + end)/2.0
    return np.c_[start, end], mid_points

# Rotates a piece of text by a given angle.
def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

'''
Represents a gauge with a set of labels and colors (formatted in hex) corresponding to each of those labels.
'''
class Gauge:
    def __init__(self, labels, colors, currentVal, minVal, maxVal, title='', displayGauge=True):
        self.labels = labels
        self.colors = colors
        self.currentVal = currentVal
        self.minVal = minVal
        self.maxVal = maxVal
        self.title = title
        
        self.gaugeGenerated = False

        self.fig = None
        self.ax = None
        
        if displayGauge:
            self.generateGauge()
        
        
    '''
    Creates and displays a gauge. Returns a tuple containing the generated figure, axes,
    and arrow.
    '''
    def generateGauge(self):
        if not self.gaugeGenerated:
            N = len(self.labels)

            if isinstance(self.colors, list): 
                self.colors = self.colors[::-1]

            """
            begins the plotting
            """

            self.fig, self.ax = plt.subplots()

            ang_range, mid_points = degreeRange(N)

            self.labels = self.labels[::-1]

            """
            plots the sectors and the arcs
            """
            patches = []
            for ang, c in zip(ang_range, self.colors): 
                # sectors
                patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
                # arcs
                patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))

            [self.ax.add_patch(p) for p in patches]


            """
            set the labels (e.g. 'LOW','MEDIUM',...)
            """

            for mid, lab in zip(mid_points, self.labels):
                AVG_STR_LENGTH = 12
                AVG_FONT_SIZE = 11
                MAX_FONT_SIZE = 30

                fontSize = min(AVG_STR_LENGTH / len(lab) * AVG_FONT_SIZE, MAX_FONT_SIZE) # create dynamic font size based on string length
                self.ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab,
                    horizontalalignment='center', verticalalignment='center', fontsize=fontSize,
                    fontweight='bold', rotation = rot_text(mid))

            """
            set the bottom banner and the title
            """
            r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
            self.ax.add_patch(r)

            self.ax.text(0, -0.05, self.title, horizontalalignment='center',
                verticalalignment='center', fontsize=22, fontweight='bold')

            #Plot the arrow based on given sentiment value.
            lowestAngle = ang_range[0][0]
            highestAngle = ang_range[-1][1]

            pos = mathutil.map(self.currentVal, self.minVal, self.maxVal, highestAngle, lowestAngle)

            self.arrow = self.ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)),
                        width=0.03, head_width=0.09, head_length=0.1, fc='k', ec='k')

            self.ax.add_patch(Circle((0, 0), radius=ARROW_TAIL_RADIUS, facecolor='k')) # make the arrow rounded at the tail

            """
            removes frame and ticks, and makes axis equal and tight
            """

            self.ax.set_frame_on(False)
            self.ax.axes.set_xticks([])
            self.ax.axes.set_yticks([])
            self.ax.axis('equal')

            plt.tight_layout()
            plt.show()
        else:
            self.arrow.remove()
            highestAngle = 180
            lowestAngle = 0
            pos = mathutil.map(self.currentVal, self.minVal, self.maxVal, highestAngle, lowestAngle)
            self.arrow = self.ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)),
                                                           width=0.03, head_width=0.09, head_length=0.1, fc='k', ec='k')
      
            self.fig.canvas.draw_idle()
        
        self.gaugeGenerated = True

        return (self.fig, self.ax, self.arrow)

# Generates a gauge with options "Low", "Medium", and "High".
def displayNeutralGauge(currentVal, minVal, maxVal, title, display=True):
    return Gauge(labels=["Low", "Medium", "High"], colors=['#c80000','#646400','#00c800'], currentVal=currentVal,
                 minVal=minVal, maxVal=maxVal, title=title, displayGauge=display)
