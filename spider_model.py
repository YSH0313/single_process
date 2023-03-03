import os
import sys
import time
import socket
import random
from xpinyin import Pinyin
from pathlib import Path

import requests

from config.settings import Mysql, log_path
from config.Cluster import Cluster

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

model = """# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *


class Class_nameSpider(Parent_class):
    name = 'model'

    def __init__(self):
        Parent_class.__init__(self)
        # self.online = True
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        url = 'https://www.baidu.com/'
        yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    start_run = Class_nameSpider()
    start_run.run()"""

model_new = """# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *


class Class_nameSpider(Parent_class):
    name = 'model'
    spider_sign = 'sign_model'

    def __init__(self):
        Parent_class.__init__(self)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        url = 'https://www.baidu.com/'
        yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    start_run = Class_nameSpider()
    start_run.run()"""

cluster = Cluster()
p = Pinyin()


def re_name(str_data):
    new_name = ''.join([i.capitalize() for i in str_data.split('_')])
    return new_name


def register_spider(spider_path, owner):
    url = "http://8.140.146.196:8889/liuqingchuan"
    data = {'type': 'register', 'task_name': f'{spider_path}', 'group_name': 'kaifa', 'owner': owner, }
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        print(response.status_code, '增量爬虫注册成功')
    else:
        print('增量爬虫注册异常，请检查！')


def production(spider_name, incremental, pages, owner, remarks, owner_path, interval_time=None, rabbitmq=True, redis=False, sign=''):
    sys.argv.pop(0)
    current_path = os.getcwd()
    if len(sys.argv) != 0:
        current_path = current_path
    else:
        current_path = os.getcwd() + '/spider'

    def creat_spider():
        Parent_class = 'Manager'
        if rabbitmq:
            Parent_class = Parent_class
        if redis:
            Parent_class = 'ManagerRedis'
        only_path = os.path.join(current_path, owner_path+spider_name + '.py')
        with open(only_path, 'wb') as file:
            if sign:
                file.write(
                    model_new.replace('Class_name', re_name(spider_name)).replace('sign_model', sign).replace('model', spider_name).replace('Parent_class', Parent_class).encode('utf-8'))
            else:
                file.write(
                    model.replace('Class_name', re_name(spider_name)).replace('model', spider_name).replace('Parent_class', Parent_class).encode('utf-8'))
        if incremental == True:
            # command = f'nohup python -u {os.path.join(current_path, spider_name + ".py")} {pages} >> /dev/null 2>&1 &'
            spider_path = os.path.join('/home/bailian/single_process/spider/', owner_path+spider_name + ".py")
            print(spider_path)
            register_spider(spider_path=spider_path, owner=p.get_pinyin(owner, ''))
            log_path_lats = log_path+f'/{spider_name}.log'
            # sql = """INSERT INTO `{db}`.`single_process_listener`(`spider_path`, `interval_time`, `incremental`, `is_run`, `server_name`, `owner`) VALUES ('{spider_name}', '{interval_time}', '{incremental}', 'no', '{server_name}', '{owner}');""".format(
            #     db=Mysql['MYSQL_DBNAME'], spider_name=spider_name, interval_time=interval_time,
            #     incremental=incremental, server_name=socket.gethostbyname(socket.gethostname()), owner=owner)

            sql = """INSERT INTO `{db}`.`spiderlist_monitor`(`spider_name`, `spider_path`, `log_path`, `pages`, `run_time`, `owner`, `is_run`, `remarks`, `add_time`, `sign`) VALUES ('{spider_name}', '{spider_path}', '{log_path}', '{pages}', '{run_time}', '{owner}', '{is_run}', '{remarks}', '{add_time}', '{sign}');""".format(
                db=Mysql['MYSQL_DBNAME'], spider_name=spider_name, log_path=log_path_lats, spider_path=spider_path, pages=pages, run_time=random.randint(0, 59), owner=owner, is_run='no', remarks=remarks, add_time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), sign=sign)
            cluster.cursor.execute(sql)
            cluster.db.commit()
            log_sql = f"""INSERT INTO `spiderdetails_info` (`spider_name`, `spider_path`, `log_path`) VALUES ('{spider_name}', '{spider_path}', '{log_path_lats}');"""
            cluster.cursor.execute(log_sql)
            cluster.db.commit()
        print('创建爬虫文件\033[1;31;0m', spider_name, '\033[0m完成')
        return

    my_file = Path(os.path.join(current_path, owner_path))
    if not my_file.is_dir():
        os.makedirs(os.path.join(current_path, owner_path))

    flag = os.path.exists(os.path.join(current_path, owner_path+spider_name + '.py'))
    if flag == False:
        creat_spider()
    elif flag == True:
        print('\033[1;31;0m名称为：', spider_name, '的爬虫文件已经存在\033[0m')
        while 1:
            judge = input('是否覆盖(y/n)?')
            if judge == 'y':
                creat_spider()
                break
            if judge == 'n':
                pass
                break
            else:
                pass


if __name__ == '__main__':
    production('ceshi', True, 50, '袁少航', '测试用的', 'ysh_spiders/ceshi/')
    # spider_name = sys.argv[1]
    # incremental = sys.argv[2]
    # interval_time = sys.argv[3]
    # owner = sys.argv[4]
    # rabbitmq = True if sys.argv[5] == 'rabbitmq' else False
    # redis = True if sys.argv[5] == 'redis' else False
    # production(spider_name, incremental, interval_time, owner, rabbitmq, redis)
