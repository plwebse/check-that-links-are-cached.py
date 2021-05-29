import sys
import getopt
import urllib.request
from bs4 import BeautifulSoup


class ParseHtmlForUrlsInATagsHrefAttributes:
    def __init__(self, html):
        self.urls = self.__remove_url_that_dont_start_with_http(
            self.__parse_all_a_tags_href_attr_values_from(html))

    def __parse_all_a_tags_href_attr_values_from(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return {link.get('href') for link in soup.find_all('a', href=True)}

    def __remove_url_that_dont_start_with_http(self, hrefs):
        return list(filter(lambda href: href.startswith('http'), hrefs))

    def get_parsed_urls(self):
        return self.urls


class Util:

    @staticmethod
    def intersection(dict, list):
        intersection = []
        for key in dict.keys():
            for list_item in list:
                if key.lower() == list_item.lower():
                    intersection.append(key)
        return intersection

    @staticmethod
    def get_list_of_values(dict, keys):
        return [dict[key] for key in keys]

    @staticmethod
    def exit_program():
        sys.exit(0)

    @staticmethod
    def str_to_bool(v):
        return str(v).lower() in ('yes', 'true', '1', 'y')
    
    @staticmethod
    def list_of_strip_strings(list_of_strings):
        return [v.strip() for v in list_of_strings.split(',')]


class HttpUtil:

    def __init__(self, urls):
        self.urls = urls

    def get_headers_for_urls(self, http_headers, times):
        for url in self.urls:
            for time in times:
                yield (url, self.get_headers_for_url(
                    self.get_http_response_from(url), http_headers), time+1)

    def get_html_from_urls(self):
        for url in self.urls:
            yield (url, self.get_html_from(self.get_http_response_from(url)))

    def get_headers_for_url(self, http_response, http_headers):
        if http_response is not None:
            headers_dict = http_response.headers
            intersection_keys = Util.intersection(
                headers_dict, http_headers)
            return (
                Util.get_list_of_values(headers_dict, intersection_keys),
                http_response.status
            )
        return ([], -1)

    def get_html_from(self, http_response):
        res = ''
        if http_response is not None:
            try:
                res = http_response.read()
            except Exception:
                res = ''
            except KeyboardInterrupt:
                Util.exit_program()
        return res

    def get_http_response_from(self, url):
        try:
            http_response = urllib.request.urlopen(url)
            return http_response
        except urllib.error.HTTPError as e:
            # e can be treated as a http.client.HTTPResponse object
            return e
        except Exception:
            return None
        except KeyboardInterrupt:
            Util.exit_program()


class ParseCommandlineOptionsOrReturnDefaults:
    def __init__(self, argv, default_http_headers, default_times, default_parse_html):
        self.argv = argv
        self.script_name = self.argv[0]
        self.url = None
        self.http_headers = default_http_headers
        self.times = range(default_times)
        self.parse_html = default_parse_html

        try:
            opts, _args = getopt.getopt(
                self.argv[1:],
                'u:t:h:p:',
                ['url=', 'times=', 'http-headers=', 'parse-html=']
            )
        except Exception as e:
            print('An error occured {0}'.format(str(e)))
            return
        for opt, arg_value in opts:
            if opt in ('-u', '--url'):
                self.url = arg_value
            elif opt in ('-t', '--times'):
                self.times = range(int(arg_value))
            elif opt in ('-h', '--http-headers'):
                self.http_headers = Util.list_of_strip_strings(arg_value)
            elif opt in ('-p', '--parse-html'):
                self.parse_html = Util.str_to_bool(arg_value)

    def get_url(self):
        return self.url

    def get_http_headers(self):
        return self.http_headers

    def get_times(self):
        return self.times

    def get_times_str(self):
        return str(len(self.times))

    def get_http_headers_str(self):
        return str(self.http_headers)

    def get_parse_html(self):
        return self.parse_html

    def get_script_name(self):
        return self.script_name


def print_response(url, count, status_code_and_list_of_headers):
    list_of_headers, status = status_code_and_list_of_headers
    str_of_headers = '\t'.join(map(str, list_of_headers))
    print('{0}\t{1}\t{2}\t{3}\t'.format(
        url, count, str(status), str_of_headers))


def get_urls_to_test(parse_html, url):
    if parse_html:
        urls = []
        for (url, html) in HttpUtil([url]).get_html_from_urls():
            urls.extend(ParseHtmlForUrlsInATagsHrefAttributes(
                html).get_parsed_urls())
        return urls
    else:
        return [url]


def main():
    values = ParseCommandlineOptionsOrReturnDefaults(
        sys.argv,
        ['cache-control', 'via', 'x-cache'],
        1,
        True
    )

    if(values.get_url() is None):
        print(
            'Usage python {0} -u https://github.com/plwebse/'.format(values.get_script_name()))
        return

    print('Checking headers {0} for all urls in html @ url:{1} {2} time(s) parsing href values {3}'.format(
        values.get_http_headers_str(),
        values.get_url(),
        values.get_times_str(),
        values.get_parse_html())
    )

    print_response('url', 'time(s)', (values.get_http_headers(), 'code'))

    urls = get_urls_to_test(values.get_parse_html(), values.get_url())

    try:
        for (url, headers, times) in HttpUtil(urls).get_headers_for_urls(values.get_http_headers(), values.get_times()):
            print_response(url, str(times), headers)
    except KeyboardInterrupt:
        Util.exit_program()


if __name__ == '__main__':
    main()
