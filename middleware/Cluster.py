# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2023-02-24- 18:17:44
# @Version: 1.0.0
# @Description: TODO


import sys
import oss2
import json
import redis
import hashlib
import logging
import pymysql
import datetime
from items import *
from kafka import KafkaProducer
from datetime import datetime, date
from filestream_y.FileStream_y import stream_type
from rediscluster import RedisCluster
from config.spider_log import SpiderLog
from asyncio_config.my_Requests import MyRequests, MyFormRequests
from settings import REDIS_HOST_LISTS, Mysql, redis_connection, kafka_servers, kafka_connection, access_key_id, \
    access_key_secret, bucket_name, endpoint

import re
from middleware.pymysqlpool.pymysqlpool import ConnectionPool
from library_tool.single_tool import SingleTool


class ExpandJsonEncoder(json.JSONEncoder):
    '''
    采用json方式序列化传入的任务参数，而原生的json.dumps()方法不支持datetime、date，这里做了扩展
    '''

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class ParentObj(SpiderLog, SingleTool):
    name = None
    spider_sign = None

    def __init__(self, custom_settings=None, **kwargs):
        SpiderLog.__init__(self)
        SingleTool.__init__(self)
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        self.logger.name = logging.getLogger(__name__).name
        self.db_success_count = 0
        self.ka_success_count = 0
        self.catch_count = 0
        self.right_count = 0
        self.error_count = 0
        self.success_code_count = 0
        self.request_count = 0
        self.wrong_count = 0
        self.fangqi_count = 0
        self.exc_count = 0
        self.other_count = 0
        self.exec_count = 0
        self.Estimated_total = 0
        self.owner = '开发爬虫'
        self.source = '未知来源'
        self.startup_nodes = REDIS_HOST_LISTS
        self.online = True if sys.platform == 'linux' else False
        self.monitor = sys.argv[2] if len(sys.argv) > 2 else None

    def key_judge(self, item):
        key_list = ['title', 'url', 'pub_time', 'source', 'html']
        if isinstance(item, BiddingItem):
            item = item.dict()
        for k in key_list:
            sgin = item.__contains__(k)
            while not sgin:
                return False
        return True

    def value_judge(self, item):
        key_list = ['title', 'url', 'pub_time', 'source', 'html']
        if isinstance(item, BiddingItem):
            item = item.dict()
        for k in key_list:
            sgin = item.get(k, 0)
            while not sgin:
                return k
        return True

    def prints(self, item, is_replace=True, db=None, is_info=True, deal_time=True, sgin=''):
        info_item = {}
        item_last = {}
        html = item.get('html')
        for k, v in item.items():
            if (v == None) or (v == 'None') or (v == ''):
                continue
            elif (('time' not in k) and ('Time' not in k) and ('updated' not in k) and ('date' not in k)) and (
                    isinstance(v, dict) == False):
                if is_replace:
                    item_last[k] = self.data_deal(v)
                else:
                    item_last[k] = v
            elif isinstance(v, dict):
                item_last[k] = str(v)
            elif k == 'body':
                item_last[k] = f"""{v}"""
            elif ('time' in k) or ('Time' in k) or ('updated' in k) or ('date' in k) or (k.endswith('T') == True):
                if self.is_valid_date(v) and deal_time:
                    item_last[k] = self.date_refix(v)
                else:
                    item_last[k] = v
        if is_info:
            # del item_last['log_info']
            if sgin and sgin != 'data_test':
                for k, v in item_last.items():
                    info_item[sgin + k] = v
            if 'html' in item_last.keys() and sgin != 'data_test':
                del item_last['html']
            self.logger.info('\r\n{item}'.format(
                item=json.dumps(item_last if not info_item else info_item, indent=2, ensure_ascii=False)))
            self.logger.info('===========================================================')
        if db == 'kafka':
            self.ka_success_count += 1
        elif db == 'mysql':
            self.db_success_count += 1
        item_last['html'] = html
        return item_last

    def get_bucket(self):
        return oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    def oss_push_img(self, url, data, suffix='', custom=False, header={}):
        """
        :param url: 详情页链接
        :param data: 文件二进制数据流
        return: 对外能访问的图片URL
        """
        if len(data) < 10:
            return url
        oss_bucket = self.get_bucket()
        stream = stream_type(data, header)
        if not stream and not custom:
            suffix_list = ['.doc', '.docx', '.xlr', '.xls', '.xlsx', '.pdf', '.txt', '.jpg', '.png', '.rar', '.zip']
            for i in suffix_list:
                if url.endswith(i):
                    suffix = i
            if not suffix.startswith('.'):
                suffix = '.' + suffix
        elif stream and not custom:
            suffix = '.' + stream
        else:
            if not suffix.startswith('.'):
                suffix = '.' + suffix
        if 'html' in suffix or suffix == '.':
            return url
        url_md5 = hashlib.sha1(url.encode()).hexdigest() + suffix
        if self.spider_sign:
            url_md5 = 'proposed/' + hashlib.sha1(url.encode()).hexdigest() + suffix
        oss_bucket.put_object(url_md5, data)
        oss_url = f'https://bid.snapshot.qudaobao.com.cn/{url_md5}'
        return oss_url


