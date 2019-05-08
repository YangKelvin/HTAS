import unittest
import json

from ..PttWebCrawler.crawler import PttWebCrawler as crawler


class TestCrawler(unittest.TestCase):
    def test_parse(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1557331202.A.58F.html'
        self.article_id = 'M.1557331202.A.58F'
        self.board = 'Gossiping'

        json_data = json.loads(crawler.parse(self.link))
        self.assertEqual(json_data['article_id'], self.article_id)
        self.assertEqual(json_data['borad'], self.borad)
