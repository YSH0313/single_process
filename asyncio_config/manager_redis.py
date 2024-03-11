# -*- coding: utf-8 -*-
import re
import os
import ssl
import sys
from itertools import chain

from requests.exceptions import ProxyError

ssl._create_default_https_context = ssl._create_unverified_context
import json
import time
import aiohttp
import asyncio
import chardet  # 字符集检测
import pdfminer
import threading
import logging
import async_timeout
import concurrent.futures
from yarl import URL
from scrapy.selector import Selector
from collections import Iterator
from config.Basic import Basic
from asyncio_config.my_Requests import MyResponse
from concurrent.futures import wait, ALL_COMPLETED
from settings import PREFETCH_COUNT, TIME_OUT, IS_PROXY, IS_SAMEIP, Asynch, Waiting_time, Delay_time, \
    max_request, Agent_whitelist, retry_http_codes, UA_PROXY

shutdown_lock = threading.Lock()


class LoopGetter(object):
    def __init__(self, custom_settings=None):
        if custom_settings:
            for varName, value in custom_settings.items():
                if varName in globals().keys():
                    globals()[varName] = value

        # 定义一个线程，运行一个事件循环对象，用于实时接收新任务
        self.new_loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self.start_loop, args=(self.new_loop,))
        self.loop_thread.setDaemon(True)
        self.loop_thread.start()

        # 定义一个线程，运行一个事件循环对象，用于实时接收新任务
        self.shutdown_loop = asyncio.new_event_loop()
        self.loop_shutdown = threading.Thread(target=self.start_loop, args=(self.shutdown_loop,))
        self.loop_shutdown.setDaemon(True)
        self.loop_shutdown.start()

        self.charset_code = re.compile(r'charset=(.*?)"|charset=(.*?)>|charset="(.*?)"', re.S)
        self.last_time = time.time()
        self.starttime = None
        self.start_run_time = time.time()

    def start_loop(self, loop):
        # 一个在后台永远运行的事件循环
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_requests(self):
        pass

    def parse(self, response):
        pass

    def parse_only(self, body):
        pass

    def close_spider(self, **kwargs):
        pass


