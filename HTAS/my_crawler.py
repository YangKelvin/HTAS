import datetime
from PttWebCrawler.crawler import PttWebCrawler as ptt_crawler

# 設定看板
BOARD = 'MobileComm'
# BOARD = 'Gossiping'

print('start my crawler...\n')

# 取得當前日期
TODAY = datetime.date.today()
# print('Today: %s' % TODAY)

# 取得要爬的日期
BEFORE_DAY = 3
CRAWLER_DAY = TODAY - datetime.timedelta(days=BEFORE_DAY)
print('爬取日期: %s' % CRAWLER_DAY)

# 宣告 my_ptt_crawler
my_ptt_crawler = ptt_crawler()

# 爬起來
my_ptt_crawler.parse_articles_by_date(CRAWLER_DAY, BOARD)
