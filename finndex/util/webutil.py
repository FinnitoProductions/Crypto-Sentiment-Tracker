from contextlib import closing

from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from requests import get
from requests.exceptions import RequestException


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

# Extracts the text from a CNN article with given URL, excluding the headline and any advertisements.
def getCNNText(url):
    htmlParser = parseHTML(url)
    
    text = ''

    for element in htmlParser.select('div'):
        if element.has_attr('class') and 'zn-body__paragraph' in element['class']: 
            text += element.text 
    text = text.replace('"', ' ')
    return text