class ManagerRedis(Basic, LoopGetter):
    name = None
    spider_sign = None
    custom_settings = {}

    def __init__(self):
        if self.custom_settings:
            Basic.__init__(self, queue_name=self.name, custom_settings=self.custom_settings, class_name='Manager')
            LoopGetter.__init__(self, custom_settings=self.custom_settings)
            for varName, value in self.custom_settings.items():
                if varName in globals().keys():
                    globals()[varName] = value
        else:
            LoopGetter.__init__(self)
            Basic.__init__(self, queue_name=self.name, class_name='Manager')
        self.pages = int(sys.argv[1]) if len(sys.argv) > 1 else None
        self.logger.name = logging.getLogger(__name__).name
        self.num = PREFETCH_COUNT
        self.is_proxy = IS_PROXY
        self.is_sameip = IS_SAMEIP

    def Environmental_judgment(self):
        if self.operating_system == 'linux' and self.pages and len(sys.argv) > 1:
            return True
        else:
            return False

    def start_loop(self, loop):
        # 一个在后台永远运行的事件循环
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def open_spider(self, spider_name: str):
        """开启spider第一步检查状态"""
        data = self.select(table='spiderlist_monitor', columns=['owner', 'remarks'],
                           where=f"""spider_name = '{spider_name}'""")
        if data:
            self.owner = self.per_json(data, '[0].owner')
            self.source = self.per_json(data, '[0].remarks')
        if data and self.operating_system == 'linux' and self.pages and len(sys.argv) > 1:
            self.update(table='spiderlist_monitor', set_data={'is_run': 'yes', 'start_time': self.now_time()},
                        where=f"""`spider_name` = '{spider_name}'""")
            if not self.monitor:
                self.send_start_info()
        elif not data:
            self.logger.info(
                'If you need to turn on increment, please register and try to run again. If not, please ignore it')
            self.logger.info(f'Crawler service startup for {spider_name}')
        self.logger.info('Crawler program starts')
        return True

    def make_start_request(self, start_fun: {__name__}):
        try:
            start_task = self.__getattribute__(start_fun.__name__)()
            if isinstance(start_task, Iterator):
                for s in start_task:
                    # self.send_message(message=s)
                    self.push_task(key=self.key, tasks=s, level=s.__dict__['level'])
        except:
            import traceback
            traceback.print_exc()

    def run(self):
        """启动spider的入口"""
        # package = __import__(self.path+ self.queue_name.replace('ysh_', ''), fromlist=['None'])
        # temp_class = getattr(package, self.queue_name.replace('ysh_', ''))
        # self.duixiang = temp_class()
        # self.duixiang = actuator.LoadSpiders()._spiders[spider_name]()
        self.starttime = self.now_time()
        self.start_time = time.time()
        status = self.open_spider(spider_name=self.name)
        if status:
            """
                暂时停用，或属于逻辑重复代码，待观察
                if 'Breakpoint' in self.custom_settings.keys():  # 如果修改了开启断点参数
                if Asynch:  # 如果是异步生产（一边生产一边消费）
                    self.async_thread_pool.submit(self.make_start_request, start_fun=self.start_requests)

                else:  # 如果不需要异步生产（等生产完之后再开始消费）
                    self.async_thread_pool.submit(self.make_start_request, start_fun=self.start_requests)
                    wait(fs=self.work_list, timeout=None, return_when=ALL_COMPLETED)

            else:  # 如果是默认断点配置"""

            if Asynch:  # 如果是异步生产（一边生产一边消费）
                self.async_thread_pool.submit(self.make_start_request, start_fun=self.start_requests)

            else:  # 如果不需要异步生产（等生产完之后再开始消费）
                self.work_list.append(
                    self.async_thread_pool.submit(self.make_start_request, start_fun=self.start_requests))
                wait(fs=self.work_list, timeout=None, return_when=ALL_COMPLETED)

            # 开启监控队列状态
            asyncio.run_coroutine_threadsafe(self.shutdown_spider(spider_name=self.name), self.shutdown_loop)
            self.consumer_status = self.async_thread_pool.submit(self.consumer_redis)  # 开启消费者
            self.logger.info(f'Consumer thread open {str(self.consumer_status)}')
            self.work_list.append(self.consumer_status)
            wait(fs=self.work_list, timeout=None, return_when=ALL_COMPLETED)

        elif status == False:
            self.logger.info('爬虫任务启动失败，可能是由于检查爬虫状态导致！')

    async def shutdown_spider(self, spider_name: str):
        """监控队列及运行状态"""
        while 1:
            now_time = time.time()
            self.logger.debug(
                f"It's been {round(now_time - self.last_time, 2)} seconds since the last time I took data from the queue. The remaining number of queues is {self.get_len(self.key)[0]}")
            if (now_time - self.last_time >= Waiting_time) and (self.get_len(self.key)[0] == 0):
                try:
                    self.update(table='spiderlist_monitor', set_data={'is_run': 'no', 'end_time': self.now_time()},
                                where=f"""`spider_name` = '{spider_name}'""")
                except Exception as e:
                    self.logger.error("Crawler closed, abnormal update of running status", exc_info=True)
                self.finished_info(self.starttime, self.start_time)  # 完成时的日志打印
                os._exit(0)  # 存疑
                # stop_thread(self.consumer_status)
                # self.r.connection_pool.disconnect()
                break
            time.sleep(Delay_time)

    def consumer_redis(self, keys=None, priority=True):
        '''
        双端队列 右边弹出任务
        :param keys: 键列表，默认为None（将获取所有任务的keys）
        :return:
        '''
        while True:
            temp_keys = keys  # 避免在while循环中修改参数，将keys参数赋值到临时变量
            if not keys:
                temp_keys = self.r.keys()
                temp_keys = list(set([re.sub('-\d+$', '', k) for k in temp_keys if re.findall('\w+-\d+$', k)]))  # 不指定keys，将获取所有任务
            all_keys = list(chain(*[self.get_keys(k) for k in temp_keys]))  # 根据key作为关键字获取所有的键
            if priority:
                all_keys = sorted(all_keys, key=lambda x: int(x.split('-')[-1]), reverse=True)  # 屏蔽任务差异性，只按优先级高到低弹出任务
            if all_keys:
                # task_key, task = self.r.brpop(all_keys)  # 右边弹出任务,优先消费优先级低的
                # task = self.r.blpop(all_keys[0])  # 左边弹出任务，优先消费优先级高的
                task = self.r.spop(all_keys[0])  # 左边弹出任务，优先消费优先级高的

                self.Requests_redis(json.loads(task))

    def Requests_redis(self, message):
        self.last_time = time.time()
        self.num -= 1
        while self.num < 0:
            self.logger.debug('The request queue is full')
            time.sleep(1)
        flag = self.is_json(message)
        if not flag:
            self.async_thread_pool.submit(self.parse_only, body=message)  # 多线程数据处理
            self.num += 1
        if flag:
            contents = message
            callback_demo = contents.get('callback')
            url = contents.get('url')
            headers = contents.get('headers')
            params = contents.get('params')
            data = contents.get('data')
            json_params = contents.get('json_params')
            timeout = contents.get('timeout')
            meta = contents.get('meta')
            level = contents.get('level')
            proxy = contents.get('proxy')
            meta['proxy'] = proxy if proxy else meta.get('proxy')
            verify_ssl = contents.get('verify_ssl')
            allow_redirects = contents.get('allow_redirects')
            is_file = contents.get('is_file')
            retry_count = contents.get('retry_count')
            is_change = contents.get('is_change')
            param = meta, meta.get('proxy') if (meta if meta else {}) else proxy
            meta = param[0]
            proxy = param[1]
            method = 'POST' if contents.get('method') == 'POST' else 'GET'
            timeout = timeout if timeout else TIME_OUT
            asyncio.run_coroutine_threadsafe(self.start_Requests(method=method, url=url, body=contents, headers=headers,
                                                                 params=params, data=data, json_params=json_params,
                                                                 timeout=timeout, callback=callback_demo, meta=meta,
                                                                 level=level, proxy=proxy, verify_ssl=verify_ssl,
                                                                 is_file=is_file, retry_count=retry_count,
                                                                 is_change=is_change,  allow_redirects=allow_redirects,
                                                                 request_info=message), self.new_loop)

    # 请求处理函数
    async def start_Requests(self, method='GET', url=None, body=None, headers=None, params=None, data=None, json_params=None, cookies=None, timeout=None,
                             callback=None, meta=None, level=0, request_info=None, proxy=None, verify_ssl=None, allow_redirects=True, is_file=False, retry_count=0, is_change=False):
        self.is_proxy = True if (len([False for i in Agent_whitelist if i in url]) == 0) and IS_PROXY == True else False
        if self.is_proxy == False:
            proxy = None
        elif self.is_proxy and ((proxy == None) or (is_change)):
            proxy = await self.asy_rand_choi_pool()
            if self.is_sameip:
                meta['proxy'] = proxy
        while (retry_count < max_request):
            try:
                async with aiohttp.ClientSession(headers=headers, conn_timeout=timeout, cookies=cookies) as session:
                    if (method == 'GET'):
                        async with session.get(url=url, params=params, data=data, json=json_params, headers=headers, proxy=proxy, verify_ssl=verify_ssl, timeout=timeout, allow_redirects=allow_redirects) as response:
                            res = await response.read()
                            await self.infos(response.status, method, url)  # 打印日志
                            text = await self.deal_code(res=res, content_type=response.headers['Content-Type'], body=body, is_file=is_file)
                            response_last = MyResponse(url=url, headers=headers, data=data, cookies=response.cookies, meta=meta,
                                                       text=text, content=res, status_code=response.status, request_info=request_info, proxy=proxy, level=level)
                            await self.Iterative_processing(method=method, callback=callback, response_last=response_last, body=body, level=level, retry_count=retry_count)

                    elif (method == "POST"):
                        async with session.post(url=url, headers=headers, data=data, json=json_params, proxy=proxy, verify_ssl=verify_ssl, timeout=timeout, allow_redirects=allow_redirects) as response:
                            res = await response.read()
                            await self.infos(response.status, method, url)  # 打印日志
                            text = await self.deal_code(res=res, content_type=response.headers['Content-Type'], body=body, is_file=is_file)
                            response_last = MyResponse(url=url, headers=headers, data=data, cookies=response.cookies, meta=meta, text=text,
                                                       content=res, status_code=response.status, request_info=request_info, proxy=proxy, level=level)
                            await self.Iterative_processing(method=method, callback=callback, response_last=response_last, body=body, level=level, retry_count=retry_count)
                break
            except (aiohttp.ClientProxyConnectionError, aiohttp.ServerTimeoutError, TimeoutError, concurrent.futures._base.TimeoutError, aiohttp.ClientHttpProxyError, aiohttp.ServerDisconnectedError, aiohttp.ClientConnectorError, aiohttp.ClientOSError, aiohttp.ClientPayloadError) as e:
                if (IS_PROXY == True):
                    retry_count += 1
                    await self.retry(method, url, retry_count, repr(e), body)
                    if self.is_proxy:
                        proxy = await self.asy_rand_choi_pool()
                        if self.is_sameip:
                            meta['proxy'] = proxy

            except pdfminer.pdfparser.PDFSyntaxError as e:
                response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta, text='PDF无法打开或失效', content=b'', status_code=200, proxy=proxy)
                await self.Iterative_processing(method=method, callback=callback, response_last=response_last, body=body, level=level, retry_count=retry_count)

            except Exception as e:
                if (not self.is_proxy) and (max_request):
                    retry_count += 1
                    await self.retry(method, url, retry_count, repr(e), body)
                else:
                    retry_count += 1
                    body['is_change'] = True
                    self.push_task(key=self.key, tasks=body, level=level)
                    self.logger.error('{exc} Returning to the queue {body}'.format(exc=repr(e), body=body), exc_info=True)
        else:
            response_last = MyResponse(url=url, headers=headers, data=data, cookies=cookies, meta=meta, retry_count=retry_count,
                                       text='', content=b'', status_code=None, request_info=request_info, proxy=proxy, level=level)
            await self.Iterative_processing(method=method, callback=callback, response_last=response_last,
                                            body=body, level=level, retry_count=retry_count)
        self.num += 1

    async def deal_code(self, res, body, is_file, content_type=None):  # 编码处理函数
        if is_file:
            text = None
            return text
        # charset_code = chardet.detect(res[0:1])['encoding']
        # charset_code = self.deal_re(self.charset_code.search(str(res)))
        charset_code = content_type.split('=')[-1] if '=' in content_type else 'utf-8'
        if charset_code:
            try:
                text = res.decode(charset_code)
                return text
            except (UnicodeDecodeError, TypeError, LookupError):
                text = await self.cycle_charset(res, body)
                return text
            except Exception as e:
                self.logger.error('{err} Decoding error {body}'.format(err=repr(e), body=body), exc_info=True)
        else:
            text = await self.cycle_charset(res, body)
            return text

    async def cycle_charset(self, res, body):  # 异常编码处理函数
        charset_code_list = ['utf-8', 'gbk', 'gb2312']
        for code in charset_code_list:
            try:
                text = res.decode(code)
                return text
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.logger.error('{err} Decoding error {body}'.format(err=repr(e), body=body), exc_info=True)

    async def Iterative_processing(self, method, callback, response_last, body, level, retry_count):  # 迭代器及异常状态码处理函数
        if (response_last.status_code != 200) and (response_last.status_code in retry_http_codes) and (retry_count < max_request):
            body['retry_count'] = retry_count = int(retry_count) + 1
            if self.is_proxy:
                body['proxy'] = await self.asy_rand_choi_pool()
                if self.is_sameip:
                    body['meta']['proxy'] = body['proxy']

            if (retry_count < max_request):
                self.push_task(key=self.key, tasks=body, level=level)
                await self.retry(method, response_last.url, str(retry_count), 'Wrong status code {status}'.format(status=response_last.status_code), str(body))
                self.exc_count += 1
            elif (retry_count == max_request):
                self.logger.debug('Give up <{message}>'.format(message=body.decode('utf-8')))
                self.fangqi_count += 1
                response_last.retry_count = retry_count
                await self.__deal_fun(callback=callback, response_last=response_last)
            return
        await self.__deal_fun(callback=callback, response_last=response_last)

    async def __deal_fun(self, callback, response_last):
        """回调函数处理"""
        try:
            if response_last.text:
                response_last.xpath = Selector(response=response_last).xpath
            if self.__getattribute__(callback)(response=response_last):
                for c in self.__getattribute__(callback)(response=response_last):
                    c.meta['proxy'] = response_last.meta.get('proxy')
                    callname = c.callback if isinstance(c.callback, str) else c.callback.__name__
                    if not c.level:
                        c.level = self.callback_map[callback]+1 if callback != callname else self.callback_map[callback]
                    # print(f'{callback}优先级：{c.level}')
                    self.push_task(key=self.key, tasks=c, level=c.level)
        except Exception as e:
            self.exec_count += 1
            # self.send_log(req_id=response_last.log_info['req_id'], code='32', log_level='ERROR', url=response_last.url,
            #               message='爬虫逻辑报错',
            #               formdata=self.dic2params(response_last.log_info['params'], response_last.log_info['data'],
            #                                        response_last.log_info['json_params']),
            #               show_url=response_last.meta.get('show_url'))
            # if self.exec_count >= 100 and self.pages:
            #     import os
            #     self.finished_info(self.starttime, self.start_time, exec_info=True)  # 完成时的日志打印
            #     if self.pages:
            #         self.send_close_info()
            #     os._exit(0)
            self.logger.error(e, exc_info=True)

    async def infos(self, status, method, url):  # 日志函数
        self.request_count += 1
        self.logger.info('Mining ({status}) <{method} {url}>'.format(status=status, method=method, url=url))
        if str(status) == '200':
            self.success_code_count += 1
            self.logger.debug('Catched from <{status} {url}>'.format(status=status, url=url))

    async def retry(self, method, url, retry_count, abnormal, message):  # 重试日志函数
        self.logger.debug('Retrying <{method} {url}> (failed {retry_count} times): {abnormal} {message}'.format(method=method, url=url, retry_count=retry_count, abnormal=abnormal, message=message))
        self.wrong_count += 1