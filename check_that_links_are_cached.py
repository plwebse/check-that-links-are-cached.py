import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup


class ParseHtmlForUrlsInATagsHrefAttributes:
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
        try:
            return http_response.read()
        except Exception:
            return ""
        except KeyboardInterrupt:
            exit_program()

    @staticmethod
    def get_http_response_from(url):
        try:
            http_response = urllib.request.urlopen(url)
            return http_response
        except urllib.error.HTTPError as e:
            # "e" can be treated as a http.client.HTTPResponse object
            return e
        except Exception:
            return None
        except KeyboardInterrupt:
            exit_program()


class ParseValuesOrReturnDefaultValues:
    def __init__(self, argv, defaultHttpHeaders, defaultTimes, defaultParseHtml):
        self.argv = argv
        self.scriptName = self.argv[0]
        self.url = None
        self.httpHeaders = defaultHttpHeaders
        self.times = range(defaultTimes)
        self.parseHtml = defaultParseHtml

        try:
            opts, _args = getopt.getopt(
                self.argv[1:], "u:t:h:p:", ['url=', 'times=', 'http-headers=', 'parse-html='])
        except Exception as e:
            print("An error occured {0}".format(str(e)))
            return
        for opt, arg_value in opts:
            if opt in ('-u', '--url'):
                self.url = arg_value
            elif opt in ('-t', '--times'):
                self.times = range(int(arg_value))
            elif opt in ('-h', '--http-headers'):
                self.httpHeaders = [v.strip() for v in arg_value.split(',')]
            elif opt in ('-p', '--parse-html'):
                self.parseHtml = self.__str2bool(arg_value)

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

    def getScriptName(self):
        return self.scriptName

    def __str2bool(self, v):
        return str(v).lower() in ("yes", "true", "1", "y")


def exit_program():
    sys.exit(0)


def main():    
    values = ParseValuesOrReturnDefaultValues(
        sys.argv,
        ["cache-control", "via", "x-cache"],
        1,
        True
    )

    if(values.getUrl() is None):
        print(
            "Usage python {0} -u https://github.com/plwebse/".format(values.getScriptName()))
        return

    print("Checking headers {0} for all urls in html @ url:{1} {2} time(s) parsing href values {3}".format(
        values.gethttpHeadersStr(),
        values.getUrl(),
        values.getTimesStr(),
        values.getParseHtml())
    )

    urls = [values.getUrl()]
    if values.getParseHtml():
        html = HttpUtil.get_html_from(
            HttpUtil.get_http_response_from(values.getUrl()))
        urls = ParseHtmlForUrlsInATagsHrefAttributes(html).getParsedUrls()

    tableHeader = 'url'
    tableHeader += '\tcode'
    for header in values.gethttpHeaders():
        tableHeader += '\t' + header

    print(tableHeader)
    try:
        for url in urls:
            for _time in values.getTimes():
                print(HttpUtil.get_headers_for_url(
                    url, HttpUtil.get_http_response_from(url), values.gethttpHeaders()))
    except KeyboardInterrupt:
        exit_program()


if __name__ == "__main__":
    main()
