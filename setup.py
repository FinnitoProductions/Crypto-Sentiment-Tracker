from setuptools import setup

VERSION = '0.6.0'

setup(name='finndex',
      version=VERSION,
      description='A useful tool for crypto analysts providing several metrics on various cryptocurrencies.',
      url='https://github.com/FinnitoProductions/Crypto-Sentiment-Tracker',
      download_url='https://github.com/FinnitoProductions/finndex/archive/v{}-alpha.tar.gz'.format(VERSION),
      author='Finn Frankis',
      author_email='finn@teachmy.com',
      license='MIT',
      packages=['finndex', 'finndex.util', 'finndex.sentiment', 'finndex.fundamental', 'finndex.aggregate'],
      install_requires=['beautifulsoup4',
                        'ipykernel',
                        'ipython',
                        'ipywidgets',
                        'matplotlib',
                        'numpy',
                        'pandas',
                        'plotly',
                        'pycorenlp',
                        'pytrends',
                        'requests',
                        'scipy',
                        'stanfordnlp'],
      zip_safe=False)
