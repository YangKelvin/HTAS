import requests
import json
from bs4 import BeautifulSoup
import re
from six import u
import codecs

class PttWebCrawler():
    PTT_URL = 'https://www.ptt.cc'

    def __init__():
        pass

    @staticmethod
    def parse(link, article_id, board, timeout=3):
        # resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY, timeout=timeout)
        resp = requests.get(url=link, cookies={'over18': '1'}, timeout=timeout)
        # print('status code: %d' % (resp.status_code))
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
        print(content)

        json_data = {
            'url': link,
            'board': board,
            'article_id': article_id,
            'article_title': title,
            'author': author,
            'date': date,
            'content': content,
            # 'ip': ip,
            'message_count': message_count,
            'messages': messages
        }
        return json.dumps(json_data, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(data)