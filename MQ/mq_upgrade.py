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
from concurrent.futures import ThreadPoolExecutor

from items import *
from asyncio_config.my_Requests import MyFormRequests, MyRequests
from settings import Rabbitmq, message_ttl, Auto_clear, X_MAX_PRIORITY


class MqProducer:
    def __init__(self, queue_name, custom_settings=None):
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        self.rabbit_username = Rabbitmq['username']  # 连接mq的各项参数
        self.rabbit_password = Rabbitmq['password']  # 连接mq的各项参数
        self.rabbit_host = Rabbitmq['host']  # 连接mq的各项参数
        self.rabbit_port = Rabbitmq['port']  # 连接mq的各项参数
        self.vhost_check = '%2F'  # 连接mq的各项参数
        self.async_thread_pool = ThreadPoolExecutor()  # 线程池
        self.connections = Queue(maxsize=10)  # 连接池
        self.lock = threading.Lock()  # 线程锁
        self.work_list = []  # 线程子任务池
        self.operating_system = sys.platform  # 运行平台
        self.pages = sys.argv[1] if len(sys.argv) > 1 else None
        self.queue_name = self.make_queue_name(queue_name)
        self.req_s = requests.session()
        self.callback_map = {}  # 回调函数优先级map表

        if Auto_clear:
            self.delete_queue()

        self.send_channel = self.conn()

        self.thread_channel = self.conn()

    def obj_json(self, obj):
        """json格式化调用函数"""
        data = obj.__dict__
        data['item_name'] = obj.__class__.__name__
        return data

    def handle(self, obj):
        """处理特殊meta参数"""
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

    def getMessageCount(self):
        # 返回3种消息数量：ready, unacked, total
        url = 'http://%s:15672/api/queues/%s/%s' % (self.rabbit_host, self.vhost_check, self.queue_name)
        r = self.req_s.get(url, auth=(self.rabbit_username, self.rabbit_password))
        if r.status_code != 200:
            return 0, 0, 0
        dic = json.loads(r.text)
        count = dic.get('messages', 0)
        # print('队列长度', count)
        return count

    def rm_task(self):
        """移除已结束的线程子任务池"""
        [self.work_list.remove(i) for i in self.work_list if i.done()]

    def delete_queue(self):
        channel = self.conn()
        channel.queue_delete(self.queue_name)

    def channel_declare(self, channel):
        """对队列进行声明"""
        return channel.queue_declare(queue=self.queue_name,
                                     arguments={'x-max-priority': (X_MAX_PRIORITY or 0),
                                                'x-queue-mode': 'lazy', 'x-message-ttl': message_ttl},
                                     durable=True)

    def conn(self):
        """建立连接"""
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbit_host, port=self.rabbit_port,
                credentials=pika.credentials.PlainCredentials(self.rabbit_username, self.rabbit_password), heartbeat=0
            )
        )
        channel = connection.channel()
        self.channel_declare(channel)
        return channel

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
        return self.connections.get()

    def return_connection(self, connection):
        """重新连接后放到连接池里"""
        self.connections.put(connection)

    def reconnect(self, conn_user):
        """重连机制"""
        # print('开始重连')
        try:
            if conn_user == 'get_message':
                connection = self.conn()
                self.return_connection(connection)
            elif conn_user == 'send_message':
                self.send_channel = self.conn()
                self.thread_channel = self.conn()
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
            fun_name = ''
            for k, v in message.__dict__.items():
                if (k == 'callback') and v:
                    if isinstance(v, str):
                        fun_name = v
                    else:
                        fun_name = v.__name__
                    mess_demo[k] = fun_name
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
            if fun_name not in self.callback_map.keys():
                self.callback_map[fun_name] = mess_demo.get('level') or 0
            mess_last = json.dumps(mess_demo)
            return mess_last, mess_demo.get('level') or 0

        elif isinstance(message, str) or isinstance(message, int):
            return str(message), 0

    @retrying(stop_max_attempt_number=Rabbitmq['max_retries'], befor_fun=reconnect, befor_parmas='send_message')  # 重试装饰器
    def send_message(self, message, is_thread=False):
        """生产者"""
        message, level = self.make_data(message)
        channel = self.send_channel
        if is_thread:
            channel = self.thread_channel
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=message,
                                        properties=pika.BasicProperties(priority=level, delivery_mode=1))
        # print(f"已发送消息：{message}, {time.time()}")

    @retrying(stop_max_attempt_number=Rabbitmq['max_retries'], befor_fun=reconnect, befor_parmas='get_message')  # 重试装饰器
    def get_message(self):
        """消费者"""
        with self.get_connection() as channel:
            channel.basic_qos(prefetch_count=1)  # 让rabbitmq不要一次将超过1条消息发送给work
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.Requests)
            channel.start_consuming()

    def async_send_message(self, message):
        """异步发送消息"""
        self.async_thread_pool.submit(self.send_message, message=message)

    def start(self, **kwargs):
        """开始发送消息"""
        for i in range(100):
            message = i
            self.send_message(str(message), **kwargs)  # 单进程发送
            # self.async_send_message(message)  # 线程池发送

    def Requests(self, ch, method, properties, body):  # 消息处理函数
        print(['X'], body.decode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动发送ack,如果没有发送,队列里的消息将会发给下一个worker

        # print(self.getMessageCount())

    def rrr(self):
        self.async_thread_pool.submit(self.start)
        self.async_thread_pool.submit(self.get_message)
        # print('==================================================')
        # self.async_thread_pool.submit(self.start, is_thread=True)


if __name__ == '__main__':
    start_time = time.time()
    producer = MqProducer(queue_name='first_spider')
    producer.rrr()
    end_time = time.time()
    total = (end_time - start_time)
    print(total)
