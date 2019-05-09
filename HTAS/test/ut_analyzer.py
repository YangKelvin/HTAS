import unittest
from ..MyAnalyzer.analyzer import Analyzer


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()

    def tearDown(self):
        self.analyzer = None

    def test_read_ptt_json(self):
        self.text = self.analyzer.read_ptt_json(
            'HTAS/test/test_tmp/data-1.json')
        self.assertEqual('M.1557332400.A.08C', self.text['article_id'])
        self.assertEqual('Re: [爆卦] 台灣一定會被統一，因為經濟', self.text['article_title'])


if __name__ == '__main__':
    unittest.main()
