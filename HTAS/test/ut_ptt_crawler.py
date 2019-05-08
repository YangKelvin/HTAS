import unittest
import json

from ..PttWebCrawler.crawler import PttWebCrawler as crawler


class TestCrawler(unittest.TestCase):
    def test_parse_failed(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/failure.html'
        crawler_data = crawler.parse(self.link)
        json_data = json.loads(crawler_data)  # str to dict
        self.assertEqual('invalid url', json_data['error'])


if __name__ == '__main__':
    unittest.main()
