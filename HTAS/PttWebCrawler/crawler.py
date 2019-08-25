import requests
import json
from bs4 import BeautifulSoup
import re
from six import u
import codecs
import os
import sys
import time
from datetime import datetime

VERIFY = True
if sys.version_info[0] < 3:
    VERIFY = False
    requests.packages.urllib3.disable_warnings()

class PttWebCrawler():
    PTT_URL = 'https://www.ptt.cc'

    def __init__(self):
        pass

    def parse_articles(self, start, end, board, path='.', timeout=3):
        print('parse articles')
        filename = board + '-' + str(start) + '-' + str(end) + '.json'
        filename = os.path.join(path, filename)
        self.store(filename, u'{"articles": [', 'w')
        for i in range(end-start+1):
            index = start + i
            print('Processing index:', str(index))
            resp = requests.get(
                url = self.PTT_URL + '/bbs/' + board + '/index' + str(index) + '.html',
                cookies={'over18': '1'}, verify=VERIFY, timeout=timeout
            )
            if resp.status_code != 200:
                print('invalid url:', resp.url)
                continue
            soup = BeautifulSoup(resp.text, 'html.parser')
            divs = soup.find_all("div", "r-ent")
            for div in divs:
                try:
                    # ex. link would be <a href="/bbs/PublicServan/M.1127742013.A.240.html">Re: [問題] 職等</a>
                    href = div.find('a')['href']
                    link = self.PTT_URL + href
                    article_id = re.sub('\.html', '', href.split('/')[-1])
                    if div == divs[-1] and i == end-start:  # last div of last page
                        self.store(filename, self.parse(link, article_id, board), 'a')
                    else:
                        self.store(filename, self.parse(link, article_id, board) + ',\n', 'a')
                except:
                    pass
            time.sleep(0.1)
        self.store(filename, u']}', 'a')
        return filename

    def parse_articles_by_date(self, target_day, board, path='.', timeout=3):
        # 取得看板的 index
        url_index = self.PTT_URL + '/bbs/' + board + '/index.html'

        # 設定 filename
        filename = board + '(' + str(target_day) + ').json'
        filename = os.path.join(path, filename)
        # print('filename: %s' % filename)

        resp = requests.get(
            url = url_index,
            cookies={'over18': '1'}, verify=VERIFY, timeout=3
        )

        # 取得八卦版的最新頁數
        top_page = self.get_top_page(url_index, resp)
        # print('top_page: %s' % top_page)
        
        # 更新 url
        url_index = self.PTT_URL + '/bbs/' + board + '/index'+ str(top_page) + '.html'
        # print('url_index: %s' % url_index)

        # 取得那一日第一篇文章的頁數
        # top_page = 38540
        start_page, end_page = self.find_start_day(self.PTT_URL, board, top_page, timeout, target_day)
        print('start page: %s' % start_page)
        print('end page: %s' % end_page)
        
        # 爬起來
        print('parse articles')
        self.store(filename, u'{"articles": [', 'w')
        resp = ''

        is_last_page = False    # 判斷是否為最後一頁

        data_index = 0      # 流水號
        for i in range(end_page - start_page + 1):
            index = start_page + i
            page_count = end_page - start_page
            # print(i)
            # print(page_count)
            if (i == page_count):
                print('last page')
                is_last_page = True

            print('Processing index:', str(index))
            try:
                resp = requests.get(
                    url = self.PTT_URL + '/bbs/' + board + '/index' + str(index) + '.html',
                    cookies={'over18': '1'}, verify=VERIFY, timeout=timeout
                )
            except:
                Exception('timeout over')
                continue

            if resp.status_code != 200:
                print('invalid url:', resp.url)
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            divs = soup.find_all("div", "r-ent")

            # 處理 divs，移除不符合目標日期的文章
            divs_index = 0
            for i in range(len(divs)):
                # print('round %s' % i)
                is_we_want = self.is_we_want_article(divs[divs_index], target_day)
                if(is_we_want != True):
                    del divs[divs_index]
                    continue
                divs_index = divs_index + 1
            # print(len(divs))

            for div in divs:
                try:
                    # ex. link would be <a href="/bbs/PublicServan/M.1127742013.A.240.html">Re: [問題] 職等</a>
                    href = div.find('a')['href']
                    link = self.PTT_URL + href
                    article_id = re.sub('\.html', '', href.split('/')[-1])

                    if (div == divs[len(divs)-1] and is_last_page):     # 是否為最後一頁的最後一個 div
                        self.store(filename, self.parse(link, article_id, board, data_index), 'a')
                    else:
                        self.store(filename, self.parse(link, article_id, board, data_index) + ',\n', 'a')
                    data_index = data_index + 1
                except:
                    pass
            time.sleep(0.1)
        self.store(filename, u']}', 'a')

    @staticmethod
    def parse(link, article_id, board, data_index, timeout=3):
        # resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY, timeout=timeout)
        resp = requests.get(url=link, cookies={'over18': '1'}, timeout=timeout)
        # print('status code: %d' % (resp.status_code))
        print('Processing article:', article_id)
        if (resp.status_code != 200):
            print('invalid url:', resp.url)
            return json.dumps({"error": "invalid url"}, sort_keys=True, ensure_ascii=False)

        soup = BeautifulSoup(resp.text, 'html.parser')
        # print(soup)
        main_content = soup.find(id="main-content")
        # print(main_content)
        metas = main_content.select('div.article-metaline')
        # print(metas)

        '''取得「作者」、「標題」、「日期」'''
        author = ''
        title = ''
        date = ''

        if (metas):
            author = metas[0].select('span.article-meta-value')[0].string
            title = metas[1].select('span.article-meta-value')[0].string
            date = metas[2].select('span.article-meta-value')[0].string
            date = datetime.strptime(date, '%a %b %d %H:%M:%S %Y')
            date = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
            # print('author: %s \ntitle: %s \ndate: %s' % (author, title, date))

            # remove meta nodes (?)
            # extract()： 返回被選擇元素的unicode字符串
            for meta in metas:
                meta.extract()
            for meta in main_content.select('div.article-metaline-right'):
                meta.extract()

        # print(main_content)

        '''取得貼文'''
        messages = []
        p, b, n = 0, 0, 0
        pushes = main_content.find_all('div', class_='push')
        for push in pushes:
            push.extract()

        # print(pushes)
        for push in pushes:
            # print(push)
            push_tag = push.find('span', 'push-tag').string.strip(' \t\n\r')
            # print(push_tag)
            push_userid = push.find(
                'span', 'push-userid').string.strip(' \t\n\r')
            # print(push_userid)
            push_content = push.find('span', 'push-content').strings
            push_content = ' '.join(push_content)[
                1:].strip(' \t\n\r')  # remove ':'
            # print(push_content)
            push_ipdatetime = push.find(
                'span', 'push-ipdatetime').string.strip(' \t\n\r')
            # print(push_ipdatetime)

            messages.append({
                'push_tag': push_tag,
                'push_userid': push_userid,
                'push_content': push_content,
                'push_ipdatetime': push_ipdatetime
            })

            if push_tag == u'推':
                p += 1
            elif push_tag == u'噓':
                b += 1
            else:
                n += 1
        # print(messages)
        message_count = {
            'all': p+b+n,
            'count': p-b,
            'push': p,
            'boo': b,
            "neutral": n}
        # print(message_count)

        '''取得內文'''
        # 移除 '※ 發信站:' (starts with u'\u203b'), '◆ From:' (starts with u'\u25c6'), 空行及多餘空白
        # 保留英數字, 中文及中文標點, 網址, 部分特殊符號
        filtered = [v for v in main_content.stripped_strings if v[0]
                    not in [u'※', u'◆'] and v[:2] not in [u'--']]
        # print(filtered)
        expr = re.compile(
            u(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]'))
        for i in range(len(filtered)):
            filtered[i] = re.sub(expr, '', filtered[i])
            # print(filtered[i])

        filtered = [_f for _f in filtered if _f]  # remove empty strings
        # remove last line containing the url of the article
        filtered = [x for x in filtered if article_id not in x]
        content = ' '.join(filtered)
        content = re.sub(r'(\s)+', ' ', content)
        # print(content)

        json_data = {
            'article_id': board + '(' + date + ')_' + str(data_index),
            'article_title': title,
            'author': author,
            'date': date,
            'content': content,
            'message_count': message_count,
            'messages': messages,
            'url': link,
            'board': board
        }
        return json.dumps(json_data, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def get_top_page(url_index, resp):
        soup = BeautifulSoup(resp.text, "html.parser")

        # action-bar 的五顆按鈕
        # 其中第三顆為 '上一頁'
        btns = soup.select('div.btn-group > a')
        # print(btns[3])

        # 取得上一頁按鈕的 href
        up_page_href = btns[3]['href']
        # print(up_page_href)

        # 取得 top_page
        top_page = up_page_href.split('/')[3]   # 取得 index頁數.html
        top_page = top_page.split('.')[0]       # 取得 index頁數
        top_page = top_page[5:]                 # 取得 頁數（此為上一頁頁數
        top_page = int(top_page) + 1            # 取得最新的頁數
        # print(top_page)

        return top_page
    
    @staticmethod
    def get_article_date(link, timeout):

        resp = requests.get(url=link, cookies={'over18': '1'}, timeout=timeout)
        if (resp.status_code != 200):
            return 'invalid url'
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        main_content = soup.find(id="main-content")
        metas = main_content.select('div.article-metaline')
        date = metas[2].select('span.article-meta-value')[0].string
        # print(date)

        return date

    @staticmethod
    def convert_date(origin_datetime):
        result = datetime.strptime(origin_datetime, '%a %b %d %H:%M:%S %Y')
        result = str(result)[:10]
        # print(result)

        return result

    @staticmethod
    def find_start_day(ptt_url, board, start_page, timeout, target_day):
        page = start_page   # 當前頁數
        end_page = 0        # 目標天數的最後一頁
        status = 0          # 0: 初始值 1: 為當天日期 2: 當天日期變成不是當天日期
        
        while(True):
            print('Processing page:', str(page))

            # 取得 那一頁的 response
            try:
                page_url = ptt_url + '/bbs/' + board + '/index' + str(page) + '.html'
                current_page_resp = requests.get(
                    url = page_url,
                    cookies={'over18': '1'}, verify=VERIFY, timeout=timeout
                )
            except:
                Exception('timeout over')
                continue

            # 是否找到該網頁
            if (current_page_resp.status_code != 200):
                print('invalid url:', current_page_resp.url)
                continue

            soup = BeautifulSoup(current_page_resp.text, 'html.parser')
            divs = soup.find_all("div", "r-ent")
            current_article_date = divs[0].find_all('div', 'date')[0].text.strip()
            current_article_date = datetime.strptime(current_article_date, '%m/%d')
            # print(current_article_date)

            if(current_article_date.month == target_day.month and current_article_date.day == target_day.day):
                # 同一天
                if(status == 0):
                    status = 1
                    end_page = page
            elif(current_article_date.month != target_day.month or current_article_date.day != target_day.day):
                # 不同天
                if(status == 1):
                    status = 2
                    break  

            # 找到前一天日期時跳出 while 迴圈
            print(status)
            if (status == 2):
                break
            page = page - 1
        
        return page, end_page

    @staticmethod
    def is_we_want_article(div, target_day):
        # print(div)
        current_article_date = div.find_all('div', 'date')[0].text.strip()
        current_article_date = datetime.strptime(current_article_date, '%m/%d')
        return (current_article_date.month == target_day.month and current_article_date.day == target_day.day)