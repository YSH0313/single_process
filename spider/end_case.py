from config.all_config import *
import importlib
importlib.reload(sys)

s = requests.Session()


class end_case(Manager):
    name='end_case'

    def __init__(self):
        Manager.__init__(self, 'ysh_end_case')
        self.insert_db = pymysql.connect(host='117.50.3.204', user='lym', password='Elements123', port=3306, db="adjudicative", charset='utf8', use_unicode=True)
        self.insert_cursor = self.insert_db.cursor()
        self.pdf_name = re.compile('http://zxgk\.court\.gov\.cn/xglfile/.*?/.*?/(.*?)pdf')
        self.code = re.compile("<script type='text/javascript' r='m'>.*?_\$.*?\('(.*?)'\);.*?</script>", re.S)
        self.header_img = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'Cookie': 'JSESSIONID=7CD091CD972DD65A7D97EDB8EAF5FFB9; _gscu_15322769=70521550o3616h14; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1575536041,1575596255,1575871264,1575941712; _gscbrs_15322769=1; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1575962147; _gscs_15322769=t75961297i2nu3q18|pv:5',
            'Host': 'zxgk.court.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        self.header_content = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Cookie': 'JSESSIONID=960891C1D9B7DE36D1BF3D3A7F7F4031; _gscu_15322769=70521550o3616h14; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1575536041,1575596255,1575871264,1575941712; _gscbrs_15322769=1; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1575962147; _gscs_15322769=t75961297i2nu3q18|pv:5',
            'Host': 'zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/zhongben/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.uuid_lists = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                           'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                           'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                           'x', 'y', 'z']

    def start_requests(self):
        lists = ['15239273', '1309196', '1309210', '14579545', '10715853', '10837210', '1599349', '14403693', '10791569', '11074303']
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
        img_url = 'http://zxgk.court.gov.cn/zhongben/captcha.do?captchaId={captchaId}&random=0.5612285532452921'.format(captchaId=captchaId)
        img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta={'pid': pid, 'captchaId': captchaId, 'cishu': cishu}, level=5)
        self.send_mqdata(img_request)

    def img_response(self, response):
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url='http://127.0.0.1:8008/zqsx'
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, callback='req_content', meta={'pid': response.meta['pid'], 'cishu': response.meta['cishu'], 'captchaId': response.meta['captchaId']}, level=6)
        self.send_mqdata(decode_requests)

    def req_content(self, response):
        num = response.text.replace('_', '')
        if len(num) == 4:
            print(num)
            url = 'http://zxgk.court.gov.cn/zhongben/searchZbDetail?id={pid}&j_captcha={j_captcha}&captchaId={captchaId}'.format(pid=response.meta['pid'], j_captcha=str(num), captchaId=response.meta['captchaId'])
            request = MyRequests(url=url, headers=self.header_content, callback='get_content', meta={'pid': response.meta['pid'], 'cishu': response.meta['cishu']}, level=7)
            self.send_mqdata(request)
        else:
            if int(response.meta['cishu'])>6:
                pass
            else:
                print('验证码出现问题，开始重回队列')
                self.send_mqdata(str(response.meta['pid'])+'~'+str(int(response.meta['cishu'])+1))

    def get_content(self, response):
        try:
            content = json.loads(response.text)
            if len(content) == 0:
                if int(response.meta['cishu']) > 6:
                    pass
                else:
                    print('未找到数据，开始重回队列', response.meta['pid'])
                    self.send_mqdata(str(response.meta['beizhi_id']) + '~' + str(int(response.meta['cishu']) + 1))
            else:
                item = {}
                body = content
                pid = response.meta['pid']
                title = self.data_deal(content.get('ah'))
                pname = self.data_deal(content.get('xm'))
                sex = self.data_deal(content.get('xb')).replace('09_00003-2', '女').replace('09_00003-1', '男')
                address = self.data_deal(content.get('dz'))
                court = self.data_deal(content.get('zxfymc'))
                caseNo = self.data_deal(content.get('ah'))
                lianTime = self.data_deal(content.get('larq'))
                sortTime = self.data_deal(content.get('jarq'))
                execMoney = self.data_deal(str(content.get('sqzxbdje')))
                unnexeMoney = self.data_deal(str(content.get('swzxbdje')))
                idcardNo = self.data_deal(content.get('sfzhm'))
                url = response.url
                source = 'http://zxgk.court.gov.cn/zhongben/'
                loadtime = self.now_time()
                MD5 = self.production_md5(str(content)+response.url)
                item['body'] = body
                item['pid'] = pid
                item['title'] = title
                item['pname'] = pname
                item['sex'] = sex
                item['address'] = address
                item['court'] = court
                item['caseNo'] = caseNo
                item['lianTime'] = lianTime
                item['sortTime'] = sortTime
                item['execMoney'] = execMoney
                item['unnexeMoney'] = unnexeMoney
                item['idcardNo'] = idcardNo
                item['url'] = url
                item['source'] = source
                item['loadtime'] = loadtime
                item['MD5'] = MD5
                # self.insert(item, 'zbaj', db_name='adjudicative')
                self.prints(item)
        except:
            if int(response.meta['cishu'])>6:
                pass
            else:
                print('出现异常，开始重回队列')
                self.send_mqdata(str(response.meta['pid'])+'~'+str(int(response.meta['cishu'])+1))


if __name__ == '__main__':
    start_run = end_case()
    start_run.run('end_case')