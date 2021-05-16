import unittest
from check_that_links_are_cached import ParseHtmlForUrlsInATagsHrefAttributes, HttpUtil, ParseCommandlineOptionsOrReturnDefaults
from unittest.mock import MagicMock


class TestParseHtmlForUrlsInATagsHrefAttributes(unittest.TestCase):

    def test_empty_result(self):
        html = "test"
        exepected = []
        actual = self.__parse_html(html).get_parsed_urls()
        self.assertEqual(exepected, actual)

    def test_some_result(self):
        html = '<html><head></head><body><a href="https://www.plweb.se/"></body></html>'
        exepected = ['https://www.plweb.se/']
        actual = self.__parse_html(html).get_parsed_urls()
        self.assertEqual(exepected, actual)

    def test_no_ancor_result(self):
        html = '<html><head></head><body><a href="https://www.plweb.se/"><a href="#test"></body></html>'
        exepected = ['https://www.plweb.se/']
        actual = self.__parse_html(html).get_parsed_urls()
        self.assertEqual(exepected, actual)

    def test_no_duplicate_result(self):
        html = '<html><head></head><body><a href="https://www.plweb.se/"><a href="#test"><a href="https://www.plweb.se/"></body></html>'
        exepected = ['https://www.plweb.se/']
        actual = self.__parse_html(html).get_parsed_urls()
        self.assertEqual(exepected, actual)

    def test_http_util_get_no_headers_for_url(self):
        http_response = None
        exepected = {'status': -1, 'headers': []}
        actual = HttpUtil.get_headers_for_url(http_response, ['via'])
        self.assertEqual(exepected, actual)

    def test_http_util_get_other_headers_for_url(self):
        http_response = MagicMock()
        headers = {}
        headers['cache-control'] = 'max-age=2592000'
        http_response.headers = headers
        http_response.status = 200
        exepected = {'status': 200, 'headers': []}
        actual = HttpUtil.get_headers_for_url(http_response, ['via'])
        self.assertEqual(exepected, actual)

    def test_http_util_get_matching_headers_for_url(self):
        http_response = MagicMock()
        headers = {}
        headers['via'] = 'max-age=2592000'
        http_response.headers = headers
        http_response.status = 200
        exepected = {'status': 200, 'headers': ['max-age=2592000']}
        actual = HttpUtil.get_headers_for_url(http_response, ['via'])
        self.assertEqual(exepected, actual)

    def test_parse_values_or_return_default_values_bare_minimum(self):
        expected_script_name = 'scriptname'
        expected_url = None
        expected_http_headers = ['via']
        expected_times = 1
        expected_parse_html = True
        args = [expected_script_name]
        values = ParseCommandlineOptionsOrReturnDefaults(
            args, ['via'], 1, True)
        self.assertEqual(expected_script_name, values.get_script_name())
        self.assertEqual(expected_url, values.get_url())
        self.assertEqual(expected_http_headers, values.get_http_headers())
        self.assertEqual(expected_times, len(values.get_times()))
        self.assertEqual(expected_parse_html, values.get_parse_html())

    def test_parse_values_or_return_default_values_sort_names(self):
        expected_script_name = 'scriptname'
        expected_url = 'https://plweb.se/'
        expected_times = 3
        input_http_headers = 'max-age, private, must-revalidate'
        expected_http_headers = ['max-age', 'private', 'must-revalidate']
        input_parse_html = 'false'
        expected_parse_html = False
        args = [expected_script_name, '-u', expected_url, '-t', expected_times,
                '-h', input_http_headers, '-p', input_parse_html]
        values = ParseCommandlineOptionsOrReturnDefaults(args, [], 1, True)
        self.assertEqual(expected_script_name, values.get_script_name())
        self.assertEqual(expected_url, values.get_url())
        self.assertEqual(expected_times, len(values.get_times()))
        self.assertEqual(expected_http_headers, values.get_http_headers())
        self.assertEqual(expected_parse_html, values.get_parse_html())

    def test_parse_values_or_return_default_values_long_names(self):
        expected_script_name = 'scriptname'
        expected_url = 'https://plweb.se/'
        expected_times = 3
        input_http_headers = 'max-age, private, must-revalidate'
        expected_http_headers = ['max-age', 'private', 'must-revalidate']
        input_parse_html = 'false'
        expected_parse_html = False
        args = [expected_script_name, '--url='+expected_url, '--times='+str(expected_times),
                '--http-headers=' + input_http_headers, '--parse-html='+input_parse_html]
        values = ParseCommandlineOptionsOrReturnDefaults(args, [], 1, True)
        self.assertEqual(expected_script_name, values.get_script_name())
        self.assertEqual(expected_url, values.get_url())
        self.assertEqual(expected_times, len(values.get_times()))
        self.assertEqual(expected_http_headers, values.get_http_headers())
        self.assertEqual(expected_parse_html, values.get_parse_html())

    def test_parse_values_or_return_default_values_long_names(self):
        expected_script_name = 'scriptname'
        expected_url = 'https://plweb.se/'
        expected_times = 3
        input_http_headers = 'max-age, private, must-revalidate'
        expected_http_headers = ['max-age', 'private', 'must-revalidate']
        input_parse_html = 'false'
        expected_parse_html = False
        args = [expected_script_name, '--url='+expected_url, '--times='+str(expected_times),
                '--http-headers=' + input_http_headers, '--parse-html='+input_parse_html]
        values = ParseCommandlineOptionsOrReturnDefaults(args, [], 1, True)
        self.assertEqual(expected_script_name, values.get_script_name())
        self.assertEqual(expected_url, values.get_url())
        self.assertEqual(expected_times, len(values.get_times()))
        self.assertEqual(expected_http_headers, values.get_http_headers())
        self.assertEqual(expected_parse_html, values.get_parse_html())

    def __parse_html(self, html):
        return ParseHtmlForUrlsInATagsHrefAttributes(html)


if __name__ == '__main__':
    unittest.main()
