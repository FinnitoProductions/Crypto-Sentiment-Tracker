from setuptools import setup

setup(name='finndex',
      version='0.1',
      description='A useful tool for crypto analysts providing several metrics on various cryptocurrencies.',
      url='https://github.com/FinnitoProductions/Crypto-Sentiment-Tracker',
      download_url='https://github.com/FinnitoProductions/finndex/archive/v0.1-alpha.tar.gz',
      author='Finn Frankis',
      author_email='finn@teachmy.com',
      license='MIT',
      packages=['finndex'],
      install_requires=['beautifulsoup4',
                        'ipykernel',
                        'ipython',
                        'ipywidgets',
                        'matplotlib',
                        'numpy',
                        'pandas',
                        'pycorenlp',
                        'pytrends',
                        'requests',
                        'stanfordnlp'],
      zip_safe=False)
