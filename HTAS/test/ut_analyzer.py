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

    def test_read_ptt_json2(self):
        self.text = self.analyzer.read_ptt_json(
            'HTAS/test/test_tmp/Gossiping-39001-39100.json')
        self.assertEqual('M.1557139088.A.5B2',
                         self.text['articles'][0]['article_id'])
        self.assertEqual('[問卦] 超人何時再起', self.text['articles']
                         [0]['article_title'])

    def test_analysis_article(self):
        article = self.analyzer.read_ptt_json(
            'HTAS/test/test_tmp/Gossiping-39001-39100.json')
        article = article['articles'][0]
        # print(article)
        title = article['article_title']
        content = article['content']

        title_cut = self.analyzer.cut(title)
        print('/'.join(title))
        # for text in title_cut:
        #     print('text: %s' % (text))

    def test_add_word_test(self):
        sentence = '人渣文本好好看喔'
        title_cut = self.analyzer.cut(sentence)
        for text in title_cut:
            print('text: %s' % (text))


    def test_analysis_articles(self):
        data = self.analyzer.read_ptt_json('HTAS/test/test_tmp/Gossiping-39001-39100.json')
        tmp_df, tmp_title, tmp_contents, tmp_total_lens = self.analyzer.analysis_articles(data)
        print(tmp_df)


if __name__ == '__main__':
    unittest.main()