class MysqlDb(ParentObj):
    def __init__(self, custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        self.host = Mysql['MYSQL_HOST']
        self.port = Mysql['PORT']
        self.user = Mysql['MYSQL_USER']
        self.password = Mysql['MYSQL_PASSWORD']
        self.db = Mysql['MYSQL_DBNAME']
        # self.conn = None
        self.pool = self.create_pool()
        self.condition_re = re.compile('(.*?)\\(')
        self.params_re = re.compile('\\((.*?)\\)')

    def create_pool(self):
        conn = ConnectionPool(
            pool_name='mypool',
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            autocommit=False
        )
        return conn

    def execute(self, query, parameters=None, many=False):
        attempts = 3  # allow 3 attempts to execute the query
        while attempts > 0:
            conn = self.pool.borrow_connection()
            try:
                with conn.cursor() as cursor:
                    if many:
                        cursor.executemany(query, parameters)
                    else:
                        cursor.execute(query, parameters)
                    conn.commit()
                    if cursor.lastrowid:
                        return cursor.lastrowid
                    else:
                        return cursor.rowcount
            except pymysql.OperationalError as e:
                if e.args[0] in (2006, 2013):  # MySQL server has gone away
                    self.pool.close()
                    self.pool = self.create_pool()
                    attempts -= 1
                else:
                    raise
            except Exception as e:
                self.logger.error(f"Error while executing query: {e}")
                conn.rollback()
                attempts -= 1
                if attempts == 0:
                    raise Exception("Failed to execute query after 3 attempts")
            finally:
                self.pool.return_connection(conn)
                # if conn:
                #     conn.close()

    def insert(self, table, data, if_update=False, is_info=True):
        columns = ', '.join([f"`{i}`" for i in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT IGNORE INTO `{table}` ({columns}) VALUES ({placeholders});"
        sql = query % tuple([f"'{i}'" if i else i for i in data.values()])
        if if_update:
            update = ', '.join([f"`{key}` = %s" for key in data.keys()])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update}"
            sql = query % tuple([f"'{i}'" if i else i for i in data.values()] * 2)
        if is_info:
            self.logger.info(sql)
            self.logger.info('===========================================================')
        return self.execute(query, tuple(data.values()))

    def update(self, table, set_data, where=None):
        set_pairs = [f"`{column}`=%s" for column in set_data.keys()]
        query = f"UPDATE `{table}` SET {', '.join(set_pairs)}"
        parameters = tuple(set_data.values())
        if where:
            query += f" WHERE {where}"
        sql = query % tuple([f"'{i}'" if i else i for i in parameters])
        self.logger.info(sql)
        self.logger.info('===========================================================')
        return self.execute(query, parameters)

    def delete(self, table, where=None):
        query = f"DELETE FROM `{table}`"
        if where:
            query += f" WHERE {where}"
        self.logger.info(query)
        self.logger.info('===========================================================')
        return self.execute(query)

    def trucate(self, table):
        sql = f"""TRUNCATE `{table}`;"""
        return self.execute(sql)

    def get_condition(self, columns):
        condition_map = {'count': 'count', 'max': 'max', 'min': 'min', 'sum': 'sum', 'avg': 'avg',
                         'distinct': 'distinct'}
        condition = ''
        if isinstance(columns, list):
            columns = ', '.join([f"`{i}`" for i in columns])
        elif isinstance(columns, str):
            condition = self.deal_re(self.condition_re.search(columns))
            condition_exis = True if [True for i in condition_map.keys() if i.upper() in columns.upper()] else False
            if not condition_exis:
                columns = ', '.join(f'`{i.strip(" ")}`' for i in columns.split(','))
        return condition_map, condition, columns

    def select(self, table, columns='*', where=None, order_by=None, limit=None, offset=None):
        condition_map, condition, columns = self.get_condition(columns)
        query = f"SELECT {columns} FROM `{table}`"
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"
        self.logger.info('查询字段：' + query)
        self.logger.info('===========================================================')
        with self.pool.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            if self.judge_er(condition):
                condition_map = [i.upper() for i in condition_map.keys()]
            if f'{condition}' in condition_map:
                data = data[0].get(columns)
            return data

    def judge_er(self, str_data):
        if str_data.isupper():
            return True
        else:
            return False


class KafkaDb(ParentObj):
    def __init__(self, custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value

        if kafka_connection:
            self.producer = KafkaProducer(bootstrap_servers=kafka_servers['server'], max_request_size=3145728,
                                          api_version=(0, 10, 2))

    def key_judge(self, item):
        key_list = ['title', 'url', 'pub_time', 'source', 'html']
        if isinstance(item, BiddingItem):
            item = item.dict()
        for k in key_list:
            sgin = item.__contains__(k)
            while not sgin:
                return False
        return True

    def value_judge(self, item):
        key_list = ['title', 'url', 'pub_time', 'source', 'html']
        if isinstance(item, BiddingItem):
            item = item.dict()
        for k in key_list:
            sgin = item.get(k, 0)
            while not sgin:
                return k
        return True

    def kafka_producer(self, item):
        key_judge = False
        value_judge = False
        if self.isSubClassOf(item, SingleItem):
            item = item.dict()
            if 'file_url' in item.keys():
                del item['file_url']
        if isinstance(item, BiddingItem) or isinstance(item, dict):
            key_judge = self.key_judge(item)
            value_judge = self.value_judge(item)
        item['pub_time'] = self.date_refix(item.get('pub_time')) if item.get('pub_time') else None
        if (key_judge == True and value_judge == True and item['pub_time']) or (
                item.get('project_name') and self.spider_sign):
            if self.pages:
                item['monitor'] = True
            if self.online and not self.monitor:
                topic = kafka_servers['topic'] if key_judge and value_judge else 'proposed_tasks_mid'
                self.producer.send(topic, json.dumps(item).encode('utf-8'))
            self.send_log(req_id=0, code='40', log_level='INFO', url=item['url'], message='数据存储kafka成功',
                          show_url=item.get('show_url', ''))
            self.prints(item, is_replace=False, db='kafka', sgin='data_test' if not self.online else '')
            # self.add_url_sha1(item['url']) if not item.get('show_url') else (self.add_url_sha1(item['url']), self.add_url_sha1(item.get('show_url'), sgin='show_'))
            self.right_count += 1
        else:
            debug_info = value_judge
            if (not key_judge and not value_judge) or self.spider_sign:
                debug_info = 'project_name'
            if debug_info and not item['pub_time']:
                debug_info = 'pub_time'
            self.logger.debug(
                f'\033[5;31;1m{debug_info} \033[5;33;1mfield does not exist, Data validation failed, please check！\033[0m {item}')
            self.send_log(req_id=0, code='31', log_level='WARN', url=item['url'], message=f'抓取结果缺少{debug_info}字段',
                          show_url=item.get('show_url'))
            self.error_count += 1
        self.catch_count += 1

    def send_log(self, req_id, code, log_level, url, message, time='', formdata='', show_url=''):
        log_info = {
            'log_id': self.get_inttime(),
            'req_id': req_id,
            'crawler_time': self.get_inttime(is_int=False),
            'crawler_name': self.source,
            'crawler_source': 2,
            'log_level': log_level,
            'code': code,
            'url': url,
            'message': message,
            'time': time if time else '',
            'crawler_author': self.owner,
            'formdata': formdata if formdata else '',
            'show_url': show_url if show_url else ''
        }
        if self.online:
            self.producer.send('qdb_crawler_log_online_topic', json.dumps(log_info).encode('utf-8'))
            self.logger.info(f'Log details：{log_info}')


class RedisDb(ParentObj):
    def __init__(self, key='', custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        self.key = 'ysh_' + key
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        if redis_connection:
            if len(REDIS_HOST_LISTS) == 1:
                for k, v in REDIS_HOST_LISTS[0].items():
                    self.pool = redis.ConnectionPool(host=k, port=v, db=1, decode_responses=True)
                    self.r = redis.Redis(connection_pool=self.pool)
            elif len(REDIS_HOST_LISTS) > 1:
                self.r = RedisCluster(startup_nodes=self.startup_nodes, decode_responses=True)

    def get_len(self, key):
        keys = self.get_keys(key)
        # 每个键的任务数量
        key_len = [(k, self.r.llen(k)) for k in keys]
        # 所有键的任务数量
        task_len = sum(dict(key_len).values())
        return task_len, key_len

    def get_keys(self, key):
        # Redis的键支持模式匹配
        keys = self.r.keys(key + '-[0-9]*')
        # 按优先级将键降序排序
        keys = sorted(keys, key=lambda x: int(x.split('-')[-1]), reverse=True)
        return keys

    def push_task(self, tasks, key=None, level=0):
        '''
        双端队列，左边推进任务
        :param level: 优先级(int类型)，数值越大优先级越高，默认1
        :return: 任务队列任务数量
        '''
        # 重新定义优先队列的key
        if key == None:
            key = self.key
        new_key = key + '-' + str(level)
        # 序列化任务参数
        if (isinstance(tasks, MyFormRequests)) or (isinstance(tasks, MyRequests)):
            mess_demo = {}
            for k, v in tasks.__dict__.items():
                if (k == 'callback') and (v != None):
                    if (isinstance(v, str)):
                        mess_demo[k] = v
                    else:
                        fun_name = v.__name__
                        mess_demo['callback'] = fun_name
                else:
                    mess_demo[k] = v
            tasks = json.dumps(mess_demo, cls=ExpandJsonEncoder)
            self.r.lpush(new_key, tasks)
        elif isinstance(tasks, dict):
            tasks = json.dumps(tasks, cls=ExpandJsonEncoder)
            self.r.lpush(new_key, tasks)
        else:
            self.r.lpush(new_key, tasks)


class Cluster(MysqlDb, KafkaDb, RedisDb):
    def __init__(self, key='', custom_settings=None, **kwargs):
        super().__init__(key=key, custom_settings=custom_settings, **kwargs)


if __name__ == '__main__':
    database = Cluster()

    for i in range(10):
        database.insert(table='db_base_test', data={'name': 'yuanshaohang', 'age': None, 'sex': '男'})  # 增

    database.update(table='db_base_test', set_data={'name': '袁少航', 'age': 20, 'sex': '男'}, where="`name`='yuanshaohang'")  # 改

    database.delete(table='db_base_test', where="name='袁少航' limit 1")  # 删

    data_list = database.select(table='db_base_test', columns='name', where='`name` = "袁少航"')  # 查
    print(data_list)