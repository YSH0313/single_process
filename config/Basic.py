# -*- coding: utf-8 -*-
import time
import re
import os

import json
import logging
import requests

from middleware.proxys import Proxy_midddwaer
from middleware.Cluster import Cluster
# from MQ.mq import Mq
from MQ.mq_upgrade import MqProducer

s = requests.session()


class Basic(Cluster, MqProducer, Proxy_midddwaer):
    name = None
    spider_sign = None

    def __init__(self, queue_name, custom_settings=None, class_name=None):
        if custom_settings:
            if class_name == 'Manager': MqProducer.__init__(self, queue_name=queue_name,
                                                            custom_settings=custom_settings)
            Cluster.__init__(self, key=queue_name, custom_settings=custom_settings)
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        else:
            if class_name == 'Manager': MqProducer.__init__(self, queue_name=queue_name)
            Cluster.__init__(self, key=queue_name)
        self.s = requests.session()
        self.logger.name = logging.getLogger(__name__).name

    def send_start_info(self):
        pass

    def send_close_info(self):
        pass

    def finished_info(self, starttime, start_time, exec_info=False):
        Total_time = time.time() - start_time
        m, s = divmod(Total_time, 60)
        h, m = divmod(m, 60)
        import collections
        close_info = collections.OrderedDict()  # 将普通字典转换为有序字典
        close_info['Request_count'] = f'请求总数  --  {self.request_count}'
        close_info['Request_200_count'] = f'成功总数  --  {self.success_code_count}'
        close_info['Success_count'] = f'抓取总数  --  {self.catch_count}'
        close_info['Right_count'] = f'正确总数  --  {self.right_count}'
        close_info['Error_count'] = f'错误总数  --  {self.error_count}'
        close_info['Mysql_count'] = f'Mysql总数  --  {self.db_success_count}'
        close_info['Kafka_count'] = f'Kafka总数  --  {self.ka_success_count}'
        close_info['Wrong_count'] = f'重试总数  --  {self.wrong_count}'
        close_info['Give_up_count'] = f'放弃总数  --  {self.fangqi_count}'
        close_info['Abnormal_count'] = f'异常码总数  --  {self.exc_count}'
        close_info['Other_count'] = f'其他状态码总数  --  {self.other_count}'
        close_info['Start_time'] = f'开始时间  --  {starttime}'
        close_info['End_time'] = f'结束时间  --  {self.now_time()}'
        close_info['Total_time'] = "总耗时  --  %d时:%02d分:%02d秒" % (h, m, s)
        self.logger.info('\r\n' + json.dumps(close_info, indent=2, ensure_ascii=False))
        # self.spider_info_save(close_info)
        spider_name = self.path_name.replace('_add', '')
        if self.pages:
            if self.error_count and self.catch_count and not exec_info:
                bili = round(self.error_count / self.catch_count, 2)
                if bili > 0.2:
                    baifenbi = '%.f%%' % (bili * 100)
                    self.warring_deal(spider_name=spider_name, baifenbi=baifenbi)
            elif exec_info:
                self.warring_deal(spider_name=spider_name, baifenbi=0)
        # data_bi = round(self.right_count/self.Estimated_total, 2)
        # if data_bi < 0.9:
        #     send_weixin()

    def handle_item(self, close_info):
        start_time = self.select(table='spiderdetails_info', columns='MAX(`start_time`)',
                                 where=f"""spider_name='{self.path_name.replace('_add', '')}'""")
        field_lists = ['request_count', 'request_200_count', 'success_count', 'right_count',
                       'error_count', 'mysql_count', 'kafka_count', 'wrong_count', 'give_up_count',
                       'abnormal_count', 'other_count']
        if start_time:
            data = self.select(table='spiderdetails_info', columns=field_lists,
                               where=f"""spider_name='{self.path_name.replace('_add', '')}' and start_time like '%{self.now_time(is_date=True)}%'""")
        else:
            data = self.select(table='spiderdetails_info', columns=field_lists,
                               where=f"""spider_name='{self.path_name.replace('_add', '')}'""")
        item = {}
        for k, v in close_info.items():
            key = k.lower()
            if key in field_lists and data:
                befor_data = data[0][field_lists.index(key)]
                if befor_data:
                    item[key] = int(befor_data) + int(self.deal_re(re.search('--  (.*)', v, re.S)).replace(' ', ''))
                else:
                    item[key] = self.deal_re(re.search('--  (.*)', v, re.S)).replace(' ', '')
            else:
                if 'time' in key:
                    item[key] = self.deal_re(re.search('--  (.*)', v, re.S))
                else:
                    item[key] = self.deal_re(re.search('--  (.*)', v, re.S)).replace(' ', '')
        return item, start_time

    def spider_info_save(self, close_info):
        item, start_time = self.handle_item(close_info)
        if (not start_time) or (self.now_time(is_date=True) in start_time):
            self.update(table='spiderdetails_info', set_data=item,
                        where=f"""`spider_name`='{self.path_name.replace('_add', '')}' and (`start_time` = '{start_time}' OR `start_time` is NULL)""")
        else:
            info = self.select(table='spiderdetails_info', columns=['spider_name', 'spider_path', 'log_path'],
                               where=f"""spider_name='{self.path_name.replace('_add', '')}'""")
            item.update(info)
            self.insert(table='spiderdetails_info', data=item)

    def warring_deal(self, spider_name, baifenbi):
        now_time = self.now_time(is_date=True)
        item = {'spider_name': spider_name, 'end_time': now_time, 'baifenbi': baifenbi, 'add_time': now_time}
        self.insert(table='warring_deal', data=item)


if __name__ == '__main__':
    data_deal = Basic('')
    data_deal.data_deal('二〇一五年十月××日')
    data_deal.logger.info('又成功了')
