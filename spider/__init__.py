# -*- coding: utf-8 -*-
import json
import os
import sys

import demjson

sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from tkinter import _flatten

class DataComparisonSpider(Manager):
    name = 'data_comparison'
    custom_settings = {
        'Waiting_time': 180
    }

    def __init__(self):
        Manager.__init__(self)
        # self.es_port = 9200 if self.operating_system == 'linux' else 59200
        self.es_port = 59200
        self.ES_CONFIG = [
            # f'bailian-aliyun-org-es003.bl-ai.com:{self.es_port}'
            "aliyun-es.bl-ai.com:9200"
        ]
        self.es = Elasticsearch(self.ES_CONFIG, timeout=60, http_auth=('elastic', "jjMv2XcV-UGk"))
        self.index = 'bidding-source-2020-08'

    def per_dic_plus(self, dic_data, key_list):
        data = ''
        for key in key_list:
            da = dic_data.get(key)
            if da:
                data = da
                break
        return data

    def start_requests(self):
        a = ['三明市气象局', '安徽省地矿置业有限责任公司', '抚顺市顺城区人民政府', '湖北省鄂旅投旅游发展股份有限公司', '佛山市高明区农业农村局', '四川棉麻集团有限公司', '国采e网', '公采云',
             '青海煤炭地质局', '南安市人民政府', '湛江市公共资源交易中心', '菏泽市公共资源配置服务中心', '山东省政府采购网', '金华市公共资源交易中心兰溪市分中心', '石狮市总医院',
             '浙江公共资源交易服务平台', '定西市公共资源交易中心', '临夏州公共资源交易中心', '怀远县魏庄镇政府', '广州市政府采购平台', '桐城市发展和改革委员会', '西华师范大学资产经营有限责任公司',
             '厦门消防网', '邵阳市城市建设投资经营集团有限公司', '贵州理工学院工程训练中心']
        for b in a:
            body = {

                "_source": ["source", "pub_time", "title", "url", "data", "html", "show_url"],
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "source": "{}".format(b)
                                }
                            }
                        ],
                        "filter": {
                            "exists": {"field": "data"}

                        }

                    },

                },
            }
            self.send_mqdata(str(body), is_thread=True)

    def parse_only(self, body):
        query = demjson.decode(body)
        results = scan(self.es, index=self.index, query=query)
        # print(len(list(results)))
        for i in results:
            print(i)
        #     dict_data = i.get('_source')
        #     pdf_data_text = list(_flatten(dict_data.get('data')))
        #     dict_data['data'] = pdf_data_text
        #     # print(dict_data)
        #     self.kafka_producer(i['_source'])


if __name__ == '__main__':
    start_run = DataComparisonSpider()
    start_run.run()
