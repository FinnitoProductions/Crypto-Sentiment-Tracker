'''
Provides several utility functions for extracting data from websites (including HTML pages as well as JSON files from APIs).
'''
from contextlib import closing

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"


# Extracts the content located at any URL.
def getPageContent(url):
    try: 
        with closing(get(url, stream = True)) as page:
            return page.content.decode("utf-8")
    except RequestException as e:
        print(e)
        return
    
# Parses a string representing HTML, returning the parsed result for convenient iteration.
def parseHTML(url):
    return BeautifulSoup(getPageContent(url), 'html.parser')

def get_cnn_text(url):
   '''
   ' Retrieves the body of a given CNN article, excluding the headline and any advertisements.
   '
   ' url (string): the URL where the specific article is located
   '''
   htmlParser = parseHTML(url)
   
   text = ''

   for element in htmlParser.select('div'):
      if element.has_attr('class') and 'zn-body__paragraph' in element['class']: 
         text += element.text 
   text = text.replace('"', ' ')
   return text

def get_coin_desk_text(url):
   '''
   ' Retrieves the body of a given CoinDesk article.
   '
   ' url (string): the URL where the specific article is located
   '''
   parser = parseHTML(url)

   text = ""
   for element in parser.findAll("div", {"class": "article-pharagraph"}):
      text += element.text
      
   return text

def get_business_insider_text(url):
   '''
   ' Retrieves the body of a given Business Insider article.
   '
   ' url (string): the URL where the specific article is located
   '''
   parser = parseHTML(url)
   text = ""
   paragraphs = parser.findAll("p", {"class": ""})

   for element in paragraphs:
      if element.img == None:
         text += element.text

   return text.replace("\n", "").replace("\xa0", " ")