# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2020-02-23 09:56:50
# @Version: 1.0.0
# @Description: 测试爬虫文件

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *


class first_spider(ManagerMemory):
    name = 'first_spider'
    custom_settings = {
        'Waiting_time': 10,
        'IS_PROXY': False,
        'IS_SAMEIP': False,
        'UA_PROXY': False,
        'max_request': 1,
        # 'PREFETCH_COUNT': 50
    }

    def __init__(self):
        ManagerMemory.__init__(self)
        # self.online = True
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

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
