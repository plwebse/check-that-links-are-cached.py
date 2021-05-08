import sys
import urllib.request
from bs4 import BeautifulSoup

def parseATagsAndReturnHrefAttrFrom(html):
    hrefs = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('http'):
            hrefs.append(href)
    return hrefs

def printHeadersForUrl(url, printHeaders):
    output = url    
    innerUrl = openUrl(url)
    if(innerUrl != None):
        output +=  "\t" + str(innerUrl.status)
        for printHeader in printHeaders:
            header = innerUrl.headers[printHeader]        
            if(header != None):
                output +=  "\t" + header
    print(output)
        

def getHtmlFrom(url):
    url = openUrl(url)
    if(url != None):    
        return url.read()
    return ""

def openUrl(url):    
    try:
        url = urllib.request.urlopen(url)
        return url
    except urllib.error.HTTPError as e:
        # "e" can be treated as a http.client.HTTPResponse object
        return e
    except Exception as e:
        return None

headers = ["cache-control", "via", "x-cache"]
html = getHtmlFrom(sys.argv[1])
urls = parseATagsAndReturnHrefAttrFrom(html)
for url in urls:
    printHeadersForUrl(url, headers)