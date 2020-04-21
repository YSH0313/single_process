from config.all_config import *


class shixin_beizhi(Manager):
    name = 'shixin_beizhi'

    def __init__(self):
        Manager.__init__(self, 'ysh_shixin_beizhi')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.header_img = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'Cookie': 'JSESSIONID=7E0DC9EAB1505F9FD3177789FF19377D; _gscu_15322769=70521550o3616h14; _gscbrs_15322769=1; SESSION=48b84ab2-2ef1-458b-af8e-691d670c7a69; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1573436346,1573437717,1573438136,1573456566; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1573457425; _gscs_15322769=t73456562txbjmk18|pv:4',
            'Host': 'zxgk.court.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        self.header_content = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'Cookie': 'JSESSIONID=7A46A582A68E1612C80D89F43DA4C765; _gscu_15322769=70521550o3616h14; _gscbrs_15322769=1; SESSION=48b84ab2-2ef1-458b-af8e-691d670c7a69; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1573436346,1573437717,1573438136,1573456566; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1573457723; _gscs_15322769=t73456562txbjmk18|pv:6',
            'Host': 'zxgk.court.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        self.check_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
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
        lists = ['700198325', '124713589', '517146749', '700676557', '701613118', '702933434', '703707400', '704851818', '704851818', '705696432', '706584258']
        for i in lists:
            self.send_mqdata(str(i))

    def parse_only(self, body):
        if '~' in body:
            data_demo = body.split('~')
            pid = data_demo[0]
            cishu = data_demo[1]
        else:
            pid = body
            cishu = '0'
        captchaId = ''.join(random.sample(self.uuid_lists, 32))
        img_url = 'http://zxgk.court.gov.cn/shixin/captchaNew.do?captchaId={captchaId}&random=0.9222752653255852'.format(captchaId=captchaId)
        img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta={'pid': pid, 'captchaId': captchaId, 'cishu': cishu},  level=5)
        self.send_mqdata(img_request)

    def img_response(self, response):
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url='http://127.0.0.1:8011/zqsx'
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, callback='check_img', meta=response.meta,  level=6)
        self.send_mqdata(decode_requests)

    def check_img(self, response):
        num = response.text.replace('_', '')
        if len(num) == 4:
            meta = response.meta
            meta['num'] = num
            url = 'http://zxgk.court.gov.cn/shixin/checkyzm.do?captchaId={captchaId}&pCode={pCode}'.format(captchaId=response.meta['captchaId'], pCode=num)
            requets = MyRequests(url=url, headers=self.check_header, callback='req_content', meta=meta, level=3)
            self.send_mqdata(requets)
        else:
            print('检查出现问题，开始重回队列')
            self.send_mqdata(response.meta['pid']+'~'+str(response.meta['cishu']+1))

    def req_content(self, response):
        if self.data_deal(response.text) == '1':
            url = 'http://zxgk.court.gov.cn/shixin/disDetailNew?id={pid}&pCode={pCode}&captchaId={captchaId}'.format(pid=response.meta['pid'], pCode=str(response.meta['num']), captchaId=response.meta['captchaId'])
            request = MyRequests(url=url, headers=self.header_content, callback='get_content', meta=response.meta, level=7)
            self.send_mqdata(request)
        else:
            if int(response.meta['cishu'])>3:
                pass
            else:
                print('验证码出现问题，开始重回队列')
                self.send_mqdata(str(response.meta['pid'])+'~'+str(int(response.meta['cishu'])+1))

    def get_content(self, response):
        try:
            content = json.loads(response.text)
            if len(content) == 0:
                if int(response.meta['cishu'])>3:
                    pass
                else:
                    print('未找到数据，开始重回队列', response.meta['pid'])
                    self.send_mqdata(str(response.meta['pid']) + '~' + str(int(response.meta['cishu']) + 1))
            else:
                # pass
                item = {}
                pname = content.get('iname')
                sex = content.get('sexy')
                cardNum = content.get('cardNum')
                courtName = content.get('courtName')
                province = content.get('areaName')
                caseNo_r = content.get('gistId')
                sorttime = content.get('regDate')
                caseCode = content.get('caseCode')
                reg = content.get('gistUnit')
                duty = content.get('duty')
                performance = content.get('performance')
                disrupt = content.get('disruptTypeName')
                publishDate = content.get('publishDate')
                sid = content.get('id')
                age = content.get('age')

                item['pname'] = pname
                item['sex'] = sex
                item['cardNum'] = cardNum
                item['court'] = courtName
                item['province'] = province
                item['caseNo_r'] = caseNo_r
                item['sorttime'] = sorttime
                item['caseNo'] = caseCode
                item['reg'] = reg
                item['duty'] = duty
                item['performance'] = performance
                item['disrupt'] = disrupt
                item['ptime'] = publishDate
                item['sid'] = sid
                item['age'] = age
                item['json'] = content
                item['url'] = response.url
                item['source'] = 'http://zxgk.court.gov.cn/shixin/'
                item['load_time'] = self.now_time()
                item['md5'] = self.production_md5(json.dumps(content)+response.url)
                # self.prints(item)
                self.insert(item, 'shixin', db_name='adjudicative')
        except Exception as e:
            if int(response.meta['cishu'])>3:
                pass
            else:
                print(repr(e))
                print('出现异常，开始重回队列')
                self.send_mqdata(str(response.meta['pid'])+'~'+str(int(response.meta['cishu'])+1))



if __name__ == '__main__':
    start_run = shixin_beizhi()
    start_run.run('shixin_beizhi')