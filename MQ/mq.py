# -*- coding: utf-8 -*-
import pika
import json
import time
import requests
import asyncio_config
from asyncio_config.my_Requests import MyResponse, MyFormRequests, MyRequests
from config.settings import Rabbitmq, PREFETCH_COUNT, IS_connection, X_MAX_PRIORITY

class Mq(object):
    def __init__(self, queur_name, custom_settings=None):
        global Rabbitmq
        global PREFETCH_COUNT
        global IS_connection
        global X_MAX_PRIORITY
        if custom_settings:
            if custom_settings.get('Rabbitmq'):
                Rabbitmq = custom_settings.get('Rabbitmq')
            if custom_settings.get('PREFETCH_COUNT'):
                PREFETCH_COUNT = custom_settings.get('PREFETCH_COUNT')
            if custom_settings.get('IS_connection'):
                IS_connection = custom_settings.get('IS_connection')
            if custom_settings.get('X_MAX_PRIORITY'):
                X_MAX_PRIORITY = custom_settings.get('X_MAX_PRIORITY')
        if IS_connection == False:
            raise ('请先打开rabbitmq连接权限')
        else:
            self.queue_name = queur_name
            self.vhost_check = '%2F'
            self.s = requests.session()
            self.rabbit_user = Rabbitmq['user']
            self.rabbit_password = Rabbitmq['password']
            self.rabbit_host = Rabbitmq['host']
            self.credentials = pika.PlainCredentials(username=self.rabbit_user, password=self.rabbit_password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, credentials=self.credentials, heartbeat=0, socket_timeout=30))
            self.channel = self.connection.channel()
            self.send_channel = self.connection.channel()
            self.send_channel_count = self.send_channel.queue_declare(queue=self.queue_name, arguments={'x-max-priority': (X_MAX_PRIORITY or 0)}, durable=True, exclusive=False, auto_delete=False)

    def is_json(self, myjson):
        if '{' not in myjson:
            return False
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def send_mqdata(self, mess, level=0, queue_name=None):  # 生产者
        # 将声明队列持久话,rabbitmq不允许同名队列
        if queue_name != None:
            self.queue_name = queue_name
        if (isinstance(mess, MyFormRequests)) or (isinstance(mess, MyRequests)):
            mess_demo = {}
            for k, v in mess.__dict__.items():
                if k == 'callback':
                    if (isinstance(v, str)):
                        mess_demo[k] = v
                    else:
                        fun_name = v.__name__
                        mess_demo['callback'] = fun_name
                else:
                    mess_demo[k] = v
            mess_last = json.dumps(mess_demo)
            self.send_channel.basic_publish(exchange='',
                                  routing_key=self.queue_name,
                                  body=mess_last,
                                  properties=pika.BasicProperties(priority=mess.level, delivery_mode=2))  # 使消息持久化
            # print('[x] {tt} send %r to %s'.format(tt=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))%(mess_last, self.queue_name))
        else:
            self.send_channel.basic_publish(exchange='',
                                            routing_key=self.queue_name,
                                            body=mess,
                                            properties=pika.BasicProperties(priority=level, delivery_mode=2))  # 使消息持久化
            # print('[x] {tt} send %r to %s'.format(tt=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))%(mess, self.queue_name))
        # self.connection.close()

    def get_mqdata(self, queue_name, callback):  # 消费者
        self.channel.queue_declare(queue=queue_name, durable=True)
        # print('[*] Watting for messages, to exit press CTRL+C.')
        self.channel.basic_qos(prefetch_count=PREFETCH_COUNT)  # 让rabbitmq不要一次将超过1条消息发送给work
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        self.channel.start_consuming()

    # def getMessageCount(self, queue_name):
    #     # 返回3种消息数量：ready, unacked, total
    #     url = 'http://%s:15672/api/queues/%s/%s' % (self.host, self.vhost_check, queue_name)
    #     r = self.s.get(url, auth=(self.user, self.password))
    #     if r.status_code != 200:
    #         print('队列名为：', queue_name, '的状态码为：', r.status_code, '请视情况决定是否检查!')
    #         return 0, 0, 0
    #     dic = json.loads(r.text)
    #     try:
    #         return dic['messages_ready'], dic['messages_unacknowledged'], dic['messages']
    #     except KeyError:
    #         return 0, 0, 0

if __name__ == '__main__':
    mm = Mq('ysh_shixin_limit_pages')
    print(mm.send_channel_count.method.message_count)