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
    def get_headers_for_url(url, http_response, http_headers):
        output = url
        if http_response is None:
            return output + "\t0"
        output += "\t" + str(http_response.status)
        for http_header in http_headers:
            header = http_response.headers.get(http_header, None)
            if header is not None:
                output += "\t" + header
        return output

    @staticmethod
    def get_html_from(http_response):
        if http_response is None:
            return ""
        return http_response.read()

    @staticmethod
    def get_http_response_from(url):
        try:
            http_response = urllib.request.urlopen(url)
            return http_response
        except urllib.error.HTTPError as e:
            # "e" can be treated as a http.client.HTTPResponse object
            return e
        except Exception as e:
            return None


class ParseValuesOrReturnDefaultValues:
    def __init__(self, defaultHttpHeaders, defaultTimes, defaultParseHtml):
        self.url = None
        self.httpHeaders = defaultHttpHeaders
        self.times = range(defaultTimes)
        self.parseHtml = defaultParseHtml

        argv = sys.argv[1:]

        try:
            opts, _args = getopt.getopt(argv, "u:t:h:p:")
        except:
            print("An error occured")
        for opt, arg in opts:
            if opt in ['-u']:
                self.url = arg
            elif opt in ['-t']:
                self.times = range(int(arg))
            elif opt in ['-h']:
                self.httpHeaders = arg.split(',')
            elif opt in ['-p']:
                self.parseHtml = self.__str2bool(arg)

    def getUrl(self):
        return self.url

    def gethttpHeaders(self):
        return self.httpHeaders

    def getTimes(self):
        return self.times

    def getTimesStr(self):
        return str(len(self.times))

    def gethttpHeadersStr(self):
        return str(self.httpHeaders)

    def getParseHtml(self):
        return self.parseHtml

    def __str2bool(self, v):
        return str(v).lower() in ("yes", "true", "1", "y")


def main():
    scriptName = sys.argv[0]
    values = ParseValuesOrReturnDefaultValues(
        ["cache-control", "via", "x-cache"], 1, True)

    if(values.getUrl() is None):
        print(
            "Usage python {0} -u https://github.com/plwebse/".format(scriptName))
        return

    print("Checking headers {0} for all urls in html @ url:{1} {2} time(s) parsing href values {3}".format(
        values.gethttpHeadersStr(),
        values.getUrl(),
        values.getTimesStr(),
        values.getParseHtml())
    )

    urls = [values.getUrl()]
    if values.getParseHtml():
        html = HttpUtil.get_html_from(HttpUtil.get_http_response_from(values.getUrl()))
        urls = ParseHtmlForAllUrlsInATagsHrefAttributes(html).getParsedUrls()

    tableHeader = 'url'
    tableHeader += '\tcode'
    for header in values.gethttpHeaders():
        tableHeader += '\t' + header

    print(tableHeader)

    for url in urls:
        for _time in values.getTimes():
            print(HttpUtil.get_headers_for_url(
                url, HttpUtil.get_http_response_from(url), values.gethttpHeaders()))


if __name__ == "__main__":
    main()
