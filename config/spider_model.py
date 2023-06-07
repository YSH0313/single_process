import os
import sys
import time
import random
from xpinyin import Pinyin
import requests
from settings import log_path
from middleware.Cluster import Cluster

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from jinja2 import Template

model = Template("""# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *


class {{ Class_name }}Spider(Manager):
    name = '{{ model }}'{{ spider_sign }}

    def __init__(self):
        Manager.__init__(self)
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
    start_run = {{ Class_name }}Spider()
    start_run.run()""")

cluster = Cluster()
p = Pinyin()


def re_name(str_data: str):
    """格式化爬虫类名"""
    new_name = ''.join([i.capitalize() for i in str_data.split('_')])
    return new_name


def now_time(is_date=False):
    """获取现在时间"""
    if is_date == False:
        now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return now_time
    now_time = str(time.strftime("%Y-%m-%d", time.localtime()))
    return now_time


def register_spider(spider_path: str, owner: str):
    """
    :param spider_path: 爬虫路径
    :param owner: 所属人
    :return: 向调度平台注册
    """
    url = "http://8.140.146.196:8889/liuqingchuan"
    data = {'type': 'register', 'task_name': f'{spider_path}', 'group_name': 'kaifa', 'owner': owner, }
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        print(response.status_code, '增量爬虫注册成功')
    else:
        print('增量爬虫注册异常，请检查！')


def get_path(spider_name: str, file_dir: str):
    """
    :param spider_name: 爬虫名称
    :param file_dir: 爬虫文件目录
    :return: 爬虫目录， 爬虫文件路径， 使用者目录
    """
    base_path = 'spider'
    current_path = os.path.join(os.getcwd(), base_path)
    spider_path = os.path.join(current_path, file_dir)
    file_path = os.path.join(spider_path, f'{spider_name}.py')
    spider_relative_path = f'{file_dir}/{spider_name}.py'
    if file_dir.endswith('/') or file_dir.endswith('\\'):
        spider_relative_path = f'{file_dir}{spider_name}.py'
    owner_path = os.path.join(base_path, spider_relative_path)
    return spider_path, file_path, owner_path


def save_info(spider_name: str, spider_path: str, pages: int, remarks: str, sign: str, owner: str, owner_path: str):
    """
    :param spider_name: 爬虫名称
    :param spider_path: 爬虫路径
    :param pages: 增量页码
    :param remarks: 备注
    :param sign: 任务标识
    :param owner: 所属人
    :param owner_path: 使用者目录
    :return: 保存爬虫信息到mysql
    """
    online_path = os.path.join('/home/bailian/single_process/', owner_path)
    # register_spider(spider_path=online_path, owner=p.get_pinyin(owner, ''))
    log_path_lats = os.path.join(log_path, f'{spider_name}.log')
    data = {
        'spider_name': spider_name,
        'spider_path': online_path,
        'log_path': log_path_lats,
        'pages': pages,
        'run_time': random.randint(0, 59),
        'owner': owner,
        'is_run': 'no',
        'remarks': remarks,
        'add_time': now_time(),
        'sign': sign,
    }
    cluster.insert(table='spiderlist_monitor', data=data, is_info=False)
    log_data = {
        'spider_name': spider_name,
        'spider_path': online_path,
        'log_path': log_path_lats,
    }
    cluster.insert(table='spiderdetails_info', data=log_data, is_info=False)


def write_file(spider_name: str, file_path: str, sign: str):
    """
    :param spider_name: 爬虫名称
    :param file_path: 爬虫文件路径
    :param sign: 任务标识
    :return: 生成爬虫文件
    """
    spider_sign = f"""\n    spider_sign = '{sign}'""" if sign else ''
    with open(file_path, "w") as file:
        file.write(model.render(Class_name=re_name(spider_name), model=spider_name, spider_sign=spider_sign))


def production(spider_name: str, is_increment: bool, pages: int, owner: str, remarks: str, file_dir: str, sign=''):
    """
    :param spider_name: 爬虫名称
    :param is_increment: 是否增量
    :param pages: 增量页码
    :param owner: 所属人
    :param remarks: 备注
    :param file_path: 文件路径
    :return: 根据所给的参数创建爬虫文件
    """
    spider_path, file_path, owner_path = get_path(spider_name, file_dir)
    if os.path.exists(file_path):
        print('\033[1;31;0m名称为：', spider_name, '的爬虫文件已经存在\033[0m')
        while 1:
            judge = input('是否覆盖(y/n)?')
            if judge == 'y':
                write_file(spider_name, file_path, sign)
                print('创建爬虫文件\033[1;31;0m', spider_name, '\033[0m完成')
                break
            if judge == 'n':
                print('爬虫文件\033[1;31;0m', spider_name, '\033[0m未创建')
                break
            else:
                pass
    else:
        if not os.path.exists(spider_path):
            os.makedirs(spider_path)
        write_file(spider_name, file_path, sign)
        if is_increment:
            save_info(spider_name, file_path, pages, remarks, sign, owner, owner_path)
        print('创建爬虫文件\033[1;31;0m', spider_name, '\033[0m完成')


if __name__ == '__main__':
    production('ceshi', True, 50, '袁少航', '测试用的', 'ysh_spiders/ceshi/')
    # spider_name = sys.argv[1]
    # incremental = sys.argv[2]
    # interval_time = sys.argv[3]
    # owner = sys.argv[4]
    # rabbitmq = True if sys.argv[5] == 'rabbitmq' else False
    # redis = True if sys.argv[5] == 'redis' else False
    # production(spider_name, incremental, interval_time, owner, rabbitmq, redis)
