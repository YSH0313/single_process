from config.all_config import *

class shixin_limit(Manager):
    name = 'shixin_limit'

    def __init__(self):
        Manager.__init__(self, 'ysh_shixin_limit')
        self.yiju = re.compile('本院依照(.*?)规定，对你', re.S)
        self.court = re.compile('(.*?)法院', re.S)
        self.pdf_name = re.compile('http://zxgk\.court\.gov\.cn/xglfile/.*?/.*?/(.*?)pdf')
        self.code = re.compile("<script type='text/javascript' r='m'>.*?_\$.*?\('(.*?)'\);.*?</script>", re.S)
        self.header_img = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'Host': 'zxgk.court.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        }
        self.header_content = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'zxgk.court.gov.cn',
            'Origin': 'http://zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/xgl/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.check_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Host': 'zxgk.court.gov.cn',
            'Referer': 'http://zxgk.court.gov.cn/xgl/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.header_pdf = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.url = 'http://zxgk.court.gov.cn/xgl/showPDF'
        self.uuid_lists = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                           'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                           'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                           'x', 'y', 'z']

    def start_requests(self):
        lists = ['张三~0'
            # '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0',
            # '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0',
            # '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0',
            # '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0',
            # '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0',
            # '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0', '张三~0'
        ]
        for i in lists:
            self.send_mqdata(str(i))

    def parse_only(self, body):
        data_demo = body.split('~')
        captchaId = ''.join(random.sample(self.uuid_lists, 32))
        img_url = 'http://zxgk.court.gov.cn/xgl/captchaXgl.do?captchaId={captchaId}&random=0.8989795955515694'.format(captchaId=captchaId)
        if 'http://' in data_demo[0]:
            url = data_demo[0]
            cishu = data_demo[1]
            meta = {}
            meta['url'] = url
            meta['cishu'] = cishu
            meta['captchaId'] = captchaId
            img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta=meta, level=5)
            self.send_mqdata(img_request)
        else:
            pname = data_demo[0]
            cishu = data_demo[1]
            meta = {}
            meta['pname'] = pname
            meta['cishu'] = cishu
            meta['captchaId'] = captchaId
            img_request = MyRequests(url=img_url, headers=self.header_img, callback='img_response', meta=meta, level=1)
            self.send_mqdata(img_request)

    def img_response(self, response):
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url='http://127.0.0.1:8011/zqsx'
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, callback='check_img', meta=response.meta, level=2)
        self.send_mqdata(decode_requests)

    def check_img(self, response):
        print('检查用的代理：', response.proxy)
        num = response.text.replace('_', '')
        if len(num) == 4:
            meta = response.meta
            meta['num'] = num
            url = 'http://zxgk.court.gov.cn/xgl/checkyzm?captchaId={captchaId}&pCode={pCode}'.format(captchaId=response.meta['captchaId'], pCode=num)
            requets = MyRequests(url=url, headers=self.check_header, callback='req_content', meta=meta, level=3)
            self.send_mqdata(requets)
        else:
            print('验证码出现问题，开始重回队列')
            if response.meta.get('pname') != None:
                self.send_mqdata(response.meta['pname']+'~0')
            else:
                self.send_mqdata(response.meta['url'] + '~0')

    def req_content(self, response):
        print('查询用的代理：', response.proxy, response.text)
        if self.data_deal(response.text) == '1':
            if response.meta.get('pname') != None:
                url = 'http://zxgk.court.gov.cn/xgl/searchXgl.do?pName={pName}&pCardNum=&selectCourtId=0&pCode={pCode}&captchaId={captchaId}&searchCourtName=%E5%85%A8%E5%9B%BD%E6%B3%95%E9%99%A2%EF%BC%88%E5%8C%85%E5%90%AB%E5%9C%B0%E6%96%B9%E5%90%84%E7%BA%A7%E6%B3%95%E9%99%A2%EF%BC%89&selectCourtArrange=1&currentPage=1'.format(pName=response.meta['pname'], captchaId=response.meta['captchaId'], pCode=response.meta['num'])
                request = MyRequests(url=url, headers=self.header_content, callback='get_page', meta=response.meta, level=5)
                self.send_mqdata(request)
                request_content = MyRequests(url=url, headers=self.header_content, callback='get_content', meta=response.meta, level=4)
                self.send_mqdata(request_content)
            elif response.meta.get('url') != None:
                url = response.meta['url'].replace('captchaId_demo', response.meta['captchaId']).replace('pCode_demo', response.meta['num'])
                request_content = MyRequests(url=url, headers=self.header_content, callback='get_content', meta=response.meta, level=5)
                self.send_mqdata(request_content)
        else:
            print('打码错误，开始重回队列')
            if response.meta.get('pname') != None:
                self.send_mqdata(response.meta['pname']+'~0')
            else:
                self.send_mqdata(response.meta['url'] + '~0')

    def get_page(self, response):
        print('翻页用的代理：', response.proxy, response.text)
        try:
            content = json.loads(response.text)
            if len(content) == 0:
                if int(response.meta['cishu']) > 6:
                    pass
                else:
                    print('未找到数据，开始重回队列', response.meta['pname'])
                    if response.meta.get('pname') != None:
                        self.send_mqdata(response.meta['pname'] + '~0' + str(int(response.meta['cishu']) + 1))
                    else:
                        self.send_mqdata(response.meta['url'] + '~0')
            else:
                totalPage = content[0]['totalPage']
                for page in range(2, int(totalPage)+1):
                    url = 'http://zxgk.court.gov.cn/xgl/searchXgl.do?pName={pName}&pCardNum=&selectCourtId=0&pCode={pCode}&captchaId={captchaId}&searchCourtName=%E5%85%A8%E5%9B%BD%E6%B3%95%E9%99%A2%EF%BC%88%E5%8C%85%E5%90%AB%E5%9C%B0%E6%96%B9%E5%90%84%E7%BA%A7%E6%B3%95%E9%99%A2%EF%BC%89&selectCourtArrange=1&currentPage={currentPage}'.format(pName=response.meta['pname'], captchaId='captchaId_demo', pCode='pCode_demo', currentPage=page)
                    self.send_mqdata(url+'~0')

        except Exception as e:
            if int(response.meta['cishu']) > 6:
                pass
            else:
                print('出现异常，开始重回队列', e)
                if response.meta.get('pname') != None:
                    self.send_mqdata(response.meta['pname'] + '~0' + str(int(response.meta['cishu']) + 1))
                else:
                    self.send_mqdata(response.meta['url'] + '~0')

    def get_content(self, response):
        print('获取内容用的代理：', response.proxy, response.text)
        try:
            content = json.loads(response.text)
            if len(content) == 0:
                if int(response.meta['cishu']) > 6:
                    pass
                else:
                    print('未找到数据，开始重回队列', response.meta['pname'])
                    if response.meta.get('pname') != None:
                        self.send_mqdata(response.meta['pname'] + '~0' + str(int(response.meta['cishu']) + 1))
                    else:
                        self.send_mqdata(response.meta['url'] + '~0')
            else:
                content_demo = content[0]['result']
                for i in content_demo:
                    title = i.get('XM')
                    caseNo = i.get('AH')
                    sortTime = i.get('LASJStr')
                    sex = i.get('ZXFYMC')
                    url_pdf = 'http://zxgk.court.gov.cn/xglfile' + i.get('FILEPATH')
                    item = {}
                    item['title'] = title
                    item['pname'] = title
                    item['caseNo'] = caseNo
                    item['sortTime'] = sortTime
                    item['sex'] = sex
                    item['url'] = url_pdf
                    item['source'] = 'http://zxgk.court.gov.cn/xgl/'
                    pdf_analysis = MyRequests(url=url_pdf, headers=self.header_content, callback='get_response', meta={'item':item}, level=6)
                    self.send_mqdata(pdf_analysis, queue_name='ysh_shixin_limit')
        except Exception as e:
            if int(response.meta['cishu'])>6:
                pass
            else:
                print('出现异常，开始重回队列', e)
                if response.meta.get('pname') != None:
                    self.send_mqdata(response.meta['pname'] + '~0' + str(int(response.meta['cishu']) + 1))
                else:
                    self.send_mqdata(response.meta['url'] + '~0')

    def get_response(self, response):
        item = response.meta['item']
        contents = self.analysis(pdfFile=BytesIO(response.content))
        item['court'] = self.deal_re(self.court.search(contents)) + '法院'
        item['body'] = self.data_deal(contents)
        item['yiju'] = self.deal_re(self.yiju.search(contents)) + '的规定'
        item['MD5'] = self.production_md5(contents + response.url)
        item['loadtime'] = self.now_time()
        self.insert(item, 'xgl', db_name='adjudicative')
        # self.prints(item)

    def analysis(self, pdfFile):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        try:
            process_pdf(rsrcmgr, device, pdfFile)
        except:
            return ''
        device.close()
        content = retstr.getvalue()
        retstr.close()
        return content


if __name__ == '__main__':
    start_run = shixin_limit()
    start_run.run('shixin_limit')