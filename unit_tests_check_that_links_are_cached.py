import unittest
from check_that_links_are_cached import ParseHtmlForAllUrlsInATagsHrefAttributes, HttpUtil
from unittest.mock import MagicMock


class TestParseHtmlForAllUrlsInATagsHrefAttributes(unittest.TestCase):

    def test_empty_result(self):
        html = "test"
        exepected = []
        actual = self.__phfauiatagsha(html).getParsedUrls()
        self.assertEqual(exepected, actual)

    def test_some_result(self):
        html = '<html><head></head><body><a href="https://www.plweb.se/"> </body></html>'
        exepected = ['https://www.plweb.se/']
        actual = self.__phfauiatagsha(html).getParsedUrls()
        self.assertEqual(exepected, actual)

    def test_no_ancor_result(self):
        html = '<html><head></head><body><a href="https://www.plweb.se/"><a href="#test"> </body></html>'
        exepected = ['https://www.plweb.se/']
        actual = self.__phfauiatagsha(html).getParsedUrls()
        self.assertEqual(exepected, actual)

    def test_no_duplicate_result(self):
        html = '<html><head></head><body><a href="https://www.plweb.se/"><a href="#test"><a href="https://www.plweb.se/"></body></html>'
        exepected = ['https://www.plweb.se/']
        actual = self.__phfauiatagsha(html).getParsedUrls()
        self.assertEqual(exepected, actual)

    def test_http_util_get_no_headers_for_url(self):
        http_response = None
        exepected = "test\t0"
        actual = HttpUtil.get_headers_for_url("test", http_response, ['via'])
        self.assertEqual(exepected, actual)

    def test_http_util_get_other_headers_for_url(self):
        http_response = MagicMock()
        headers = {}
        headers['cache-control'] = 'max-age=2592000'
        http_response.headers = headers
        http_response.status = 200
        exepected = "test\t200"
        actual = HttpUtil.get_headers_for_url("test", http_response, ['via'])
        self.assertEqual(exepected, actual)

    def test_http_util_get_matching_headers_for_url(self):
        http_response = MagicMock()
        headers = {}
        headers['via'] = 'max-age=2592000'
        http_response.headers = headers
        http_response.status = 200
        exepected = "test\t200\tmax-age=2592000"
        actual = HttpUtil.get_headers_for_url("test", http_response, ['via'])
        self.assertEqual(exepected, actual)

    def __phfauiatagsha(self, html):
        return ParseHtmlForAllUrlsInATagsHrefAttributes(html)


if __name__ == '__main__':
    unittest.main()
