'''
Sets up the library by starting the NLP sever and initializing the graphing engine's date format.
'''

from pandas.plotting import register_matplotlib_converters

import finndex.sentiment.nlp as nlp

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"


nlp.startServer(nlp.STANFORD_NLP_TIMEOUT, nlp.STANFORD_NLP_PORT)
register_matplotlib_converters() # register MatPlotLib date converter
