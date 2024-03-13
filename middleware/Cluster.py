# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2023-02-24 18:17:44
# @Version: 1.0.0
# @Description: TODO
import re
import os
import sys
import json

import pymongo
import redis
import heapq
import logging
from dbutils.pooled_db import PooledDB
import pymysql
import datetime

from pymongo.errors import ConnectionFailure, AutoReconnect

from items import *
from kafka import KafkaProducer
from datetime import datetime, date
from elasticsearch import Elasticsearch
from rediscluster import RedisCluster
from asyncio_config.my_Requests import MyRequests, MyFormRequests
from settings import (REDIS_HOST_LISTS, Mysql, redis_connection, kafka_servers, kafka_connection, ES_CONFIG, IS_INSERT,
                      IS_ES, MONGO_CONFIG, MONGO_client)

# from middleware.pymysqlpool.pymysqlpool import ConnectionPool
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


class ParentObj(SingleTool):
    name = None
    spider_sign = None

    def __init__(self, custom_settings=None, **kwargs):
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


class Mysqldb(ParentObj):
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
        if IS_INSERT:
            self.pool = self.create_pool()
            self.condition_re = re.compile('(.*?)\\(')
            self.params_re = re.compile('\\((.*?)\\)')

    def create_pool(self):
        # 设置连接池参数
        pool = PooledDB(
            creator=pymysql,  # 使用PyMySQL作为数据库连接模块
            maxconnections=10,  # 连接池最大连接数
            mincached=2,  # 初始化时，池中至少创建的空闲的连接
            maxcached=5,  # 池中最多闲置的连接
            maxshared=3,  # 池中最多共享的连接数量
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            charset='utf8mb4',
            use_unicode=True
        )
        return pool

    def execute(self, query, parameters=None, many=False):
        conn = self.pool.connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if many:
                    cursor.executemany(query, parameters)
                else:
                    if 'SELECT' in query:
                        cursor.execute(query)
                        results = cursor.fetchall()
                        conn.commit()
                        return results
                    else:
                        cursor.execute(query, parameters)
                conn.commit()
        except Exception as e:
            import traceback
            traceback.print_exc()
        finally:
            conn.close()  # 使用完毕后，关闭连接（实际上会放回连接池，而不是真正的关闭）

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
        results = self.execute(query)
        return results

    def judge_er(self, str_data):
        if str_data.isupper():
            return True
        else:
            return False


