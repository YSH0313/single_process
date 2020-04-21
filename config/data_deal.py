# -*- coding: utf-8 -*-
import time
import re
import xlrd
import json
import requests
import hashlib
import datetime
from config.proxys import rand_choi_pool
from scrapy.selector import Selector
from config.Cluster import Cluster
from config.settings import IS_PROXY, max_request, redis_connection
from MQ.mq import Mq

s = requests.session()
class Deal(Cluster, Mq):
    def __init__(self, queue_name, custom_settings=None):
        global IS_PROXY
        global max_request
        global redis_connection
        Cluster.__init__(self)
        if custom_settings:
            Mq.__init__(self, queur_name=queue_name, custom_settings=custom_settings)
        else:
            Mq.__init__(self, queur_name=queue_name)
        self.s = requests.session()
        if custom_settings:
            if custom_settings.get('IS_PROXY'):
                IS_PROXY = custom_settings['IS_PROXY']
            if custom_settings.get('max_request'):
                max_request = custom_settings['max_request']
            if custom_settings.get('redis_connection'):
                redis_connection = custom_settings['redis_connection']

        if redis_connection != False:
            self.r = Cluster().r
            self.anyou_lists = self.r.lrange('anyou', 0, -1)
            self.lawyer_lists = self.r.lrange('lawyer', 0, -1)
        self.caseno = re.compile(r'(（ *?\d{4} *?）.{5,20}号)|(\( *?\d{4} *?\).{5,20}号)|(^\d{4}.{5,20}号)|(\[ *?\d{4} *?\].{5,20}号)', re.S)

    def try_request(self, url, headers=None):
        try:
            if IS_PROXY == False:
                response = self.s.post(headers=headers, url=url, timeout=15)
            else:
                # response = s.get(url=url, headers=headers, timeout=30)
                response = self.s.get(url=url, headers=headers, proxies=rand_choi_pool(), timeout=30)
            response.encoding = 'utf-8'
            print('GET：'+str(response.status_code), url)
            return response
        except Exception as e:
            # raise e
            print('\033[1;31;0mretrying：\033[0m', e)
            return False

    def request(self, url, headers=None, callback=None, meta=None):
        response = self.try_request(url=url, headers=headers)
        if response == False:
            number = 0
            for i in range(0, max_request):
                response = self.try_request(url=url, headers=headers)
                if response != False:
                    break
                elif i == 3:
                    return
                else:
                    number += 1
        if callback != None:
            if isinstance(meta, dict):
                return callback(response, meta)
            else:
                return callback(response)
        else:
            return response

    def try_formrequest(self, url, data, headers=None):
        try:
            if '127.0.0.1' in url:
                response = self.s.post(headers=headers, url=url, data=data, timeout=15)
            elif IS_PROXY == False:
                response = self.s.post(headers=headers, url=url, data=data, timeout=15)
            else:
                response = self.s.post(headers=headers, url=url, data=data, proxies=rand_choi_pool(), timeout=15)
            # response.encoding = 'utf-8'
            print('POST：'+str(response.status_code), url, data)
            return response
        except Exception as e:
            print('\033[1;31;0mretrying：\033[0m', e)
            return False

    def formrequest(self, url, data, callback=None, headers=None, meta=None):
        response = self.try_formrequest(url=url, headers=headers, data=data)
        while response == False:
            response = self.try_formrequest(url=url, headers=headers, data=data)
        if callback != None:
            if isinstance(meta, dict):
                return callback(response, meta)
            else:
                return callback(response)
        else:
            return response
    
    def split_str(self, str_data):
        data_lists = []
        split_fuhao = [',', ';', '、']
        for i in split_fuhao:
            data_demo = str_data.split(i)
            data_lists.append(data_demo)
        len_all = [len(i) for k, i in enumerate(data_lists)]
        last_lists = data_lists[len_all.index(max(len_all))]
        for k, l in enumerate(split_fuhao):
            for a in last_lists:
                if l in a:
                    data_demo = a.split(l)
                    last_lists.remove(a)
                    for i in data_demo:
                        last_lists.append(i)
            return last_lists
        return last_lists
    
    def data_deal(self, data):  # 一般数据处理
        if (data == None) or (data == ''):
            data_last = ''
            return data_last
        elif isinstance(data, dict):
            return json.loads(data)
        else:
            return str(data).replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\u3000', '').replace('\\u3000', '').replace('\t', '').replace(' ', '').replace('&nbsp;', '').replace('\\r', '').replace('\\n', '')

    def judge_deal(self, judge_lists):  # 审判员是否合法处理
        judge = []
        for i in judge_lists:
            if len(self.data_deal(i)) > 6:
                continue
            else:
                judge.append(self.data_deal(i))
        return ';'.join(judge)


    def analysis_excel(self, path, sheet_index):
        workbook = xlrd.open_workbook(path)
        data_sheet = workbook.sheets()[sheet_index]
        rowNum = data_sheet.nrows  # sheet行数
        all_data = []
        for r in range(rowNum):
            rows = data_sheet.row_values(r)
            all_data.append(rows)
        return all_data

    def custom_time(self, timestamp):  # 时间戳转化时间处理（秒级）
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def custom_time_mill(self, timestamp):  # 时间戳转化时间处理（毫秒级）
        # 转换成localtime
        time_local = time.localtime(timestamp/1000)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def production_md5(self, str_data):  # 生成md5
        md5 = hashlib.md5(str_data.encode(encoding='UTF-8')).hexdigest()
        return md5

    def get_caseType(self, data):  # 案件类型判断
        if '民事' in data:
            last_data = '民事案件'
            return last_data

        elif '刑事' in data:
            last_data = '刑事案件'
            return last_data

        elif '行政' in data:
            last_data = '行政案件'
            return last_data

        elif '赔偿' in data:
            last_data = '赔偿案件'
            return last_data

        elif '执行' in data:
            last_data = '执行案件'
            return last_data
        else:
            return ''

    def get_wslx(self, str):
        data_demo = re.compile('.*?(判.*?决.*?书).*?|.*?(裁.*?定.*?书).*?|.*?(调.*?解.*?书).*?|.*?(决.*?定.*?书).*?|.*?(通.*?知.*?书).*?', re.S)
        data = self.deal_re(data_demo.search(str))
        return data

    def get_caseno(self, str):
        caseno = self.deal_re(self.caseno.search(str))
        return caseno
    

    def now_time(self, is_date=False):  # 获取现在时间
        if is_date == False:
            now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return now_time
        now_time = str(time.strftime("%Y-%m-%d", time.localtime()))
        return now_time

    def get_host(self, url):  # 从url中提取域名
        host = self.deal_re(re.search('http://(.*?)/.*?', url, re.S))
        return host

    def deal_lists(self, lists):  # 判断列表里的元素是否为None，并去除None，返回；分割的字符串
        lists_1 = []
        for i in lists:
            if (i == None) or (i == ''):
                continue
            else:
                lists_1.append(i)
        return ';'.join(lists_1)

    def deal_re(self, demo):  # 判断正则是否匹配到的是否为空
        if demo != None:
            data_tuple = demo.groups()
            lists = list(data_tuple)
            data = ''.join([i for i in lists if i != None])
            return data
        else:
            return ''

    def get_time(self, str_data):  # 提取时间
        data = self.deal_re(re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", str_data))
        return data

    def _is_valuetime(self, str_time):
        tt = self.deal_re(re.search(r"(\d{4}-\d{1,2}-\d{1,2})", str_time, re.S))
        if tt != '':
            demo = tt.split('-')
            if (len(demo[1]) == 1) and (len(demo[2]) != 1):
                demo[1] = '0'+demo[1]
                return '-'.join(demo)
            if (len(demo[2]) == 1) and (len(demo[1]) != 1):
                demo[2] = '0'+demo[2]
                return '-'.join(demo)
            if (len(demo[2]) == 1) and (len(demo[1]) == 1):
                demo[1] = '0'+demo[1]
                demo[2] = '0'+demo[2]
                return '-'.join(demo)
            if int(demo[1]) > 12:
                return ''
            if int(demo[2]) > 31:
                return ''
            if (int(demo[1]) == 00) or (int(demo[2]) == 0):
                return ''
            else:
                return '-'.join(demo)
        else:
            return str_time

    def _deal_time(self, str_time):
        data = str_time
        flag = self.deal_lists(re.findall(r'(\D)', str_time, re.S))
        if flag != '':
            for i in flag:
                if (i == '-'):
                    continue
                elif (i == '/') or (i == '年') or (i == '月'):
                    data = data.replace(i, '-')
                else:
                    data = data.replace(i, '')
            return self._is_valuetime(data)
        else:
            return str_time

    def parseDate(self, str_data):
        try:
            if (type(str_data) == None) or (str_data == 'None') or (str_data == None):
                return self.data_deal(str_data)
            if ('二' in str_data) or ('一' in str_data) or ('十' in str_data):
                nm = {'十': '10', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8',
                      '九': '9', '零': '0', 'o': '0', 'O': '0', '○': '0', '〇': '0', 'Ｏ': '0', '0': '0', 'Ο': '0',
                      'О': '0', 'ο': '0', '੦': '0', '୦': '0', 'օ': '0', 'Օ': '0', '०': '0', '০': '0', '૦': '0',
                      '◦': '0', '⃝': '0', '◯': '0', '๐': '0', '໐': '0', '￮': '0', 'ᄋ': '0', '×': '0', '?': '?',
                      '廿': '2',
                      '元': '11'}
                if str_data.count("年", 0, len(str_data)) == 2:
                    str_data = str_data.split('年')
                    if len(str_data) == 3:
                        str_data = str_data[1] + '年' + str_data[2]
                    elif len(str_data) == 2:
                        str_data = str_data[1] + '年'
                    else:
                        return ''
                year = str_data.split('年')[0]
                month = str_data.split('年')[1].split('月')[0]
                day = str_data.split('年')[1].split('月')[1].split('日')[0]
                if (len(day) == 3):
                    day = day.replace('十', '')
                year = ''.join(nm[i] for i in year)
                month = ''.join(nm[i] for i in month)
                day = ''.join(nm[i] for i in day)
                if (len(month) == 3) and (int(month[1:]) != 10):
                    month = month.replace('0', '')
                if (len(month) == 3) and (int(month[1:]) == 10):
                    month = month.replace('1', '')
                if (len(day) == 3) and (int(day[1:]) != 10):
                    day = day.replace('0', '')
                if (len(day) == 3) and (int(day[1:]) == 10):
                    day = day.replace('1', '')
                data = self._deal_time(year + '-' + month + '-' + day)
                return data
            patternForTime = r'(\d{4}[\D]\d{1,2}[\D]\d{1,2}[\D]?)'
            data = self._deal_time(self.deal_re(re.search(patternForTime, str_data, re.S)))
            return data
        except:
            print(str_data)
            return ''

    def get_anyou(self, str_data):  # 从文本中提取案由
        anyou_lists = []
        for anyou in self.anyou_lists:
            if anyou in str_data:
                anyou_lists.append(anyou)
        if len(anyou_lists) != 0:
            array = []
            for a in anyou_lists:
                array.append(len(a))
            n = len(array)
            for i in range(n):
                for j in range(0, n-i-1):
                    if array[j] > array[j + 1]:
                        array[j], array[j + 1] = array[j + 1], array[j]
            ln = list(filter(lambda s: isinstance(s, str) and len(s) == array[-1], anyou_lists))
            if len(ln) > 1:
                for l in ln:
                    if l+'一案' in str_data:
                        return l
            elif len(ln) == 1:
                return ''.join(ln)

        elif len(anyou_lists) == 0:
            return ''

        else:
            return ''
        
    
    def check_name(self, name_lists):
        data_lists = []
        for i in name_lists:
            if ((i.endswith('企业') == True) or (i.endswith('检察院') == True) or (i.endswith('部门') == True) or (i.endswith('部') == True) or (
                    i.endswith('学院') == True) or (i.endswith('商户') == True) or (i.endswith('商行') == True) or (
                        i.endswith('店') == True) or (i.endswith('机构') == True) or (i.endswith('合作社') == True) or (
                        i.endswith('平台') == True) or (i.endswith('医院') == True) or (i.endswith('集团') == True) or (
                        i.endswith('单位') == True) or (i.endswith('政府') == True) or (i.endswith('公司') == True) or (
                        i.endswith('机关') == True) or (i.endswith('厂') == True) or (i.endswith('中心') == True) or (
                        i.endswith('学校') == True) or (i.endswith('院') == True) or (i.endswith('局') == True) or (
                        i.endswith('委员会') == True) or (i.endswith('社') == True)) and (len(i) <= 20):
                data_lists.append(i)
            if (len(i) <= 5) and ('的' not in i):
                data_lists.append(i)
        return list(set(data_lists))
        # return list(set(data_lists))


    def deal_re_lists(self, lists):  # 判断列表里的元素是否为None，并去除None，返回；分割的字符串
        lists_1 = []
        for i in lists:
            for t in list(i):
                if (t == None) or (t == ''):
                    continue
                else:
                    lists_1.append(t)
        return list(tuple(lists_1))
    

    def replace_html(self, html):  # 去除html标签
        s = Selector(text=html)
        pattern = self.data_deal(''.join(s.xpath('//text()').extract())).replace('。', '，').replace(',', '，').replace('、', '，').replace('\r', '').replace('\n', '').replace('\t', '')
        return pattern
    
    def replace_other(self, html):
        s = Selector(text=html)
        pattern = self.data_deal(''.join(s.xpath('//text()').extract()))
        return pattern

    def changeStrtoTime(self, str_text):
        re = ""
        for s in str_text:
            re = re + self.SBC2DBC(s)
        str_text = re
        re = ""
        # print(str_text)
        strtoalb = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
                    '7': '7', '8': '8', '9': '9', '10': '10', '11': '11', '12': '12', '13': '13', '14': '14',
                    '15': '15', '16': '16', '17': '17', '18': '18', '19': '19', '20': '20', '21': '21',
                    '22': '22', '23': '23', '24': '24', '25': '25', '26': '26', '27': '27', '28': '28', '29': '29',
                    '30': '30', '31': '31', '〇': '0', '零': '0', '○': '0', '1O': '10', '一': '1', '元': '1', '二': '2',
                    '两': '2', '三': '3',
                    '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10', '十一': '11', '十二': '12',
                    '十三': '13', '十四': '14',
                    '十五': '15', '十六': '16', '十七': '17', '十八': '18', '十九': '19', '二十': '20', '二十一': '21',
                    '二十二': '22', '二十三': '23', '二十四': '24', '二十五': '25', '二十六': '26', '二十七': '27',
                    '二十八': '28', '二十九': '29', '三十': '30', '三十一': '31'}
        for i in range(1, 10):
            temp_key = '0' + str(i)
            strtoalb[temp_key] = str(i)
        nian = str_text.split("年")  # nian[0]是年份，nian[1]是月份加号
        if len(nian) == 2:
            for s in nian[0]:
                if s in strtoalb:
                    re = re + strtoalb[s]
            re = re + "-"
            # print(re)
            yue = nian[1].split("月")
            if len(yue) == 2:
                if yue[0] in strtoalb:
                    re = re + strtoalb[yue[0]] + "-"
                # print(re)
                ri = yue[1].split("日")
                if ri[0] in strtoalb:
                    re = re + strtoalb[ri[0]]
                # print(re)
        try:
            self.datetime.datetime.strptime(re, '%Y-%m-%d')
        except:
            re = ""
        return re

    def SBC2DBC(self, char):
        chr_code = ord(char)
        # 处理全角中数字大等于10的情况
        if chr_code in range(9312, 9332):
            return str(chr_code - 9311)
        elif chr_code in range(9332, 9352):
            return str(chr_code - 9331)
        elif chr_code in range(9352, 9372):
            return str(chr_code - 9351)
        elif chr_code in range(8544, 8556):
            return str(chr_code - 8543)

        else:
            if chr_code == 12288:  # 全角空格，同0x3000
                chr_code = 32
            if chr_code == 8216 or chr_code == 8217:  # ‘’
                chr_code = 39  # '
            elif chr_code in range(65281, 65374):
                chr_code = chr_code - 65248
            return chr(chr_code)

    def getone(self, texts, rules):
        pattern = re.compile(rules, re.DOTALL)
        rete = pattern.search(texts)
        if rete is not None:
            return rete.group()
        else:
            return ""

    def getall(self, texts, rules):
        pattern = re.compile(rules, re.S)
        retes = pattern.finditer(texts)
        return retes

    # 在getall基础上改进，直接返回正则匹配后的list
    def get_all_text(self, texts, rules):
        list = []
        pattern = re.compile(rules)
        retes = pattern.finditer(texts)
        for rete in retes:
            list.append(rete.group())
        return list

    # 增加删除操作，让代码简洁
    def del_opt(self, org_txt, word_replace_list):
        for word in word_replace_list:
            org_txt = org_txt.replace(word, '')
        return org_txt

    def get_real_hj_text(self, texts, rules):
        rete = self.getone(texts, rules)
        if rete.count("罪") < 1 and rete.count("公司") < 1 and rete.count("年") < 1 and rete.count("月") < 1 \
                and rete.count("日") < 1 and rete.count("被") < 1 and rete.count("经") < 1:
            rete = rete.replace("生于", "")
        else:
            rete = ""
        return rete

    def get_dsr(self, zw):
        dsr = []
        dsr1 = self.del_opt(self.getone(zw, r"(原审第三人：|第三人：|原审第三人|第三人)\S{2,5}?[,，。]"),
                       ["委托诉讼代理人", "原审第三人", "，", "、", "。", "：", ":", "第三人", "委托", "男", "女"])
        dsr.append(dsr1)
        # print(dsr, '第三人')
        return ",".join(list(dsr))

    def get_glah(self, zw):
        list1 = []
        glah1 = self.getone(zw, r'(?<=以)\（\d{4}\）.{4,15}号|(?<=以)\S{0,8}\d{4}.{2,15}号')
        if "及" in glah1:
            glah1 = ''

        if glah1 == '' or None:
            glah = self.getall(zw, r'\（\d{4}\）.{4,15}号')
            lastlist = []
            for i in glah:
                anhao = i.group()
                lastlist.append(anhao)
            list1 = set(lastlist)  # 对重复数据进行去重处理
            print(list1, '关联案号')
        return list1

    def get_lawname(self, zw):
        # 辩护人
        bhur = self.getall(zw, r"(委托诉讼代理人|诉讼代理人|委托代理人|暨委托代理人|辩护人)\S{2,5}[,，。]")
        bhr = []
        for i in bhur:
            bhr1 = self.del_opt(i.group(),
                           ["委托诉讼代理人", "辩护人", "，", "、", "。", "：", ":", "暨委托代理人", "暨诉讼代理人", "诉讼代理人", "委托代理人", "法定代理人",
                            "指定辩护人", "男", "女", "辩称", "终本约谈", "的辩护意见"])
            bhr.append(bhr1)
        return ','.join(list(bhr))

    def get_pnametext(self, zw):  # 被执行人.+?(男|女).+?(?=[。])
        texts_bg = self.getall(zw,
                          r'被(执行人|申请人|申请执行人|告|告人)\S{2,12}(男|女).+?(?=(，|被执行人|被告|被申请人|。))|被(执行人|申请人|申请执行人|告|告人)\S{2,12}农民.+?(?=[。])|被(执行人|申请人|申请执行人|告|告人)\S{2,8}(男|女).+?住.+?(?=[。，])|被(执行人|申请人|申请执行人|告|告人)\S{2,16}(公司|局|事务所|检察院|法院|医院|政府|委员会|企业|部门|部|学院|商户|商行|店|机构|合作社|平台|医院|集团|单位|政府|机关|厂|中心|学校|院|局|委员会|组|支行|总行)\S{1,12}(住|地址).+?(?=[。,\s])|被告：.+?(?=\s)|被(执行人|申请人|申请执行人|告|告人)[:：].+?(公司|地址).+?(?=[。])|被(执行人|申请人|申请执行人|告|告人)\S{2,20}(公司|地址|个体).+?(?=[。])')  # 2018.10.16

        data_all = []
        for text in texts_bg:
            data_lists = []

            bgrxx = text.group()
            # print(bgrxx, '-----')
            filters = ['无名氏', '舞女', '妇女', '卖淫女', '男模', '女模特', '受伤', '诊断', '第三人']
            if all(t not in bgrxx for t in filters):
                # print(bgrxx, "=============")
                bgrxxs = bgrxx
                # jobs = "无职业|无固定职业"
                # for gz in dic_gz.keys():
                #     jobs = gz
                # 户籍地、出生地规则
                hj_rules = r'生于\w+?国\w+|' \
                           r'生于\w+?省\w+|' \
                           r'生于\w+?市\w+|' \
                           r'生于\w+?区\w+|' \
                           r'生于\w+?县\w+|' \
                           r'生于\w+?镇\w+|' \
                           r'生于\w+?乡\w+|' \
                           r'\w+?国\w{0,30}人|' \
                           r'\w+?省\w*?人|' \
                           r'\w+?市\w*?人|' \
                           r'\w+?区\w*?人|' \
                           r'\w+?县\w*?人|' \
                           r'\w+?镇\w*?人|' \
                           r'\w+?乡\w*?人|' \
                           r'生于\w+?县|' \
                           r'生于\w+?市'
                name = self.del_opt(self.getone(bgrxxs,
                                      r'被(执行人|上诉人|申请人|申请执行人|告|告人).+?(?=(男|女))|被(执行人|申请人|申请执行人|告|告人)\S{2,18}(公司|局|事务所|检察院|法院|医院|政府|委员会|企业|部门|部|学院|商户|商行|店|机构|合作社|平台|医院|集团|单位|政府|机关|厂|中心|学校|院|局|委员会|组|支行|总行)|被(执行人|申请人|申请执行人|告|告人)\S{2,6}(,|，|。|\s)'),
                               ["被执行人：", "被上诉人：", "反诉原告：", "被申请人：", "被告人：", "被告：", "被执行人：", "被申请执行人：", "被上诉人", "反诉原告",
                                "被申请人", "被告人", "被告", "被执行人", "被申请执行人", "）：", "：", ":", ",", "，"])
                # print(name)
                if name == "":
                    name = self.del_opt(self.getone(bgrxxs, r'被执行人[:：].+?(男|女)'), ["（", "）", "上诉人", "原审", "被告人"])
                data_lists.append(name)
                # 性别
                if bgrxxs.count("男"):
                    data_lists.append("男")
                if bgrxxs.count("女"):
                    data_lists.append("女")
                # 出生日期
                csrq = self.del_opt(self.getone(bgrxxs, r'\d{2,4}年\w{0,10}(出生|生)|生于\d{2,4}年\w{0,10}'),
                               ["生于", "出生", "生"])
                try:
                    birth_date = self.changeStrtoTime(csrq)
                except:
                    birth_date = ""
                data_lists.append(birth_date)

                # 民族
                def get_mz(texts, rules):
                    retes = self.getall(texts, rules)
                    ret = ""
                    for rete in retes:
                        r = rete.group()
                        if r.count("广西") < 1 and r.count("宁夏") < 1 and r.count("自治") < 1 and r.count("区") < 1 \
                                and r.count("市") < 1 and r.count("县") < 1 and r.count("镇") < 1 and r.count("乡") < 1 \
                                and r.count("州") < 1 and r.count("村") < 1:
                            ret = r
                            break
                    return ret

                data_lists.append(get_mz(bgrxxs, r'\w+?族'))
                # 教育程度
                data_lists.append(self.getone(bgrxxs, r'\w+文化|文化程度\w+|研究生|博士|硕士|大学本科|大学|本科|大本|大学专科'
                                                 r'|大专|专科|中专|中技|高中|初中|小学|文盲|半文盲|职高|无文化')
                                  .replace('无文化', '文盲').replace("大本", "本科").replace("大学", "本科")
                                  .replace("大学本科", "本科").replace("大学专科", "大专").replace("专科", "大专"))
                jiaoyu = self.getone(bgrxxs, r'\w+文化|文化程度\w+|研究生|博士|硕士|大学本科|大学|本科|大本|大学专科'
                                        r'|大专|专科|中专|中技|高中|初中|小学|文盲|半文盲|职高|无文化')
                data_lists.append(self.getone(bgrxxs,
                                         r'农民|务工|机动车驾驶员|无职业|军人|现役军人|会计|和尚|牙医|建筑师|医生|司机|出租车司机|老师|教授|护士|主持人|司仪|演员|助理|警察|厨师|营养师|工人|面点师|电工|演员|出纳|厨师|服务员|秘书|无业').replace(
                    "无职业", "无业").replace("无固定职业", "无业"))
                locofbirth = self.get_real_hj_text(bgrxxs, hj_rules)
                if locofbirth != "":
                    data_lists.append(locofbirth)
                else:
                    hj = self.del_opt(self.getone(bgrxxs, r'户籍(|地|所在地)|住所地.+'), ["户籍地", "户籍", "所在地", "：", "，", ":", "住所地"])
                    data_lists.append(hj)
                # 居住地,为啥每次都是居住地
                jzd = self.del_opt(self.getone(bgrxxs, r'住址：\w+|住址\w+|住\w+'), ['住址：', '住址', "住在", "住", "所地"])
                data_lists.append(jzd)
            data_all.append(data_lists)
        return data_all

    def get_plaintifftext(self, zw):  # 被执行人.+?(男|女).+?(?=[。])
        texts_bg = self.getall(zw, r'(申请执行人|申请人|上诉人|原\s{0,3}告|赔偿请求人)\S{2,12}(男|女).+?(?=(，|申请执行人|上诉人|原告|申请人|。))|(执\s{0,3}行\s{0,3}人|申\s{0,3}请\s{0,3}人|申请执行人|上诉人|原\s{0,3}告)\S{2,12}(男|女).+?住.+?(?=[。，])|(执\s{0,3}行\s{0,3}人|申\s{0,3}请\s{0,3}人|申请执行人|上诉人|原\s{0,3}告)\S{2,22}(公司|局|事务所|检察院|法院|医院|政府|委员会|企业|部门|部|学院|商户|商行|店|机构|合作社|平台|医院|集团|单位|政府|机关|厂|中心|学校|院|局|委员会|组|支行|总行)\S{1,12}(住|地址|信用代码).+?(?=[。,\s])|(执行申请人|申请人|上诉人|申请执行人|原告)[:：].+?(公司|地址).+?(?=[。])|(执行申请人|申请人|上诉人|申请执行人|原\s{0,3}告).+?公司.+?(住|地址).+?(?=[。,\s])|原告：.+?(?=\s)|原告.+?(?=\s)')  # 2018.10.16

        xm_yg, xb_yg, csrq_bg, mz_bg, jycd_bg, gz_bg, hj_bg, jzd_bg = [], [], [], [], [], [], [], []
        data_all = []
        for text in texts_bg:
            data_lists = []
            ygrxx = text.group()

            filters = ['无名氏', '舞女', '妇女', '卖淫女', '男模', '女模特', '受伤', '诊断', '被']

            if all(t not in ygrxx for t in filters):
                # print(ygrxx, "=============")

                ygrxxs = ygrxx
                hj_rules = r'生于\w+?国\w+|' \
                           r'生于\w+?省\w+|' \
                           r'生于\w+?市\w+|' \
                           r'生于\w+?区\w+|' \
                           r'生于\w+?县\w+|' \
                           r'生于\w+?镇\w+|' \
                           r'生于\w+?乡\w+|' \
                           r'\w+?国\w{0,30}人|' \
                           r'\w+?省\w*?人|' \
                           r'\w+?市\w*?人|' \
                           r'\w+?区\w*?人|' \
                           r'\w+?县\w*?人|' \
                           r'\w+?镇\w*?人|' \
                           r'\w+?乡\w*?人|' \
                           r'生于\w+?县|' \
                           r'生于\w+?市'

                # 姓名
                name = self.del_opt(self.getone(ygrxxs, r'(执行人|申请执行人|申请人|上诉人|原告|赔偿申请人|赔偿请求人).+?(?=(男|女))'
                                              r'|(执行人|申请执行人|告|告人).+?(公司|局|事务所|检察院|法院|医院|政府|委员会|企业|部门|部|学院|商户|商行|店|机构|合作社|平台|医院|集团|单位|政府|机关|厂|中心|学校|院|局|委员会|组|支行|总行)'
                                              r'|原告：\S{2,15}(,|，|。|\s)|原告\S{2,15}(,|，|。|\s)'),
                               ["申请执行人", "执行人：", "赔偿请求人", "上诉人：", "原审", "", "原告：", "执行人：", "申请执行人：", "上诉人", "申请人", "原告",
                                "执行人", "）：", "：", "）:", ",", "，", ":", ")", "）"])
                data_lists.append(name)
                # 性别
                if ygrxxs.count("男"):
                    data_lists.append("男")
                elif ygrxxs.count("女"):
                    data_lists.append("女")
                else:
                    data_lists.append("未知")

                # 出生日期
                csrq = self.del_opt(self.getone(ygrxxs, r'\d{2,4}年\w{0,10}(出生|生)|生于\d{2,4}年\w{0,10}'),
                               ["生于", "出生", "生"])
                try:
                    birth_date = self.changeStrtoTime(csrq)
                except:
                    birth_date = ""

                data_lists.append(birth_date)

                # 民族
                def get_mz(texts, rules):
                    retes = self.getall(texts, rules)
                    ret = ""
                    for rete in retes:
                        r = rete.group()
                        if r.count("广西") < 1 and r.count("宁夏") < 1 and r.count("自治") < 1 and r.count("区") < 1 \
                                and r.count("市") < 1 and r.count("县") < 1 and r.count("镇") < 1 and r.count("乡") < 1 \
                                and r.count("州") < 1 and r.count("村") < 1:
                            ret = r
                            break
                    return ret

                data_lists.append(get_mz(ygrxxs, r'\w+?族'))
                # 教育程度
                data_lists.append(self.getone(ygrxxs, r'\w+文化|文化程度\w+|研究生|博士|硕士|大学本科|大学|本科|大本|大学专科'
                                                 r'|大专|专科|中专|中技|高中|初中|小学|文盲|半文盲|职高|无文化')
                                  .replace('无文化', '文盲').replace("大本", "本科").replace("大学", "本科")
                                  .replace("大学本科", "本科").replace("大学专科", "大专").replace("专科", "大专"))

                data_lists.append(self.getone(ygrxxs,
                                         r'农民|务工|机动车驾驶员|无职业|军人|现役军人|会计|和尚|牙医|建筑师|医生|司机|出租车司机|老师|教授|护士|主持人|司仪|演员|助理|警察|厨师|营养师|工人|面点师|电工|演员|出纳|厨师|服务员|秘书|无业').replace(
                    "无职业", "无业").replace("无固定职业", "无业"))
                # print(gz_bg)
                # 户籍地
                locofbirth = self.get_real_hj_text(ygrxxs, hj_rules)
                if locofbirth != "":
                    data_lists.append(locofbirth)
                else:
                    hj = self.del_opt(self.getone(ygrxxs, r'户籍(|地|所在地)|住所地.+'), ["户籍地", "户籍", "所在地", "：", "，", ":", "住所地"])
                    data_lists.append(hj)
                # 居住地,为啥每次都是居住地
                jzd = self.del_opt(self.getone(ygrxxs, r'住址：\w+|住址\w+|住.+?(?=[，])|住\w+'), ['住址：', '住址', "住在", "住", "所地", "所住地"])
                data_lists.append(jzd)
            data_all.append(data_lists)
        return data_all

    def get_sorttime(self, str_data):  # 获取sorttime
        sorttime_ling = ['○', '〇', 'Ｏ', 'O', '0', 'Ο', 'О', 'ο', '੦', '୦', 'օ', 'Օ', '०', '০', '૦', '◦', '⃝', '◯', '๐', '໐', '￮', 'ᄋ', '੦']
        sorttime = None
        for i in sorttime_ling:
            sorttime_demo = re.compile('二'+i+'(.*?)日', re.S)
            sorttime = self.deal_re(sorttime_demo.search(self.replace_html(str_data[-100:])))
            # print(sorttime)
            if sorttime != '':
                # print('二'+sorttime+'日')
                sorttime = '二'+i+sorttime+'日'
                return sorttime
            else:
                sorttime = sorttime
        return self.data_deal(sorttime)
    
    def getYesterday(self, num=0):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        yesterday = today - twoday
        return str(yesterday)

    def get_lawyer(self, str):
        content = self.replace_html(str)
        lawyer = None
        lawyer_lists = []
        for i in self.lawyer_lists:
            if i in content:
                lawyer_lists.append(i)
            else:
                lawyer = lawyer
        return ';'.join(lawyer_lists)

    def try_request_only(self, url, proxies=None, headers=None):
        try:
            # response = s.get(url=url, headers=headers, timeout=30)
            response = s.get(url=url, headers=headers, proxies=proxies, timeout=30)
            print('\033[1;31;0mGET：\033[0m'+str(response.status_code), url)
            return response
        except Exception as e:
            # raise e
            print('\033[1;31;0mretrying：\033[0m', e)
            return False

    def request_only(self, url, proxies=None, headers=None, callback=None, meta=None):
        response = self.try_request_only(url=url, headers=headers, proxies=proxies)
        while response == False:
            response = self.try_request_only(url, headers)
        if callback != None:
            if isinstance(meta, dict):
                return callback(response, meta)
            else:
                return callback(response)
        else:
            return response

    def try_formrequest_only(self, url, data, proxies=None, headers=None):
        try:
            if '127.0.0.1' in url:
                response = s.post(url=url, data=data)
            else:
                response = s.post(headers=headers, url=url, data=data, proxies=proxies, timeout=15)
            print('\033[1;31;0mPOST：\033[0m'+str(response.status_code), url, data)
            return response
        except Exception as e:
            print('\033[1;31;0mretrying：\033[0m', e)
            return False

    def formrequest_only(self, url, data, proxies=None, callback=None, headers=None, meta=None):
        response = self.try_formrequest_only(url=url, headers=headers, data=data, proxies=proxies)
        while response == False:
            response = self.try_formrequest_only(url=url, headers=headers, data=data, proxies=proxies)
        if callback != None:
            if isinstance(meta, dict):
                return callback(response, meta)
            else:
                return callback(response)
        else:
            return response
