# -*- coding: utf-8 -*-
import re
import pika
import socket
import aiohttp
import asyncio
import actuator
import datetime
from config.data_deal import Deal
from asyncio_config.th_read import *
from config.proxys import asy_rand_choi_pool
from asyncio_config.my_Requests import MyResponse
from config.settings import PREFETCH_COUNT, TIME_OUT, X_MAX_PRIORITY, Mysql, IS_PROXY, IS_SAMEIP

socket.timeout=TIME_OUT
class Manager(Deal):
    def __init__(self, queue_name):
        Deal.__init__(self, queue_name=queue_name)
        self.num = PREFETCH_COUNT
        self.timeout = TIME_OUT
        self.x_max_priority = X_MAX_PRIORITY
        self.mysql = Mysql
        self.is_proxy = IS_PROXY
        self.is_sameip = IS_SAMEIP
        self.new_loop = asyncio.new_event_loop()
        # 定义一个线程，运行一个事件循环对象，用于实时接收新任务
        self.loop_thread = threading.Thread(target=self.start_loop, args=(self.new_loop,))
        self.loop_thread.setDaemon(True)
        self.loop_thread.start()
        self.duixiang = None
        self.charset_code = re.compile(r'charset=(.*?)"', re.S)

    def start_loop(self, loop):
        self.send_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, credentials=self.credentials, heartbeat=0, socket_timeout=30))
        self.send_channel = self.send_connection.channel()
        # 一个在后台永远运行的事件循环
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def open_spider(self, spider_name):
        data = self.select_data(field_lists=['spider_name', 'interval_time', 'incremental', 'is_run', 'end_time', 'server_name', 'owner'], db_name=self.mysql['MYSQL_DBNAME'], table='single_process_listener', where="""spider_name = '{spider_name}'""".format(spider_name=spider_name))
        if data:
            self.update_data({'is_run': 'yes'}, self.mysql['MYSQL_DBNAME'], 'single_process_listener', where="""`spider_name` = '{spider_name}'""".format(spider_name=spider_name))
            print('\033[1;31;0m' + spider_name + '爬虫程序启动\033[0m', data[0])
            return True
        else:
            print('\033[1;31;0m如需开启增量，请先在注册表里注册后再次尝试运行，不需要请忽略\033[0m')
            print('\033[1;31;0m' + spider_name + '爬虫程序启动\033[0m')
            return True

    def run(self, spider_name):
        self.duixiang = actuator.LoadSpiders()._spiders[spider_name]()
        if hasattr(self.duixiang, "custom_settings"):
            Deal.__init__(self, queue_name=self.queue_name, custom_settings=self.duixiang.custom_settings)
            for k, v in self.duixiang.custom_settings.items():
                if 'PREFETCH_COUNT' == k:
                    self.num = v
                if 'TIME_OUT' == k:
                    self.timeout = v
                if 'X_MAX_PRIORITY' == k:
                    self.x_max_priority = v
                if 'Mysql' == k:
                    self.mysql = v
                if 'IS_PROXY' == k:
                    self.is_proxy = v
                if 'IS_SAMEIP' == k:
                    self.is_sameip = v
        starttime = datetime.datetime.now()
        status = self.open_spider(spider_name)
        # status = True
        if status == True:
            if hasattr(self.duixiang, "custom_settings"):
                if 'Breakpoint' in self.duixiang.custom_settings.keys():
                    start_th([self.duixiang.start_requests], self.queue_name, self.duixiang.custom_settings['Breakpoint'])
            else:
                start_th([self.duixiang.start_requests], self.queue_name)
            self.consumer(self.queue_name)
            self.close_spider(spider_name)
            endtime = datetime.datetime.now()
            print('\033[1;31;0m总用时:\033[0m', endtime - starttime, '分')
        elif status == False:
            return

    def close_spider(self, spider_name):
        self.update_data({'is_run': 'no', 'end_time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))}, db_name=self.mysql['MYSQL_DBNAME'], table='single_process_listener', where="""`spider_name` = '{spider_name_demo}'""".format(spider_name_demo=spider_name))
        print('\033[1;31;0m' + spider_name + '爬虫程序关闭\033[0m', self.now_time())
        return

    def start_requests(self):
        pass

    def parse(self, response):
        pass

    def parse_only(self, body):
        pass

    def consumer(self, queue_name):  # 消费者
        while 1:
            try:
                self.channel.queue_declare(queue=queue_name, arguments={'x-max-priority': (self.x_max_priority or 0)}, durable=True)
                self.channel.basic_qos(prefetch_count=1)  # 让rabbitmq不要一次将超过1条消息发送给work
                self.channel.basic_consume(queue=queue_name, on_message_callback=self.Requests)
                self.channel.start_consuming()
            except Exception as e:
                # raise e
                print('\033[1;31;0m{info}\033[0m'.format(info=self.now_time()+repr(e)+'channel丢失，正在重连'))
                self.credentials = pika.PlainCredentials(username=self.rabbit_user, password=self.rabbit_password)
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host, credentials=self.credentials, heartbeat=0))
                self.channel = self.connection.channel()
                self.send_channel = self.connection.channel()
                self.send_channel_count = self.send_channel.queue_declare(queue=queue_name, arguments={'x-max-priority': (self.x_max_priority or 0)}, durable=True, exclusive=False, auto_delete=False)

    def Requests(self, ch, method, properties, body):
        self.num -= 1
        while self.num <= 0:
            print('请求队列已满，等待中')
            time.sleep(1)
        flag = self.is_json(body.decode('utf-8'))
        if flag == False:
            self.parse_only(body.decode('utf-8'))
            ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动发送ack,如果没有发送,队列里的消息将会发给下一个worker
            self.num += 1
        if (flag == True):
            contents = json.loads(body.decode('utf-8'))
            callback_demo = contents.get('callback')
            url = contents.get('url')
            headers = contents.get('headers')
            data = contents.get('data')
            timeout = contents.get('timeout')
            meta = contents.get('meta')
            level = contents.get('level')
            proxy = contents.get('proxy')
            if meta:
                if meta.get('proxy'):
                    proxy = meta['proxy']
            else:
                meta = {}
            if contents.get('types') == 'POST': types = 'POST'
            else:
                types = 'GET'
            if timeout: timeout = timeout
            else:
                timeout = self.timeout
            ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动发送ack,如果没有发送,队列里的消息将会发给下一个worker
            asyncio.run_coroutine_threadsafe(self.start_Requests(types=types, url=url, body=body, headers=headers,
                                                                 data=data, timeout=timeout, callback=callback_demo,
                                                                 meta=meta, level=level, proxy=proxy, request_info=body.decode('utf-8')), self.new_loop)

    async def start_Requests(self, types='GET', url=None, body=None, headers=None, data=None, cookies=None, timeout=None,
                             callback=None, meta=None, level=0, request_info=None, proxy=None):
        if (proxy == None) and (self.is_sameip == True) and (self.is_proxy == True):
            proxy = await asy_rand_choi_pool()
            meta['proxy'] = proxy
        if (proxy != None) and (self.is_sameip == False) and (self.is_proxy == True):
            proxy = await asy_rand_choi_pool()
        if proxy != None:
            proxy = proxy
        try:
            async with aiohttp.ClientSession(headers=headers, conn_timeout=timeout, cookies=cookies) as session:
                print(self.now_time(), 'INFO: {types} from'.format(types=types), url)
                if (types == 'GET') and (self.is_proxy == True):
                    response = await session.get(url=url, headers=headers, proxy=proxy, verify_ssl=True, timeout=timeout)
                    res = await response.read()
                    if callback == None:
                        charset_code = await self.deal_code(res)
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta,
                                                   text=res.decode(charset_code), content=res,
                                                   status_code=response.status, proxy=proxy)
                        return response_last
                    elif ('img_' in callback) or ('pdf' in url):
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=response.cookies,
                                                   meta=meta, content=res, status_code=response.status, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                    else:
                        charset_code = await self.deal_code(res)
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta,
                                                   text=res.decode(charset_code), content=res,
                                                   status_code=response.status, request_info=request_info, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                    print(self.now_time(), 'DEBUG: status:' + str(response.status), url)

                elif (types == 'GET') and (self.is_proxy == False):
                    response = await session.get(url=url, headers=headers, verify_ssl=True, timeout=timeout)
                    res = await response.read()
                    if callback == None:
                        return res
                    elif 'img_' in callback:
                        response_last = MyResponse(url=url, headers=response.headers, data=data,
                                                   cookies=response.cookies, meta=meta, content=res,
                                                   status_code=response.status, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                    else:
                        charset_code = await self.deal_code(res)
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta,
                                                   text=res.decode(charset_code), content=res,
                                                   status_code=response.status, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                    print(self.now_time(), 'DEBUG: status:' + str(response.status), url)

                elif (types == "POST") and (self.is_proxy == True):
                    if '127.0.0.1' in url:
                        response = await session.post(url=url, headers=headers, data=data, verify_ssl=True, timeout=timeout)
                        res = await response.read()
                    else:
                        response = await session.post(url=url, headers=headers, data=data, proxy=proxy, verify_ssl=True, timeout=timeout)
                        res = await response.read()
                    if callback == None:
                        return res
                    if url == 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list_content.jsp':
                        charset_code = 'gbk'
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta,
                                                   text=res.decode(charset_code), content=res,
                                                   status_code=response.status, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                        print(self.now_time(), 'DEBUG: status:' + str(response.status), url)
                    else:
                        charset_code = await self.deal_code(res)
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta,
                                                   text=res.decode(charset_code), content=res,
                                                   status_code=response.status, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                    print(self.now_time(), 'DEBUG: status:' + str(response.status), url)

                elif (types == "POST") and (self.is_proxy == False):
                    response = await session.post(url=url, headers=headers, data=data, verify_ssl=True, timeout=timeout)
                    res = await response.read()
                    if callback == None:
                        return res

                    else:
                        charset_code = await self.deal_code(res)
                        response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta,
                                                   text=res.decode(charset_code), content=res,
                                                   status_code=response.status, proxy=proxy)
                        self.duixiang.__getattribute__(callback)(response=response_last)
                    print(self.now_time(), 'DEBUG: status:' + str(response.status), url)

        except Exception as e:
            if (('ClientProxyConnectionError' in repr(e)) or ('ServerTimeoutError' in repr(e))) and (IS_PROXY == True):
                print('\033[1;31;0m', self.now_time(), '由于：', repr(e), '正在重回队列\033[0m', body.decode('utf-8'))
                mess = json.loads(body.decode('utf-8'))
                mess['proxy'] = await asy_rand_choi_pool()
                mess['meta']['proxy'] = mess['proxy']
                # mess['level'] = 10
                self.send_mqdata(mess=json.dumps(mess), level=level)
            elif 'PDFSyntaxError' in repr(e):
                response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta, text='PDF无法打开或失效', content=b'', status_code=200, proxy=proxy)
                self.duixiang.__getattribute__(callback)(response=response_last)
            else:
                print('\033[1;31;0m', self.now_time(), '由于：', repr(e), '正在重回队列\033[0m', body.decode('utf-8'))
                self.send_mqdata(mess=body.decode('utf-8'), level=level)
        self.num += 1
        # print(self.num)

    async def deal_code(self, res):
        charset_code = self.deal_re(self.charset_code.search(str(res)))
        if charset_code:
            return charset_code
        else:
            return 'utf-8'