# 暂时弃用
# class MysqlDb(ParentObj):
#     def __init__(self, custom_settings=None, **kwargs):
#         super().__init__(custom_settings=custom_settings, **kwargs)
#         if custom_settings:
#             for varName, value in custom_settings.items():
#                 s = globals().get(varName)
#                 if s:
#                     globals()[varName] = value
#         self.host = Mysql['MYSQL_HOST']
#         self.port = Mysql['PORT']
#         self.user = Mysql['MYSQL_USER']
#         self.password = Mysql['MYSQL_PASSWORD']
#         self.db = Mysql['MYSQL_DBNAME']
#         # self.conn = None
#         if IS_INSERT:
#             self.pool = self.create_pool()
#             self.condition_re = re.compile('(.*?)\\(')
#             self.params_re = re.compile('\\((.*?)\\)')
#
#     def create_pool(self):
#         conn = ConnectionPool(
#             pool_name='mypool',
#             host=self.host,
#             port=self.port,
#             user=self.user,
#             password=self.password,
#             db=self.db,
#             autocommit=False
#         )
#         return conn
#
#     def execute(self, query, parameters=None, many=False):
#         attempts = 3  # allow 3 attempts to execute the query
#         while attempts > 0:
#             conn = self.pool.borrow_connection()
#             try:
#                 with conn.cursor() as cursor:
#                     if many:
#                         cursor.executemany(query, parameters)
#                     else:
#                         cursor.execute(query, parameters)
#                     conn.commit()
#                     if cursor.lastrowid:
#                         return cursor.lastrowid
#                     else:
#                         return cursor.rowcount
#             except pymysql.OperationalError as e:
#                 if e.args[0] in (2006, 2013):  # MySQL server has gone away
#                     self.pool.close()
#                     self.pool = self.create_pool()
#                     attempts -= 1
#                 else:
#                     raise
#             except Exception as e:
#                 self.logger.error(f"Error while executing query: {e}")
#                 conn.rollback()
#                 attempts -= 1
#                 if attempts == 0:
#                     raise Exception("Failed to execute query after 3 attempts")
#             finally:
#                 self.pool.return_connection(conn)
#                 # if conn:
#                 #     conn.close()
#
#     def insert(self, table, data, if_update=False, is_info=True):
#         columns = ', '.join([f"`{i}`" for i in data.keys()])
#         placeholders = ', '.join(['%s'] * len(data))
#         query = f"INSERT IGNORE INTO `{table}` ({columns}) VALUES ({placeholders});"
#         sql = query % tuple([f"'{i}'" if i else i for i in data.values()])
#         if if_update:
#             update = ', '.join([f"`{key}` = %s" for key in data.keys()])
#             query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update}"
#             sql = query % tuple([f"'{i}'" if i else i for i in data.values()] * 2)
#         if is_info:
#             self.logger.info(sql)
#             self.logger.info('===========================================================')
#         return self.execute(query, tuple(data.values()))
#
#     def update(self, table, set_data, where=None):
#         set_pairs = [f"`{column}`=%s" for column in set_data.keys()]
#         query = f"UPDATE `{table}` SET {', '.join(set_pairs)}"
#         parameters = tuple(set_data.values())
#         if where:
#             query += f" WHERE {where}"
#         sql = query % tuple([f"'{i}'" if i else i for i in parameters])
#         self.logger.info(sql)
#         self.logger.info('===========================================================')
#         return self.execute(query, parameters)
#
#     def delete(self, table, where=None):
#         query = f"DELETE FROM `{table}`"
#         if where:
#             query += f" WHERE {where}"
#         self.logger.info(query)
#         self.logger.info('===========================================================')
#         return self.execute(query)
#
#     def trucate(self, table):
#         sql = f"""TRUNCATE `{table}`;"""
#         return self.execute(sql)
#
#     def get_condition(self, columns):
#         condition_map = {'count': 'count', 'max': 'max', 'min': 'min', 'sum': 'sum', 'avg': 'avg',
#                          'distinct': 'distinct'}
#         condition = ''
#         if isinstance(columns, list):
#             columns = ', '.join([f"`{i}`" for i in columns])
#         elif isinstance(columns, str):
#             condition = self.deal_re(self.condition_re.search(columns))
#             condition_exis = True if [True for i in condition_map.keys() if i.upper() in columns.upper()] else False
#             if not condition_exis:
#                 columns = ', '.join(f'`{i.strip(" ")}`' for i in columns.split(','))
#         return condition_map, condition, columns
#
#     def select(self, table, columns='*', where=None, order_by=None, limit=None, offset=None):
#         condition_map, condition, columns = self.get_condition(columns)
#         query = f"SELECT {columns} FROM `{table}`"
#         if where:
#             query += f" WHERE {where}"
#         if order_by:
#             query += f" ORDER BY {order_by}"
#         if limit:
#             query += f" LIMIT {limit}"
#         if offset:
#             query += f" OFFSET {offset}"
#         self.logger.info('查询字段：' + query)
#         self.logger.info('===========================================================')
#         with self.pool.cursor() as cursor:
#             cursor.execute(query)
#             data = cursor.fetchall()
#             if self.judge_er(condition):
#                 condition_map = [i.upper() for i in condition_map.keys()]
#             if f'{condition}' in condition_map:
#                 data = data[0].get(columns)
#             return data
#
#     def judge_er(self, str_data):
#         if str_data.isupper():
#             return True
#         else:
#             return False


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
        self.pwd = os.getcwd()
        self.spider_path = os.path.join(self.pwd, f'{self.name}.py')

    def key_judge(self, item):
        key_list = ['title', 'url', 'source', 'html']
        if isinstance(item, BiddingItem):
            item = item.dict()
        for k in key_list:
            sgin = item.__contains__(k)
            while not sgin:
                return False
        return True

    def value_judge(self, item):
        key_list = ['title', 'url', 'source', 'html']
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
        if (key_judge == True and value_judge == True) or (
                item.get('project_name') and self.spider_sign):
            if self.pages:
                item['monitor'] = True
            if self.online and not self.monitor:
                topic = kafka_servers['topic'] if key_judge and value_judge else 'proposed_tasks_mid'
                self.producer.send(topic, json.dumps(item).encode('utf-8'))
            self.prints(item, is_replace=False, db='kafka', sgin='data_test' if not self.online else '')
            # self.add_url_sha1(item['url']) if not item.get('show_url') else (self.add_url_sha1(item['url']), self.add_url_sha1(item.get('show_url'), sgin='show_'))
            self.right_count += 1
        else:
            debug_info = value_judge
            if (not key_judge and not value_judge) or self.spider_sign:
                debug_info = 'project_name'
            self.miss_filed = debug_info
            self.logger.debug(
                f'\033[5;31;1m{debug_info} \033[5;33;1mfield does not exist, Data validation failed, please check！\033[0m {item}')
            self.error_count += 1
        self.catch_count += 1


