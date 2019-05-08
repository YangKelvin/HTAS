import unittest
import json

from ..PttWebCrawler.crawler import PttWebCrawler as crawler


class TestCrawler(unittest.TestCase):
    def test_parse_failed(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/failure.html'
        self.board = 'Gossiping'
        self.article_id = 'failure'

        crawler_data = crawler.parse(self.link, self.article_id, self.board)
        json_data = json.loads(crawler_data)  # str to dict
        self.assertEqual('invalid url', json_data['error'])

    def test_parse(self):
        # self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1557332400.A.08C.html'
        self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1554562631.A.37E.html'
        self.board = 'Gossiping'
        self.article_id = 'M.1557332400.A.08C'

        crawler_data = crawler.parse(self.link, self.article_id, self.board)
        json_data = json.loads(crawler_data)  # str to dict
        self.assertEqual(
            'https://www.ptt.cc/bbs/Gossiping/M.1554562631.A.37E.html', json_data['url'])
        self.assertEqual('Gossiping', json_data['board'])
        self.assertEqual('M.1557332400.A.08C', json_data['article_id'])
        self.assertEqual('Re: [爆卦] 台灣一定會被統一，因為經濟', json_data['article_title'])
        self.assertEqual('linwuno ()', json_data['author'])
        self.assertEqual('Sat Apr  6 22:57:09 2019', json_data['date'])
        self.assertEqual('5', str(json_data['message_count']['all']))

    def test_store(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1554562631.A.37E.html'
        self.board = 'Gossiping'
        self.article_id = 'M.1557332400.A.08C'

        crawler_data = crawler.parse(self.link, self.article_id, self.board)

        self.file_name  = './HTAS/test/test_tmp/filename.json'
        crawler.store(self.file_name, crawler_data, 'w')

    def test_parse_articles(self):
        a = crawler()
        print('parse_article: %s' %(a.parse_articles(39278, 39278, 'Gossiping')))

if __name__ == '__main__':
    unittest.main()
