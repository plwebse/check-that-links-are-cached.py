import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup


class ParseHtmlForAllUrlsInATagsHrefAttributes:
    def __init__(self, html):
        self.urls = self.__remove_url_that_dont_start_with_http(
            self.__parse_all_a_tags_href_attr_values_from(html))

    def __parse_all_a_tags_href_attr_values_from(self, html):
        hrefs = set()
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            hrefs.add(link.get('href'))
        return hrefs

    def __remove_url_that_dont_start_with_http(self, hrefs):
        urls = []
        for href in hrefs:
            if href.startswith('http'):
                urls.append(href)
        return urls

    def getParsedUrls(self):
        return self.urls


class HttpUtil:

    @staticmethod
    def get_headers_for_url(url, http_headers):
        output = url
        http_response = HttpUtil.__open_url(url)
        if http_response is None:
            return output + "\t0"
        output += "\t" + str(http_response.status)
        for http_header in http_headers:
            header = http_response.headers[http_header]
            if header is not None:
                output += "\t" + header
        return output

    @staticmethod
    def get_html_from(url):
        http_response = HttpUtil.__open_url(url)
        if http_response is None:
            return ""
        return http_response.read()

    @staticmethod
    def __open_url(url):
        try:
            http_response = urllib.request.urlopen(url)
            return http_response
        except urllib.error.HTTPError as e:
            # "e" can be treated as a http.client.HTTPResponse object
            return e
        except Exception as e:
            return None


class ParseValuesOrReturnDefaultValues:
    def __init__(self, defaultHttpHeaders, defaultNrOfTimes):
        self.url = None
        self.httpHeaders = defaultHttpHeaders
        self.nrOfTimes = range(defaultNrOfTimes)

        argv = sys.argv[1:]

        try:
            opts, _args = getopt.getopt(argv, "u:t:h:")
        except:
            print("An error occured")
        for opt, arg in opts:
            if opt in ['-u']:
                self.url = arg
            elif opt in ['-t']:
                self.nrOfTimes = range(int(arg))
            elif opt in ['-h']:
                self.httpHeaders = arg.split(',')

    def getUrl(self):
        return self.url

    def gethttpHeaders(self):
        return self.httpHeaders

    def getNrOfTimes(self):
        return self.nrOfTimes


def main():

    values = ParseValuesOrReturnDefaultValues(
        ["cache-control", "via", "x-cache"], 1)

    if(values.getUrl() is None):
        print("Usage python " + sys.argv[0] + " -u https://www.plweb.se/")
        return

    print("Checking headers " + str(values.gethttpHeaders()) +
          " for all urls in html @ url:" + values.getUrl() + " " + str(len(values.getNrOfTimes())) + " nr of times")

    html = HttpUtil.get_html_from(values.getUrl())
    urls = ParseHtmlForAllUrlsInATagsHrefAttributes(html).getParsedUrls()
    for url in urls:
        for _time in values.getNrOfTimes():
            print(HttpUtil.get_headers_for_url(url, values.gethttpHeaders()))


if __name__ == "__main__":
    main()
