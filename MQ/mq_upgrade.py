# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2023-02-23- 09:56:50
# @Version: 1.0.0
# @Description: rabbitmq队列中间件

import sys
import time
import pika
import json
import requests
import threading
from queue import Queue
from library_tool.sugars import retrying
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from items import *
from asyncio_config.my_Requests import MyFormRequests, MyRequests
from config.settings import Rabbitmq


class MqProducer:
    def __init__(self, queue_name, custom_settings=None):
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        self.rabbit_username = Rabbitmq.get('username')  # 连接mq的各项参数
        self.rabbit_password = Rabbitmq.get('password')  # 连接mq的各项参数
        self.rabbit_host = Rabbitmq.get('host')  # 连接mq的各项参数
        self.rabbit_port = Rabbitmq.get('port')  # 连接mq的各项参数
        self.vhost_check = '%2F'  # 连接mq的各项参数
        self.async_thread_pool = ThreadPoolExecutor(Rabbitmq['async_thread_pool_size'])  # 线程池
        self.connections = Queue(maxsize=100)  # 连接池
        self.lock = threading.Lock()  # 线程锁
        self.work_list = []  # 线程子任务池
        self.operating_system = sys.platform  # 运行平台
        self.pages = sys.argv[1] if len(sys.argv) > 1 else None
        self.queue_name = self.make_queue_name(queue_name)
        self.req_s = requests.session()

    def conn(self):
        """建立连接"""
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbit_host, port=self.rabbit_port,
                credentials=pika.credentials.PlainCredentials(self.rabbit_username, self.rabbit_password), heartbeat=0
            )
        )
        return connection

    def get_connection(self):
        """构造连接池并获取连接"""
        if not self.connections.full():
            self.lock.acquire()
            try:
                if not self.connections.full():
                    connection = self.conn()
                    self.connections.put(connection)
            finally:
                self.lock.release()
        return self.connections.get(block=True)

    def return_connection(self, connection):
        """重新连接后放到连接池里"""
        self.connections.put(connection)

    def reconnect(self, connection):
        """重练机制"""
        # print('开始重连')
        try:
            connection.close()
            connection = self.conn()
            self.return_connection(connection)
        except:
            pass

    def make_queue_name(self, queue_name):
        """构造queue_name"""
        sgin = Rabbitmq['Sgin']
        queue_name = (
            sgin + '_' + queue_name + '_online' if self.operating_system == 'linux' else sgin + '_' + queue_name) if not self.pages else (
            sgin + '_' + queue_name + '_online_add' if self.operating_system == 'linux' else sgin + '_' + queue_name + '_add')
        return queue_name

    def make_data(self, message):
        """构造消息体"""
        if (isinstance(message, MyFormRequests)) or (isinstance(message, MyRequests)):
            mess_demo = {}
            for k, v in message.__dict__.items():
                if (k == 'callback') and (v != None):
                    if (isinstance(v, str)):
                        mess_demo[k] = v
                    else:
                        fun_name = v.__name__
                        mess_demo['callback'] = fun_name
                elif (k == 'meta') and len(v) != 0:
                    for key, value in v.items():
                        if isinstance(value, BiddingItem) or isinstance(value, ProposedItem):
                            mess_demo[k] = dict(v, **{key: json.dumps(value, default=self.obj_json)})
                            break
                        elif not isinstance(value, BiddingItem) and not isinstance(value, ProposedItem) and len(v) > 1:
                            mess_demo[k] = v
                        else:
                            mess_demo[k] = {}
                            mess_demo[k][key] = value
                else:
                    mess_demo[k] = v
            mess_last = json.dumps(mess_demo)
            return mess_last, mess_demo.get('level') or 0

        elif isinstance(message, str) or isinstance(message, int):
            return str(message), 0

    @retrying(stop_max_attempt_number=Rabbitmq['max_retries'])  # 重试装饰器
    def send_message(self, message, befor_fun=reconnect, befor_parmas=conn):
        """生产者"""
        message, level = self.make_data(message)
        with self.get_connection() as connection:
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name,
                                  arguments={'x-max-priority': (Rabbitmq['X_MAX_PRIORITY'] or 0),
                                             'x-queue-mode': 'lazy', 'x-message-ttl': Rabbitmq['message_ttl']},
                                  durable=True)

            channel.basic_publish(exchange='', routing_key=self.queue_name, body=message,
                                  properties=pika.BasicProperties(priority=level, delivery_mode=1))
            # print(f"已发送消息：{message}, {time.time()}")
            # time.sleep(0.001)

    def async_send_message(self, message):
        """异步发送消息"""
        # self.work_list.append(
        #     self.async_thread_pool.submit(self.send_message, message=message, befor_fun=self.reconnect,
        #                                   befor_parmas=self.conn))
        self.async_thread_pool.submit(self.send_message, message=message)

    @retrying(stop_max_attempt_number=Rabbitmq['max_retries'])  # 重试装饰器
    def get_message(self, befor_fun=reconnect, befor_parmas=conn):
        """消费者"""
        with self.get_connection() as connection:
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name,
                                  arguments={'x-max-priority': (Rabbitmq['X_MAX_PRIORITY'] or 0),
                                             'x-queue-mode': 'lazy', 'x-message-ttl': Rabbitmq['message_ttl']},
                                  durable=True)
            channel.basic_qos(prefetch_count=1)  # 让rabbitmq不要一次将超过1条消息发送给work
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.Requests)
            channel.start_consuming()

    def obj_json(self, obj):
        """json格式化调用函数"""
        data = obj.__dict__
        data['item_name'] = obj.__class__.__name__
        return data

    def handle(self, obj):
        item_name = obj.get('item_name')
        if item_name:
            del obj['item_name']
            item = globals()[item_name]()
            for k, v in obj.items():
                if hasattr(item, k):
                    setattr(item, k, v)
                else:
                    raise AttributeError(f'{item_name} has no attribute {k}')
            return item
        else:
            return obj

    def getMessageCount(self, queue_name):
        # 返回3种消息数量：ready, unacked, total
        url = 'http://%s:15672/api/queues/%s/%s' % (self.rabbit_host, self.vhost_check, queue_name)
        r = self.req_s.get(url, auth=(self.rabbit_username, self.rabbit_password))
        if r.status_code != 200:
            return 0, 0, 0
        dic = json.loads(r.text)
        # print(dic)
        try:
            return dic['messages']
        except KeyError:
            import traceback
            traceback.print_exc()
            return 0

    def delete_queue(self, queue_name):
        url = f'http://{self.rabbit_host}:15672/api/queues/%2F/{queue_name}'
        # url = f'http://{self.rabbit_host}/api/queues/%2F/{queue_name}'
        data = {"vhost": "/", "name": f"{queue_name}", "mode": "delete"}
        self.req_s.delete(url=url, json=data, auth=(self.rabbit_username, self.rabbit_password))

    def start(self):
        """开始发送消息"""
        for i in range(100):
            message = i
            # self.send_message(str(message))  # 单进程发送
            self.async_send_message(message)  # 线程池发送

        ret = wait(fs=self.work_list, timeout=None, return_when=ALL_COMPLETED)
        print(f"work_list ALL_COMPLETED, ret:{ret}")

        while self.work_list:
            task = self.work_list[-1]
            if task.done():
                self.work_list.remove(task)
            else:
                continue

        # print(len(self.work_list))
        # self.async_send_message('1')

    def Requests(self, ch, method, properties, body):  # 消息处理函数
        print(['X'], body.decode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动发送ack,如果没有发送,队列里的消息将会发给下一个worker


if __name__ == '__main__':
    start_time = time.time()
    producer = MqProducer(queue_name='test_queue')
    producer.start()
    producer.get_message()
    end_time = time.time()
    total = (end_time - start_time)
    print(total)

    # from retrying import retry
    # from random import randint
    #
    #
    # @retry(stop_max_attempt_number=3)
    # def get_random():
    #     int_r = randint(0, 100)
    #     if int_r > 0:
    #         print(f"该随机数等于{int_r}")
    #         raise IOError("该随机数大于0")
    #     else:
    #         return int_r
    #
    #
    # print(f"该随机数等于{get_random()}")
