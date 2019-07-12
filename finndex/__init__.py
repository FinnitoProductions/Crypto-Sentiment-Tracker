from pandas.plotting import register_matplotlib_converters

import finndex.sentiment.nlp as nlp

nlp.startServer(nlp.STANFORD_NLP_TIMEOUT, nlp.STANFORD_NLP_PORT)
register_matplotlib_converters() # register MatPlotLib date converter
