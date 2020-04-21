import os
import sys
import socket
from config.settings import Mysql
from config.Cluster import Cluster

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

model = """# -*- coding: utf-8 -*-
from config.all_config import *


class model(Manager):
    name = 'model'

    def __init__(self):
        Manager.__init__(self, 'queue_name')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        url = 'https://www.baidu.com/'
        request = MyRequests(url=url, headers=self.header, callback=self.parse, level=1)
        self.send_mqdata(request)

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    start_run = model()
    start_run.run('model')"""

cluster = Cluster()
def production(spider_name_demo, incremental, interval_time, owner):
    flag = os.path.exists(os.path.join(os.getcwd()+'\spider', spider_name_demo+'.py'))
    if flag == False:
        only_path = os.path.join(os.getcwd()+'\spider', spider_name_demo+'.py')
        with open(only_path, 'wb') as file:
            file.write(model.replace('model', spider_name_demo).replace('queue_name', 'ysh_'+spider_name_demo).encode('utf-8'))
        if incremental == True:
            print(spider_name_demo, interval_time, incremental)
            sql = """INSERT INTO `{db}`.`single_process_listener`(`spider_name`, `interval_time`, `incremental`, `is_run`, `server_name`, `owner`) VALUES ('{spider_name}', '{interval_time}', '{incremental}', 'no', '{server_name}', '{owner}');""".format(db=Mysql['MYSQL_DBNAME'], spider_name=spider_name_demo, interval_time=interval_time, incremental=incremental, server_name=socket.gethostbyname(socket.gethostname()), owner=owner)
            cluster.cursor.execute(sql)
            cluster.db.commit()
        print('创建爬虫文件\033[1;31;0m', spider_name_demo, '\033[0m完成')
        return
    elif flag == True:
        print('\033[1;31;0m名称为：', spider_name_demo, '的爬虫文件已经存在\033[0m')

# def open_spider(spider_name):
#     sql = """SELECT * FROM single_process_listener WHERE spider_name = '{spider_name}'""".format(spider_name=spider_name)
#     cluster.cursor.execute(sql)
#     cluster.db.commit()
#     data = cluster.cursor.fetchone()
#     if data != None:
#         update_sql = """UPDATE `{db}`.`single_process_listener` SET `is_run` = 'yes' WHERE `spider_name` = '{spider_name_demo}'""".format(db=Mysql['MYSQL_DBNAME'], spider_name_demo=spider_name)
#         cluster.cursor.execute(update_sql)
#         cluster.db.commit()
#         print('\033[1;31;0m'+spider_name+'爬虫程序启动\033[0m', data)
#         return True
#     else:
#         print('\033[1;31;0m如需开启增量，请先在注册表里注册后再次尝试运行，不需要请忽略\033[0m')
#         return False

# def run(spider_name):
#     a = actuator.LoadSpiders()._spiders
#     print(a[spider_name]().name)
#     starttime = datetime.datetime.now()
#     status = open_spider(spider_name)
#     if status == True:
#         only_path = os.path.join(os.getcwd() + '\spider', spider_name + '.py')
#         os.system('python {path} &'.format(path=only_path))
#         close_spider(spider_name)
#         endtime = datetime.datetime.now()
#         print('\033[1;31;0m总用时:\033[0m', endtime - starttime, '分')
#     elif status == False:
#         return

# def close_spider(spider_name):
#     sql = """UPDATE `{db}`.`single_process_listener` SET `spider_name` = '{spider_name}', `is_run` = 'no', `end_time` = '{end_time}' WHERE `spider_name` = '{spider_name_demo}'""".format(db=Mysql['MYSQL_DBNAME'], spider_name=spider_name, end_time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), spider_name_demo=spider_name)
#     cluster.cursor.execute(sql)
#     cluster.db.commit()
#     print('\033[1;31;0m'+spider_name+'爬虫程序关闭\033[0m', str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
#     return


if __name__ == '__main__':
    # production('Practice1', True)
    run('tests')