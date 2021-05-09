import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup


def parse_all_a_tags_href_attr_values_from(html):
    hrefs = set()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        hrefs.add(link.get('href'))
    return hrefs


def remove_url_that_dont_start_with_http(hrefs):
    urls = []
    for href in hrefs:
        if href.startswith('http'):
            urls.append(href)
    return urls


def get_headers_for_url(url, print_http_headers):
    output = url
    http_response = open_url(url)
    if http_response is None:
        return output + "\t0"
    output += "\t" + str(http_response.status)
    for print_http_header in print_http_headers:
        header = http_response.headers[print_http_header]
        if header is not None:
            output += "\t" + header
    return output


def get_html_from(url):
    http_response = open_url(url)
    if http_response is None:
        return ""
    return http_response.read()


def open_url(url):
    try:
        http_response = urllib.request.urlopen(url)
        return http_response
    except urllib.error.HTTPError as e:
        # "e" can be treated as a http.client.HTTPResponse object
        return e
    except Exception as e:
        return None


def main():
    argv = sys.argv[1:]
    url = None

    # default values
    times = range(1)
    list_http_headers = ["cache-control", "via", "x-cache"]

    try:
        opts, _args = getopt.getopt(argv, "u:t:h:")
    except:
        print("An error occured")
    for opt, arg in opts:
        if opt in ['-u']:
            url = arg
        elif opt in ['-t']:
            times = range(int(arg))
        elif opt in ['-h']:
            list_http_headers = arg.split(',')

    if(url is None):
        print("Usage python " + sys.argv[0] + " -u https://www.plweb.se/")
        return

    print("Checking headers " + str(list_http_headers) +
          " for all urls in html @ url:" + url + " " + str(len(times)) + " times")

    html = get_html_from(url)
    hrefs = parse_all_a_tags_href_attr_values_from(html)
    urls = remove_url_that_dont_start_with_http(hrefs)
    for url in urls:
        for _time in times:
            print(get_headers_for_url(url, list_http_headers))


if __name__ == "__main__":
    main()
