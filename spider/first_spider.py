# -*- coding: utf-8 -*-
import base64
import json
import os
import re
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *
from string import Template
import ddddocr
from urllib.parse import quote
import hmac


class first_spider(Manager):
    name = 'first_spider'
    custom_settings = {
        # 'retry_http_codes': [202, 412],
        # 'Waiting_time': 20
        # 'IS_PROXY': False,
        'IS_SAMEIP': False,
        'UA_PROXY': False,
        # 'X_MAX_PRIORITY': 15,
        # 'max_request': 1
    }

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        # self.ddd = ddddocr.DdddOcr(show_ad=False)
        # self.pages = True

    def start_requests(self):
        for i in range(100):
            url = f'https://www.baidu.com'
            yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        print('状态码：', response.status_code)


if __name__ == '__main__':
    start_run = first_spider()
    start_run.run()