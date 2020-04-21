# -*- coding: utf-8 -*-
from config.all_config import *


class beizhixing_api(Manager):
    name = 'beizhixing_api'

    def __init__(self):
        Manager.__init__(self, 'ysh_beizhixing_api')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.header_img = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'Host': 'zxgk.court.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.content_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=59305252A1EC32D7A0F8577B4CBF7E44; _gscu_15322769=74417404itc5pr18; SESSION=0e6e9293-df73-4760-afbe-eff6efcdb4b2; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1583719282; _gscbrs_15322769=1; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1583719286; _gscs_15322769=83719285w4ljt281|pv:2',
            'Host': 'zxgk.court.gov.cn',
            'Origin': 'http://zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/zhixing/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.check_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '_gscu_15322769=74417404itc5pr18',
            'Host': 'zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/zhixing/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.uuid_lists = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                           'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                           'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                           'x', 'y', 'z']

    def start_requests(self):
        all_data = self.select_data(['fss_caseno', 'fss_name'], 'adjudicative', 'execute_yumin3', cond='WHERE (fss_caseno != "") and (fss_caseno is not NULL) and (fss_name != "") and (fss_name is not NULL) limit 100')
        for i in all_data:
            # print(self.data_deal(i[0]))
            self.send_mqdata(i[0]+'~'+i[1]+'~0~'+str(1))

    def parse_only(self, body):
        captchaId = ''.join(random.sample(self.uuid_lists, 32))
        img_url = 'http://zxgk.court.gov.cn/zhixing/captcha.do?captchaId={captchaId}&random=0.7438759475304964'.format(captchaId=captchaId)
        if 'content' in body:
            data_demo = body.split('~')
            pid = data_demo[0]
            flag = data_demo[1]
            caseno = data_demo[2]
            img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta={'pid': pid, 'captchaId': captchaId, 'flag': flag, 'caseno': caseno}, level=7)
            self.send_mqdata(img_request)
        else:
            data_demo = body.split('~')
            caseno = data_demo[0]
            pname = data_demo[1]
            cishu = data_demo[2]
            pages = data_demo[3]
            img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta={'pname': pname, 'caseno': caseno, 'captchaId': captchaId, 'cishu': cishu, 'pages':pages}, level=1)
            self.send_mqdata(img_request)

    def img_response(self, response):
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url = 'http://127.0.0.1:8011/zqsx'
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, callback='check_img', meta=response.meta, level=6)
        self.send_mqdata(decode_requests)

    def check_img(self, response):
        num = response.text.replace('_', '')
        if len(num) == 4:
            meta = response.meta
            meta['num'] = num
            url = 'http://zxgk.court.gov.cn/zhixing/checkyzm?captchaId={captchaId}&pCode={pCode}'.format(captchaId=response.meta['captchaId'], pCode=num)
            if response.meta.get('flag') == 'content':
                requets = MyRequests(url=url, headers=self.check_header, callback='req_contents', meta=meta, level=9)
                self.send_mqdata(requets)
            else:
                requets = MyRequests(url=url, headers=self.check_header, callback='req_content', meta=meta, level=9)
                self.send_mqdata(requets)
        else:
            print('检查出现问题，开始重回队列')
            if response.meta.get('pid'):
                self.send_mqdata(str(response.meta['pid'])+'~content~'+ str(response.meta['caseno']))
            else:
                self.send_mqdata(str(response.meta['caseno'])+'~'+str(response.meta['pname']) + '~' + str(int(response.meta['cishu']) + 1)+'~'+response.meta['pages'])

    def req_contents(self, response):
        if self.data_deal(response.text) == '1':
            url = 'http://zxgk.court.gov.cn/zhixing/newdetail?id={beizhi_id}&j_captcha={j_captcha}&captchaId={captchaId}&_=1575531482104'.format(beizhi_id=response.meta['pid'], j_captcha=str(response.meta['num']), captchaId=response.meta['captchaId'])
            request = MyRequests(url=url, headers=self.content_header, callback='get_content', meta=response.meta, level=8)
            self.send_mqdata(request)
        else:
            print('验证码出现问题，开始重回队列')
            self.send_mqdata(str(response.meta['pid'])+'~content~'+ str(response.meta['caseno']))

    def req_content(self, response):
        if self.data_deal(response.text) == '1':
            url = 'http://zxgk.court.gov.cn/zhixing/searchBzxr.do'
            data = {
                'pName': response.meta['pname'],
                'pCardNum': '',
                'selectCourtId': '0',
                'pCode': str(response.meta['num']),
                'captchaId': response.meta['captchaId'],
                'searchCourtName': '全国法院（包含地方各级法院）',
                'selectCourtArrange': '1',
                'currentPage': str(response.meta['pages'])
            }
            print(data)
            if str(response.meta['pages']) == '1':
                request = MyFormRequests(url=url, data=data, headers=self.content_header, callback='get_pages', meta=response.meta, level=3)
                self.send_mqdata(request)
            else:
                request = MyFormRequests(url=url, data=data, headers=self.content_header, callback='get_pid', meta=response.meta, level=4)
                self.send_mqdata(request)
        else:
            print('验证码出现问题，开始重回队列')
            self.send_mqdata(str(response.meta['caseno'])+'~'+str(response.meta['pname']) + '~' + str(int(response.meta['cishu']) + 1)+'~'+response.meta['pages'])

    def get_pages(self, response):
        try:
            # print(response.text)
            pages = json.loads(response.text)[0]['totalPage']
            print(pages)
            if int(pages) == 1:
                content = json.loads(response.text)[0]['result']
                if len(content) > 0:
                    for i in content:
                        pname_id = i.get('id')
                        print(pname_id)
                        self.send_mqdata(str(pname_id) + '~' + 'content~'+ str(response.meta['caseno']))
                if len(content) == 0:
                    item = {}
                    item['caseState'] = '全国法院被执行人查询平台已不纰漏'
                    item['update_source'] = '公示网'
                    item['update_status_time'] = self.now_time()
                    item['pname'] = response.meta['pname']
                    item['caseNo'] = response.meta['caseno']
                    item['body'] = content
                    item['source'] = 'http://zxgk.court.gov.cn/shixin/'
                    item['loadTime'] = self.now_time()
                    item['md5'] = self.production_md5(response.meta['caseno'] + response.meta['pname'])
                    self.insert(item, 'beizhixing_update', db_name='adjudicative')
            elif int(pages) >1:
                for page in range(2, int(pages)+1):
                    self.send_mqdata(str(response.meta['caseno'])+'~'+str(response.meta['pname']) + '~0~'+str(page))
        except:
            print('验证码出现问题，开始重回队列')
            self.send_mqdata(str(response.meta['caseno'])+'~'+str(response.meta['pname']) + '~' + str(int(response.meta['cishu']) + 1)+'~'+response.meta['pages'])

    def get_pid(self, response):
        if response.text != 'error':
            content = json.loads(response.text)[0]['result']
            print(response.meta['pname'], content)
            for i in content:
                pname_id = i.get('id')
                print(pname_id)
                self.send_mqdata(str(pname_id)+'~'+'content~'+ str(response.meta['caseno']))
        else:
            self.send_mqdata(str(response.meta['caseno'])+'~'+str(response.meta['pname']) + '~' + str(int(response.meta['cishu']) + 1)+'~'+response.meta['pages'])

    def get_content(self, response):
        try:
            content = json.loads(response.text)
            if len(content) == 0:
                self.send_mqdata(str(response.meta['pid']) + '~content~'+ str(response.meta['caseno']))
            else:
                item = {}
                pname = content.get('pname')
                sex = content.get('sexname')
                idcardNo = content.get('partyCardNum')
                court = content.get('execCourtName')
                sortTime = content.get('caseCreateTime')
                caseNo = content.get('caseCode')
                execMoney = content.get('execMoney')
                if caseNo == response.meta['caseno']:
                    item['caseState'] = '执行中'
                    item['caseNo'] = caseNo
                    item['update_source'] = '公示网'
                    item['update_status_time'] = self.now_time()
                    body = content
                    loadTime = self.now_time()
                    url = response.url
                    source = 'http://zxgk.court.gov.cn/zhixing/'
                    item['pname'] = pname
                    item['sex'] = sex
                    item['idcardNo'] = idcardNo
                    item['court'] = court
                    item['sortTime'] = sortTime
                    item['execMoney'] = execMoney
                    item['body'] = body
                    item['loadTime'] = loadTime
                    item['url'] = url
                    item['source'] = source
                    item['md5'] = self.production_md5(pname + str(body))
                    self.insert(item, 'beizhixing_update', db_name='adjudicative')
                    # self.prints(item)
                else:
                    item_one = {}
                    item_one['caseState'] = '全国法院被执行人查询平台已不纰漏'
                    item_one['update_source'] = '公示网'
                    item_one['update_status_time'] = self.now_time()
                    item_one['pname'] = pname
                    item_one['caseNo'] = response.meta['caseno']
                    item_one['source'] = 'http://zxgk.court.gov.cn/shixin/'
                    item_one['loadTime'] = self.now_time()
                    item_one['md5'] = self.production_md5(response.meta['caseno'] + pname)
                    self.insert(item_one, 'beizhixing_update', db_name='adjudicative')

                    item['caseState'] = '执行中'
                    item['caseNo'] = caseNo
                    item['update_source'] = '公示网'
                    item['update_status_time'] = self.now_time()
                    body = content
                    loadTime = self.now_time()
                    source = 'http://zxgk.court.gov.cn/zhixing/'
                    item['pname'] = pname
                    item['sex'] = sex
                    item['idcardNo'] = idcardNo
                    item['court'] = court
                    item['sortTime'] = sortTime
                    item['execMoney'] = execMoney
                    item['body'] = body
                    item['loadTime'] = loadTime
                    item['url'] = response.url
                    item['source'] = source
                    item['md5'] = self.production_md5(pname + str(body))
                    self.insert(item, 'beizhixing_update', db_name='adjudicative')
                    # self.prints(item)
        except Exception as e:
                print('出现异常，开始重回队列')
                self.send_mqdata(str(response.meta['pid'])+'~content~'+str(response.meta['caseno']))

if __name__ == '__main__':
    start_run = beizhixing_api()
    start_run.run('beizhixing_api')