'''
Sets up the library by starting the NLP sever and initializing the graphing engine's date format.
'''

from finndex.api import datadict
from finndex.sentiment import nlp
import pandas as pd
from pandas.plotting import register_matplotlib_converters

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"


nlp.startServer(nlp.STANFORD_NLP_TIMEOUT, nlp.STANFORD_NLP_PORT)
register_matplotlib_converters() # register MatPlotLib date converter
pd.options.plotting.backend = "plotly"

a = datadict.setupApi('__main__')
