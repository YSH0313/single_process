# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2023-02-24- 18:28:40
# @Version: 1.0.0
# @Description: TODO

import io
import re
import csv
import xlrd
import json
import time
import html
import base64
import execjs
import hashlib
import datetime
import subprocess
import dateparser
import pdfplumber
import numpy as np
import urllib.parse
from math import ceil
import dateutil.parser
import dateutil.parser
import pdfminer.psparser
from urllib import parse
import demjson3 as demjson
from string import Template
from datetime import datetime
from jsonpath import jsonpath
from dateutil.parser import parse
from scrapy.selector import Selector
from dateutil.parser import parse as pp
from xml.sax.saxutils import unescape, escape
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import *
from filestream_y.FileStream_y import stream_type
from library_tool.ocrutils import RecoFactory


class SingleTool(object):

    def deal_re(self, demo, defult=None):
        """判断正则是否匹配到的是否为空"""
        if demo != None:
            data_tuple = demo.groups()
            lists = list(data_tuple)
            data = ''.join([i for i in lists if i != None])
            return data
        else:
            if defult:
                return defult
            return ''

    def add_url_sha1(self, url, sgin=''):
        url_sha1 = self.url2sha1(url)
        t_num = str(int(url_sha1[-2:], 16) % 16)
        return url, t_num

    def url2sha1(self, url):
        import hashlib
        url_sha1 = hashlib.sha1(url.encode()).hexdigest()
        return url_sha1

    def dic2params(self, params, data, json_params):
        par = data if data else params if params else json_params
        if isinstance(par, dict):
            q = urllib.parse.urlencode(par)
            par = urllib.parse.unquote(q)
        return par

    def get_inttime(self, is_int=True):  # 获取现在时间
        import datetime
        if not is_int:
            dt_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return dt_ms
        dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        return dt_ms

    def is_json(self, myjson):
        if isinstance(myjson, dict):
            return True
        if '{' not in str(myjson):
            return False
        try:
            json.loads(myjson)
        except (ValueError, TypeError) as e:
            return False
        return True

    def isSubClassOf(self, obj, cls):
        try:
            for i in obj.__bases__:
                if i is cls or isinstance(i, cls):
                    return True
            for i in obj.__bases__:
                if self.isSubClassOf(i, cls):
                    return True
        except AttributeError:
            return self.isSubClassOf(obj.__class__, cls)
        return False

    def data_deal(self, data, no_replace=None):  # 一般数据处理
        if (data == None) or (data == ''):
            data_last = ''
            return data_last
        elif isinstance(data, dict):
            return json.loads(data)
        else:
            sin_list = ['\r', '\n', '\xa0', '\u3000', '\\u3000', '\t', ' ', '&nbsp;', '\\r', '\\n', ',,', '\\', '\\\\',
                        '\ufeff', '\u2002']
            for i in sin_list:
                if i == no_replace:
                    continue
                data = str(data).replace(i, '')
            start_with = ['、']
            for s in start_with:
                if s == no_replace:
                    continue
                elif data.startswith(s):
                    data = str(data).replace(s, '')
            return data

    def is_valid_date(self, strdate):
        '''判断是否是一个有效的日期字符串'''
        try:
            if ":" in strdate:
                time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(strdate, "%Y-%m-%d")
            return True
        except:
            return False

    def date_format(self, str_date):
        if isinstance(str_date, int):
            str_date = str(str_date)
        try:
            new_date = dateparser.parse(str_date).strftime('%Y-%m-%d %H:%M:%S')
            return new_date
        except AttributeError:
            try:
                new_date = parse(str_date)
                return str(new_date)
            except dateutil.parser.ParserError:
                return None
        except:
            return None

    def is_today(self, t1, t2, tz_count=28800):
        """
        tz_count表示当前时区与UTC0时区的时间差（秒）
        判断两个时间戳是否是同一天
        """
        if int((int(t1) + int(tz_count)) / 86400) == int((int(t2) + int(tz_count)) / 86400):
            return True
        else:
            return False

    def time_step(self, start_time, end_time, step=3600):  # step是间隔时间，单位是秒
        # 这里是上面的字符串时间格式(可以改)
        fmt = '%Y-%m-%d %H:%M:%S'

        t1 = datetime.strptime(self.date_format(start_time), fmt)
        t2 = datetime.strptime(self.date_format(end_time), fmt)

        un_time_1 = time.mktime(t1.timetuple())
        un_time_2 = time.mktime(t2.timetuple())

        if self.is_today(un_time_1, un_time_2):
            time_difference = (t2 - t1).total_seconds()
            if int(time_difference) > step:
                return False
            return time_difference
        else:
            return True

    def date_refix(self, str_date):
        flag = isinstance(str_date, list)
        if flag:
            time_list = [self.date_format(i) for i in str_date if self.date_format(i)]
            return time_list
        if str_date == '空':
            return str_date
        elif str_date and not flag:
            return self.date_format(str_date)
        else:
            return None

    def save_csv(self, path, filename, header_list, data_list, encoding):
        self.store_file = path + '{filename}.csv'.format(filename=filename)
        # 打开(创建)文件
        file = open(self.store_file, 'a+', encoding=encoding, newline='')
        # csv写法
        writer = csv.writer(file, dialect="excel")
        writer.writerow(header_list)
        writer.writerow(data_list)

    def analysis_excel(self, path, sheet_index, startrow):
        workbook = xlrd.open_workbook(path)
        data_sheet = workbook.sheets()[sheet_index]
        rowNum = data_sheet.nrows  # sheet行数
        all_data = []
        for r in range(startrow, rowNum):
            rows = data_sheet.row_values(r)
            all_data.append(rows)
        return all_data

    def custom_time(self, timestamp):  # 时间戳转化时间处理（秒级）
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def custom_time_mill(self, timestamp, separator='-'):  # 时间戳转化时间处理（毫秒级）
        # 转换成localtime
        time_local = time.localtime(timestamp / 1000)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime(f"%Y{separator}%m{separator}%d %H:%M:%S", time_local)
        return dt

    def time2stamp(self, time_str, mode="%Y-%m-%d %H:%M:%S", level=1000):
        timeArray = time.strptime(str(time_str), mode)
        timestamp = int(time.mktime(timeArray)) * level
        return timestamp

    def get_timestamp(self, level=1000):
        ts = int(round(time.time() * level))
        if level == 0:
            ts = int(round(time.time()))
        return ts

    def production_md5(self, str_data):  # 生成md5
        md5 = hashlib.md5(str_data.encode(encoding='UTF-8')).hexdigest()
        return md5

    def now_time(self, is_date=False):  # 获取现在时间
        if is_date == False:
            now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return now_time
        now_time = str(time.strftime("%Y-%m-%d", time.localtime()))
        return now_time

    def get_freetime(self, num=1, is_date=False):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        beforday = today + twoday
        if is_date:
            new_date = dateparser.parse(str(beforday)).strftime('%Y-%m-%d')
            return new_date
        new_date = dateparser.parse(str(beforday)).strftime('%Y-%m-%d %H:%M:%S')
        return str(new_date)

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

    def deal_path(self, initial_path):
        end_path = (initial_path.replace('\\', '.').replace('//', '.').replace('/', '.') + '.').replace('..', '.')
        return end_path

    def save_files(self, path, content, add=False, save_type='wb'):
        if add:
            save_type = 'a'
        with open(path, save_type) as file:
            file.write(content)

    def check_files(self, path, all=False):
        if all == True:
            with open(path, 'r') as f:
                all_files = f.read()
                return all_files
        else:
            with open(path, 'r') as f:
                files_lists = f.readlines()
                return files_lists

    def get_time(self, str_data):  # 提取时间
        if str_data:
            data = self.deal_re(re.search(
                r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})|(\d{4}年\d{1,2}月\d{1,2}日)|(\d{4}-\d{1,2}-\d{1,2})|(\d{4}\.\d{1,2}\.\d{1,2})",
                str_data))
        else:
            data = ''
        return data

    def get_all_time(self, str_data):  # 提取时间
        data_list = []
        if str_data:
            time_list = re.findall(
                r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})|(\d{4}年\d{1,2}月\d{1,2}日)|(\d{4}-\d{1,2}-\d{1,2})|(\d{4}\.\d{1,2}\.\d{1,2})",
                str_data, re.S)
            for i in time_list:
                for t in i:
                    if t:
                        data_list.append(t)
        return data_list

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
        pattern = self.data_deal(''.join(s.xpath('//text()').extract())).replace('。', '，').replace(',', '，').replace(
            '、', '，').replace('\r', '').replace('\n', '').replace('\t', '')
        return pattern

    def replace_other(self, html):
        s = Selector(text=html)
        pattern = self.data_deal(''.join(s.xpath('//text()').extract()))
        return pattern

    def getYesterday(self, num=0):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        yesterday = today - twoday
        return str(yesterday)

    def getFutureday(self, num=0):
        today = datetime.date.today()
        twoday = datetime.timedelta(days=num)
        futureday = today + twoday
        return str(futureday)

    def url_code(self, chara, encoding='utf-8'):
        data = str(parse.quote(chara, encoding=encoding))
        return data

    def url_decode(self, chara, encoding='utf-8'):
        data = str(parse.unquote(chara, encoding=encoding))
        return data

    def html_code(self, text, is_escape=False):
        data = text
        if is_escape:
            text = escape(text)
            if text == data:
                text = escape(text)
            else:
                return data
            return text
        else:
            text = unescape(text)
            if text == data.replace('amp;', '').replace('&gt;', '>'):
                text = html.unescape(text)
            else:
                return data
        return text

    def make_list(self, string):
        # 以，,空格，:,;同时进行切割
        data_list = [i for i in re.split(r'[,\t:;\、\,\，\;\；\:\；\： ]', string) if self.data_deal(i)]
        return data_list

    def is_contain_chinese(self, check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def dict2html(self, dict_data: dict):
        """
        字典数据to html表单
        html: str
        """
        html_ = ''
        base_tr = """<p>{}:{}</p>"""
        for key, value in dict_data.items():
            if value:
                html_ += base_tr.format(key, value)
        return html_

    def dict2html2(self, dict_data: dict):
        """
        字典数据to html表单
        html: str
        """
        keyd_map = {
            'project_type': '项目类型',
            'project_code': '项目编号',
            'project_name': '项目名称',
            'project_status': '项目状态',
            'project_detail': '项目描述',
            'pub_time': '时间',
            'province': '省',
            'city': '市',
            'county': '县',
            'caller': '业主单位',
            'contact': '联系人',
            'phone': '联系人电话',
            'approval_info': '审批信息',
            'agency': '审批部门',
            'time': '审批时间',
            'result': '审批结果',
            'detail': '审批事项',
            'code': '批复文号',
            'trade': '行业',
            'money': '项目总投资',
            'file_url': '文件链接'
        }
        new_dic = {}
        for k, v in dict_data.items():
            if k in keyd_map.keys():
                new_key = keyd_map[k]
                if new_key == '审批信息':
                    approval_info_list = []
                    for approval_info in v:
                        approval_info_data = {}
                        for key, value in approval_info.items():
                            approval_key = keyd_map[key]
                            approval_info_data[approval_key] = value
                        approval_info_list.append(approval_info_data)
                    new_dic[new_key] = approval_info_list
                else:
                    new_dic[new_key] = v
        td_data = ''
        approval_html = ''
        pdf_html = ''
        for new_key, new_value in new_dic.items():
            if new_key == '审批信息':
                app_tr_data = ''
                for i in new_value:
                    app_td_data = [
                        f"""<td>{i.get('审批部门', '')}</td>\r\n""",
                        f"""<td>{i.get('审批结果', '')}</td>\r\n""",
                        f"""<td>{i.get('批复文号', '')}</td>\r\n""",
                        f"""<td>{i.get('审批时间', '')}</td>\r\n""",
                        f"""<td>{i.get('审批事项', '')}</td>\r\n""",
                    ]
                    app_tr_data += f'<tr>\r\n{"".join(app_td_data)}</tr>\r\n'
                approval_html = f"""
                <table class="detailContent" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="detailFill detailBFont" colspan="5">审批信息</td>
                    </tr>
                    <tr>
                        <td class="detailFill">审批部门</td>
                        <td class="detailFill">审批结果</td>
                        <td class="detailFill">批复文号</td>
                        <td class="detailFill">审批时间</td>
                        <td class="detailFill">审批事项</td>
                    </tr>
                    {app_tr_data}
                </table>
                """
            elif new_key == '文件链接':
                if new_value.endswith('.pdf'):
                    pdf_html += f"""
                        <table class="detailContent" cellpadding="0" cellspacing="0"></table>
                        <iframe src="{new_value}" width="100%" height="1280"></iframe>
                    """
            else:
                # print(new_key, new_value)
                td_data += f"""<td class="detailFill">{new_key}</td><td>{new_value}</td>\r\n"""

        td_list = np.array([i for i in td_data.split('\r\n') if i])
        length = len(td_list)
        nu = ceil(length / 2)
        td_list.resize((nu, 2))
        tr_data = ''.join([f'<tr>{"".join(i)}</tr>' for i in td_list])
        table_html = f"""
        <table class="detailContent" cellpadding="0" cellspacing="0">
            <tr>
                <td class="detailFill detailBFont" colspan="5">项目基本信息</td>
            </tr>
            {tr_data}
        </table>
        {approval_html}
        {pdf_html}
        """
        import os, sys
        sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('js')[0])
        model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('config')[0],
                                  'config/nijian_model.html')
        with open(model_path, 'rb') as f:
            html = f.read().decode('utf-8')
            html = html.replace('<table></table>', table_html)
            return html

    def file_html_all(self, url, title):
        if url.endswith('.pdf') or title.endswith('.pdf'):
            html = f'<iframe src="{url}" width="100%" height="1280"></iframe>'
            return html
        elif url.endswith('.doc') or url.endswith('.docx') or url.endswith('.xlr') or url.endswith(
                '.xls') or url.endswith('.xlsx') or url.endswith('.txt') or url.endswith('.rar') or url.endswith(
            '.zip') or title.endswith('.doc') or title.endswith('.docx') or title.endswith(
            '.xlr') or title.endswith('.xls') or title.endswith('.xlsx') or title.endswith(
            '.txt') or title.endswith('.rar') or title.endswith('.zip'):
            html = f'<a href="{url}">附件：{title}</a>'
            return html

        elif url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg') or title.endswith(
                '.jpg') or title.endswith('.png') or title.endswith('.jpeg'):
            html = f'<img src="{url}" alt="{title}" />'
            return html
        else:
            html = f'<a href="{url}">附件：{title}</a>'
            return html

    def dic2table(self, dic_data):
        row_data = ''
        for k, v in dic_data.items():
            if v:
                row_data += f"<tr><td>{k}：{v}</td></tr>"
        table = f'<table>{row_data}</table>'
        return table

    def per_json(self, source_dict, json_path, get_num=1):
        result = jsonpath(source_dict, f'$..{json_path}')  # 如果取不到将返回False # 返回列表，如果取不到将返回False
        if isinstance(result, list) and (len(result) == 1 or get_num == 1):
            return result[0]
        elif isinstance(result, list) and (len(result) > 1 or get_num > 1):
            return '、'.join([str(i) for i in result if i])
        else:
            return result

    def per_dic_plus(self, dic_data, key_list):
        data = ''
        kong_list = ['null', 'Null', 'None', 'NULL']
        for key in key_list:
            da = dic_data.get(key)
            if da and da not in kong_list:
                data = da
                break
        return data

    def per_list(self, list_data, index):
        try:
            return list_data[index]
        except IndexError:
            return None

    def swapPositions(self, list, pos1, pos2):  # 指定列表的元素交换位置
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    def pdf2text(self, pdf_bytes):
        try:
            pdfFile = io.BytesIO(pdf_bytes)
            pdf = pdfplumber.open(pdfFile)
            data_list = []
            for page in pdf.pages:  # 遍历pdf每页进行相应的处理
                page_text = page.extract_text()
                if page_text:
                    data_list += page_text.split('\n')
            pdf.close()
            return data_list
        except (pdfminer.psparser.PSEOF, TypeError, pdfminer.pdfparser.PDFSyntaxError):
            return ''

    def execute_js(self, js_path, function_name, **kwargs):
        """
        :param js_path: js文件路径
        :param function_name: 要执行的js方法名
        :param kwargs: 执行js时需要传的参数
        :return: js返回的结果
        """
        js = ""
        fp1 = open(js_path, encoding='utf-8')
        js += fp1.read()
        fp1.close()
        ctx2 = execjs.compile(js)
        params = list(kwargs.values()) if len(list(kwargs.values())) > 1 and len(list(kwargs.values())) != 0 else \
            list(kwargs.values())[0]
        data = (ctx2.call(function_name, params))
        return data

    def hash(self, value, _mode):
        _hash = eval(f"hashlib.{_mode}(value.encode('utf-8')).hexdigest()")
        return _hash

    def get_clearance(self, item, cookie_name):
        ct = item.get('ct', None)
        bts = item.get('bts', None)
        chars = item.get('chars', None)
        hash_mode = item.get('ha', None)
        chars_length = len(item.get('chars', None))
        for i in range(chars_length):
            for j in range(chars_length):
                value = bts[0] + chars[i] + chars[j] + bts[1]
                if self.hash(value, hash_mode) == ct:
                    return f'{cookie_name}=' + value

    def jsl_second_cookie(self, cookie1, response):
        s = Selector(response=response)
        js = s.xpath('//text()').extract_first('').replace('document.cookie=', '').replace(
            'location.href=location.pathname+location.search', '')
        js_text = """
        function a(e) {
            return $text
        }"""
        d = Template(js_text).substitute(text=js)
        ctx2 = execjs.compile(d)
        cookie2 = (ctx2.call('a', 1))
        cookie = str(cookie2).split(';')[0]
        if cookie != 'None':
            cookie3 = f'{cookie1}; {cookie}'
            return cookie3

    def jsl_last_cookie(self, response, cookie_name='__jsl_clearance'):
        s = Selector(response=response)
        js_text = s.xpath('//text()').extract_first('')
        param = self.deal_re(re.search(';go\((.*?)\)', js_text, re.S))
        if param:
            cookie4 = self.get_clearance(json.loads(param), cookie_name)
            return cookie4

    def js_results(self, js_path, *args):
        params = ''
        for i in args:
            if len(args) > 1:
                params += str(i) + ' '
            else:
                params += str(i)
        params = params.rstrip(', ').rstrip(' None')
        command = f'/usr/local/bin/node {js_path} "{params}"'
        results = subprocess.getoutput(command)
        return results

    def base64_encode(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        if isinstance(data, int):
            data = str(data)
        data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        return data

    def base64_decode(self, data):
        data = base64.b64decode(data).decode('utf-8')
        return data

    def rs_server(self, html, cookies, link, js_path=r'js/rs_server/encrypt.js'):
        import sys, os
        sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('js')[0])
        js_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('library_tool')[0], js_path)
        html = base64.b64encode(html).decode('utf-8')
        command = f'/usr/local/bin/node {js_path} {html} "{cookies}" {link}'
        # print(command)
        try:
            results = subprocess.getoutput(command)
            return results
        except:
            return ''

    def fill_method(self, aes_str):
        '''pkcs7补全'''
        pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')
        return pad_pkcs7

    # 将明文用AES ECB模式加密
    def aesEncrypt(self, data, key):
        # 加密函数,使用pkcs7补全
        aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        res = aes.encrypt(self.fill_method(data))
        # 转换为base64
        msg = str(base64.b64encode(res), encoding="utf-8")
        return msg

    # 解密后，去掉补足的空格用strip() 去掉
    def aes_decrypt(self, text, key, iv):
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        # key = "BE45D593014E4A4EB4449737660876CE".encode('utf-8')
        # iv = b"A8909931867B0425"
        mode = AES.MODE_CBC
        cryptos = AES.new(key, mode, iv)
        plain_text = cryptos.decrypt(a2b_base64(text))
        data = bytes.decode(plain_text)
        fuhao = self.deal_re(re.search('(\\\\\S{3})', repr(data)[-5:], re.S))
        data = demjson.decode(repr(data).replace(fuhao, ''))
        return data

    def ocr_result(self, file_bytes):
        if len(file_bytes) > 10:
            stream = stream_type(file_bytes)
            result = []
            if stream == 'pdf' or stream == 'jpg' or stream == 'png' or stream == 'doc'or stream == 'docx':
                result = RecoFactory.reco_url(file_bytes, stream)
            return result
        else:
            return []

    def check_fileurl(self, url):
        suffix_list = ['.doc', '.docx', '.xlr', '.xls', '.xlsx', '.pdf', '.txt', '.jpg', '.png', '.rar', '.zip']
        for i in suffix_list:
            if url.endswith(i):
                return i
            elif not url.endswith(i) and i != suffix_list[-1]:
                continue
            else:
                return False