class RedisDb(ParentObj):
    def __init__(self, key='', custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        self.key = 'ysh_' + key
        self.callback_map = {}  # 回调函数优先级map表
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        if redis_connection:
            if len(REDIS_HOST_LISTS) == 1:
                for k, v in REDIS_HOST_LISTS[0].items():
                    # self.pool = redis.ConnectionPool(host=k, port=v, db=8, decode_responses=True)
                    # self.r = redis.Redis(connection_pool=self.pool)

                    self.r = redis.Redis(host=k, port=v, password='dADM1QUHjD@',
                                         db=8, socket_timeout=None,
                                         connection_pool=None, charset='utf8', errors='strict',
                                         decode_responses=True,
                                         unix_socket_path=None)
            elif len(REDIS_HOST_LISTS) > 1:
                self.r = RedisCluster(startup_nodes=self.startup_nodes, decode_responses=True)

    def get_len(self, key):
        keys = self.get_keys(key)
        # 每个键的任务数量
        key_len = [(k, self.r.scard(k)) for k in keys]
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
            fun_name = ''
            for k, v in tasks.__dict__.items():
                if (k == 'callback') and (v != None):
                    if (isinstance(v, str)):
                        mess_demo[k] = v
                    else:
                        fun_name = v.__name__
                        mess_demo['callback'] = fun_name
                else:
                    mess_demo[k] = v
            if fun_name not in self.callback_map.keys():
                self.callback_map[fun_name] = mess_demo.get('level') or 0
            tasks = json.dumps(mess_demo, cls=ExpandJsonEncoder)
            # self.r.lpush(new_key, tasks)
            self.r.sadd(new_key, tasks)
        elif isinstance(tasks, dict):
            tasks = json.dumps(tasks, cls=ExpandJsonEncoder)
            # self.r.lpush(new_key, tasks)
            self.r.sadd(new_key, tasks)
        else:
            # self.r.lpush(new_key, tasks)
            self.r.sadd(new_key, tasks)


class PriorityQueue(ParentObj):
    def __init__(self, custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        self._queue = []
        self._index = 0
        self.callback_map = {}  # 回调函数优先级map表
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value

    def push(self, item, priority=0):
        # 序列化任务参数
        if (isinstance(item, MyFormRequests)) or (isinstance(item, MyRequests)):
            mess_demo = {}
            fun_name = ''
            for k, v in item.__dict__.items():
                if (k == 'callback') and (v != None):
                    if (isinstance(v, str)):
                        mess_demo[k] = v
                    else:
                        fun_name = v.__name__
                        mess_demo['callback'] = fun_name
                else:
                    mess_demo[k] = v
            if fun_name not in self.callback_map.keys():
                self.callback_map[fun_name] = mess_demo.get('level') or 0
            priority = mess_demo.get('level')
            item = json.dumps(mess_demo, cls=ExpandJsonEncoder)
        heapq.heappush(self._queue, (-priority, self._index, item))  # 添加优先级和索引及元素
        self._index += 1

    def pop(self):
        if self._queue:
            data = heapq.heappop(self._queue)[-1]  # 返回元素不返回优先级和索引
            return data


class EsDb(ParentObj):
    def __init__(self, custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        if IS_ES:
            self.es = Elasticsearch(hosts=ES_CONFIG['host'], port=ES_CONFIG['port'],
                                    http_auth=(ES_CONFIG['user'], ES_CONFIG['password']), request_timeout=60)


class MongoDBManager(ParentObj):
    def __init__(self, custom_settings=None, **kwargs):
        super().__init__(custom_settings=custom_settings, **kwargs)
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        MONGODB_HOST = MONGO_CONFIG['MONGODB_HOST']
        MONGODB_PORT = MONGO_CONFIG['MONGODB_PORT']
        MONGODB_BASE = MONGO_CONFIG['MONGODB_BASE']
        if MONGO_client:
            try:
                self.mongo_client = pymongo.MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
                self.mong_db = self.mongo_client[MONGODB_BASE]
            except (ConnectionFailure, AutoReconnect) as e:
                raise Exception(f"Failed to connect to MongoDB: {e}")

    def insert_data(self, collection_name, data):
        try:
            collection = self.mong_db[collection_name]
            result = collection.insert_one(data)
            return result.inserted_id
        except pymongo.errors.DuplicateKeyError as e:
            raise Exception(f"Failed to insert data: {e}")

    def find_data(self, collection_name, query):
        try:
            collection = self.mong_db[collection_name]
            result = collection.find(query)
            return result
        except Exception as e:
            raise Exception(f"Failed to find data: {e}")

    def find_paginated_data(self, collection_name, page_number, page_size):
        try:
            collection = self.mong_db[collection_name]
            skip_documents = (page_number - 1) * page_size
            result = collection.find().skip(skip_documents).limit(page_size)
            return result
        except Exception as e:
            raise Exception(f"Failed to find data: {e}")

    def update_data(self, collection_name, query, update_data):
        try:
            collection = self.mong_db[collection_name]
            result = collection.update_many(query, {"$set": update_data})
            return result.modified_count
        except Exception as e:
            raise Exception(f"Failed to update data: {e}")

    def delete_data(self, collection_name, query):
        try:
            collection = self.mong_db[collection_name]
            result = collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            raise Exception(f"Failed to delete data: {e}")


class Cluster(Mysqldb, KafkaDb, RedisDb, PriorityQueue, EsDb, MongoDBManager):
    def __init__(self, key='', custom_settings=None, **kwargs):
        super().__init__(key=key, custom_settings=custom_settings, **kwargs)


if __name__ == '__main__':
    database = Cluster()

    # for i in range(10):
    #     database.insert(table='db_base_test', data={'name': 'yuanshaohang', 'age': None, 'sex': '男'})  # 增
    #
    # database.update(table='db_base_test', set_data={'name': '袁少航', 'age': 20, 'sex': '男'}, where="`name`='yuanshaohang'")  # 改
    #
    database.delete(table='weihu_website', where="`description` = '超过三个小时未结束'")  # 删
    #
    # data_list = database.select(table='db_base_test', columns='name', where='`name` = "袁少航"')  # 查
    # print(data_list)
    # query = {'_source': ['domain'], 'size': 1, 'query': {'match_phrase': {'source': '大邑县人民政府'}}}
    # print(database.es.search(index='bidding-source', body=query), 'hits.hits[0]._source.domain')
