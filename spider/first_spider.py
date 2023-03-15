# -*- coding: utf-8 -*-
import asyncio
import base64
import json
import os
import random
import re
import sys
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *
from string import Template
import ddddocr
from urllib.parse import quote
import hmac
from filestream_y.FileStream_y import stream_type


class first_spider(Manager):
    name = 'first_spider'
    custom_settings = {
        # 'retry_http_codes': [202, 412],
        'Waiting_time': 10,
        'IS_PROXY': False,
        'IS_SAMEIP': False,
        'UA_PROXY': False,
        # 'X_MAX_PRIORITY': 15,
        'max_request': 1,
        # 'PREFETCH_COUNT': 50
    }

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.ddd = ddddocr.DdddOcr(show_ad=False)
        # self.pages = True

    def start_requests(self):
        for i in range(100):
            url = 'https://www.baidu.com'
            yield MyRequests(url=url, headers=self.header, callback=self.parse)

            # self.send_message(i)

    def parse(self, response):
        print('parse状态码：', response.status_code)
        yield MyRequests(url=response.url, headers=self.header, callback=self.ceshi)

    def ceshi(self, response):
        if response.status_code == None:
            yield MyRequests(url=response.url, headers=self.header, callback=self.ceshi)
        else:
            print('ceshi状态码：', response.status_code)

    def parse_only(self, body):
        time.sleep(random.uniform(2, 3))
        print(body)


if __name__ == '__main__':
    start_run = first_spider()
    start_run.run()
