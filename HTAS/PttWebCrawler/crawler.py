import requests
import json


class PttWebCrawler():
    PTT_URL = 'https://www.ptt.cc'

    def __init__():
        pass

    @staticmethod
    def parse(link, timeout=3):
        # resp = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY, timeout=timeout)
        resp = requests.get(url=link, cookies={'over18': '1'}, timeout=timeout)
        # print('status code: %d' % (resp.status_code))
        if (resp.status_code != 200):
            print('invalid url:', resp.url)
            return json.dumps({"error": "invalid url"}, sort_keys=True, ensure_ascii=False)
