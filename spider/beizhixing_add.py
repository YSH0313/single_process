# -*- coding: utf-8 -*-
import sys
sys.path.append("/root/shaohang/single_process")
from config.all_config import *


class beizhixing_add(Manager):
    name = 'beizhixing_add'
    custom_settings = {
        'Breakpoint': True
    }
    def __init__(self):
        Manager.__init__(self, 'ysh_beizhixing_add')
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.content_header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Cookie': '_gscu_15322769=70521550o3616h14; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1575448627,1575531479,1575536041,1575596255; _gscbrs_15322769=1; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1575596258; _gscs_15322769=t75618916gfxcay44|pv:2',
            'Host': 'zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/zhixing/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
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
        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'beizhixing_add'""")[0][0]
        second_id = int(last_id)-10000
        max_id = int(second_id)+150001
        self.update_data({'minid': max_id}, db_name='adjudicative', table='xd_updateid', where="""`table`='{table}'""".format(table='beizhixing_add'))
        for i in range(second_id, max_id):
            self.send_mqdata(str(i)+'~'+'0')

    def parse_only(self, body):
        data_demo = body.split('~')
        beizhi_id = data_demo[0]
        cishu = data_demo[1]
        captchaId = ''.join(random.sample(self.uuid_lists, 32))
        img_url = 'http://zxgk.court.gov.cn/zhixing/captcha.do?captchaId={captchaId}&random=0.7438759475304964'.format(captchaId=captchaId)
        img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta={'beizhi_id': beizhi_id, 'captchaId': captchaId, 'cishu': cishu}, level=1)
        self.send_mqdata(img_request)

    def img_response(self, response):
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url = 'http://127.0.0.1:8009/zqsx'
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, callback='check_img', meta=response.meta, level=2)
        self.send_mqdata(decode_requests)

    def check_img(self, response):
        num = response.text.replace('_', '')
        if len(num) == 4:
            meta = response.meta
            meta['num'] = num
            url = 'http://zxgk.court.gov.cn/zhixing/checkyzm?captchaId={captchaId}&pCode={pCode}'.format(captchaId=response.meta['captchaId'], pCode=num)
            requets = MyRequests(url=url, headers=self.check_header, callback='req_content', meta=meta, level=3)
            self.send_mqdata(requets)
        else:
            print('检查出现问题，开始重回队列')
            self.send_mqdata(response.meta['beizhi_id']+'~'+str(response.meta['cishu']+1))

    def req_content(self, response):
        if self.data_deal(response.text) == '1':
            url = 'http://zxgk.court.gov.cn/zhixing/newdetail?id={beizhi_id}&j_captcha={j_captcha}&captchaId={captchaId}&_=1575531482104'.format(beizhi_id=response.meta['beizhi_id'], j_captcha=str(response.meta['num']), captchaId=response.meta['captchaId'])
            request = MyRequests(url=url, headers=self.content_header, callback='get_content', meta=response.meta, level=4)
            self.send_mqdata(request)
        else:
            if int(response.meta['cishu']) > 3:
                pass
            else:
                print('验证码出现问题，开始重回队列')
                self.send_mqdata(str(response.meta['beizhi_id'])+'~'+str(int(response.meta['cishu'])+1))

    def get_content(self, response):
        try:
            content = json.loads(response.text)
            if len(content) == 0:
                if int(response.meta['cishu'])>3:
                    pass
                else:
                    print('未找到数据，开始重回队列', response.meta['beizhi_id'])
                    self.send_mqdata(str(response.meta['beizhi_id'])+'~'+str(int(response.meta['cishu'])+1))
            else:
                item = {}
                pname = content.get('pname')
                sex = content.get('sexname')
                idcardNo = content.get('partyCardNum')
                court = content.get('execCourtName')
                sortTime = content.get('caseCreateTime')
                caseNo = content.get('caseCode')
                execMoney = content.get('execMoney')
                body = content
                loadTime = self.now_time()
                url = response.url
                source = 'http://zxgk.court.gov.cn/zhixing/'
                item['pname'] = pname
                item['sex'] = sex
                item['idcardNo'] = idcardNo
                item['court'] = court
                item['sortTime'] = sortTime
                item['caseNo'] = caseNo
                item['execMoney'] = execMoney
                item['body'] = body
                item['loadTime'] = loadTime
                item['url'] = url
                item['source'] = source
                item['md5'] = self.production_md5(pname+str(body))
                self.insert(item, 'beizhixing_copy2', db_name='adjudicative')
                # self.prints(item)
        except:
            if int(response.meta['cishu'])>3:
                pass
            else:
                print('出现异常，开始重回队列')
                self.send_mqdata(str(response.meta['beizhi_id'])+'~'+str(int(response.meta['cishu'])+1))


if __name__ == '__main__':
    start_run = beizhixing_add()
    start_run.run('beizhixing_add')