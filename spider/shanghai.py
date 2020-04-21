# -*- coding': 'utf-8 -*-
from config.all_config import *

s = requests.Session()
class ShangHai(Manager):
    name = 'ShangHai'

    def __init__(self):
        Manager.__init__(self, 'ysh_ShangHai')
        self.pages = re.compile("goPage\('(.*?)'\)", re.S)
        self.shenpan_z = re.compile(r'审.*?判.*?长.*?<td.*?width=.*?>(.*?)</td>', re.S)
        self.shenpan_y = re.compile(r'.*?审.*?判.*?员.*?<td.*?width=.*?>(.*?)</td>', re.S)
        self.headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Host': 'www.hshfy.sh.cn',
            'Referer': 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list.jsp?COLLCC=3404118589&ajlb=aYWpsYj3QzMrCz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.zhang = re.compile('>.*?审.*?判.*?长(.*?)<', re.S)
        self.yuan = re.compile('>.*?审.*?判.*?员(.*?)<', re.S)
        self.plaintiff = re.compile( '赔偿请求人：(.*?)，|救助申请人：(.*?)，|公诉机关(.*?)，|原告人:(.*?)，|原告人：(.*?)，|原告人(.*?)，|原告:(.*?)，|原告：(.*?)，|原告(.*?)，|上诉人：(.*?)，|上诉人:(.*?)，|上诉人(.*?)，|申请执行人:(.*?)，|申请执行人：(.*?)，|申请执行人(.*?)，|再审申请人：(.*?)，|再审申请人:(.*?)，|再审申请人(.*?)，', re.S)
        self.pname = re.compile( '赔偿义务机关：(.*?)，|被告人(.*?)，|被告:(.*?)，|被告：(.*?)，|被告(.*?)，|被上诉人：(.*?)，|被上诉人:(.*?)，|被上诉人(.*?)，|被执行人：(.*?)，|被执行人:(.*?)，|被执行人(.*?)，|被申请人：(.*?)，|被申请人:(.*?)，|被申请人(.*?)，', re.S)
        self.y_lawname = re.compile('原告.*?代理人:(.*?)，.*?被告|原告.*?代理人：(.*?)，.*?被告', re.S)
        self.b_lawname = re.compile('被告.*?代理人:(.*?)，|被告.*?代理人：(.*?)，', re.S)
        self.judgeresult = re.compile( '判决如下：(.*?)。|裁定如下：(.*?)。|判决如下:(.*?)。|裁定如下:(.*?)。|结果如下：(.*?)。|结果如下:(.*?)。|如下调解协议：(.*?)。|如下调解协议:(.*?)。|如下协议：(.*?)。|如下协议:(.*?)。|协议如下：(.*?)。|协议如下:(.*?)。|支付令：(.*?)。|支付令:(.*?)。', re.S)
        self.caf = re.compile('案件受理费(.*?)元，', re.S)
        self.cafperson = re.compile('案件受理费.*?元.*?由(.*?)负担', re.S)
        self.courtclaims = re.compile('本院认为，(.*?)，判决如下|本院认为(.*?)判决如下', re.S)
        self.content_demo = re.compile('docText ="(.*?)"', re.S)
        self.content = re.compile("[\u4e00-\u9fa5]+", re.S)
        self.yiju = re.compile("依照(.*?)之规定|依照(.*?)的规定|依照(.*?)规定", re.S)
        self.page = re.compile('共.*?<strong>(.*?)</strong>页', re.S)
        self.court = re.compile('<div align="center" class="style2">(.*?)法院.*?</div>', re.S)
        self.url = 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list_content.jsp'

    def start_requests(self):
        for page in range(20, 21):
            self.send_mqdata(str(page))

    def parse_only(self, body):
        page_num = body
        img_url = 'http://www.hshfy.sh.cn/shfy/code.do?n=' + str(random.uniform(0, 1))
        request = MyRequests(url=img_url, headers=self.headers, callback='img_response', meta={'page_num': page_num}, level=1)
        self.send_mqdata(request)

    def img_response(self, response):
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url='http://127.0.0.1:8009/zqsx'
        cookies = response.cookies
        cookies_lists = []
        for k, v in cookies.items():
            cookies_lists.append(str(v).replace('Set-Cookie: ', ''))
        img_header = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Host': 'www.hshfy.sh.cn',
            'Referer': 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list.jsp?COLLCC=3404118589&ajlb=aYWpsYj3QzMrCz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        img_header['Cookie'] = ';'.join(cookies_lists)
        response.meta['headers'] = img_header
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, headers=img_header, callback='check_status', meta=response.meta, level=2)
        self.send_mqdata(decode_requests)

    def check_status(self, response):
        code = response.text.replace('_', '')
        meta = response.meta
        meta['code'] = code
        check_url = 'http://www.hshfy.sh.cn/shfy/gweb2017/checkCode.jsp?code='+str(code)
        response_status = MyRequests(url=check_url, headers=response.meta['headers'], callback='status', meta=meta, level=3)
        self.send_mqdata(response_status)

    def status(self, response):
        if self.data_deal(response.text) == 'ok':
            print(response.meta['code'], self.data_deal(response.text))
            data = {'fydm': '', 'ah': '', 'ay': '', 'ajlb': '', 'wslb': '', 'title': '', 'jarqks': '', 'jarqjs': '',
                    'qwjs': '', 'wssj': '', 'yg': '', 'bg': '', 'spzz': '', 'flyj': '', 'pagesnum': str(response.meta['page_num']), 'zbah': ''}
            request = MyFormRequests(url=self.url, data=data, headers=response.meta['headers'], callback='get_lists', meta=response.meta, level=4)
            self.send_mqdata(request)
        else:
            self.send_mqdata(str(response.meta['page_num']))

    def get_lists(self, response):
        c = Selector(text=response.text)
        table = c.xpath('//table/tr[position()>1]')
        print(response.meta['page_num'], '页', len(table))
        if len(table) != 0:
            for i in table:
                title_href = 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_view.jsp?pa=' + str(i.xpath('./@onclick').re_first(r"showone\('\s*(.*)'\)"))
                caseNo = self.data_deal(i.xpath('./td[1]/text()').extract_first(''))
                title = self.data_deal(i.xpath('./td[2]/text()').extract_first(''))
                wslx = self.data_deal(i.xpath('./td[3]/text()').extract_first(''))
                causename = self.data_deal(i.xpath('./td[4]/text()').extract_first(''))
                sdate = self.data_deal(i.xpath('./td[7]/text()').extract_first(''))
                meta = response.meta
                meta['caseNo'] = caseNo
                meta['title'] = title
                meta['wslx'] = wslx
                meta['causename'] = causename
                meta['postTime'] = sdate
                request = MyRequests(url=title_href, headers=response.meta['headers'], callback='get_content', meta=meta, level=5)
                self.send_mqdata(request)
        else:
            self.send_mqdata(str(response.meta['page_num']))

    def get_content(self, response):
        item = {}
        content = self.replace_html(response.text)
        contents = self.replace_other(response.text)
        thirdparty = self.get_dsr(contents)
        lawname = self.get_lawname(contents)
        pnametext = self.get_pnametext(contents)
        plaintifftext = self.get_plaintifftext(contents)
        caseType = self.get_caseType(content)
        del_lists = []
        for i in plaintifftext:
            try:
                name = i[0]
                for n in pnametext:
                    if (name == n[0]):
                        del_lists.append(i)
            except:
                continue
        for i in del_lists:
            try:
                plaintifftext.remove(i)
            except:
                continue
        item['thirdparty'] = thirdparty
        item['b_lawname'] = lawname
        item['pnametext'] = pnametext
        item['plaintifftext'] = plaintifftext
        sortTime = self.data_deal(self.get_sorttime(content))
        status = ['终结', '终审裁定', '审理完结', '审理中']
        plaintiff = None
        pname = None
        for i in status:
            if (i in content) == True:
                plaintiff = self.check_name(self.deal_re_lists(self.plaintiff.findall(content.split(i)[0])))
                pname = self.check_name(self.deal_re_lists(self.pname.findall(content.split(i)[0])))
                [plaintiff.remove(i) for i in list(set(pname).intersection(set(plaintiff))) if True]
                item['status'] = i
                item['plaintiff'] = plaintiff
                item['pname'] = pname
        if (plaintiff == None) or (pname == None):
            plaintiff = self.check_name(self.deal_re_lists(self.plaintiff.findall(content)))
            pname = self.check_name(self.deal_re_lists(self.pname.findall(content)))
            [plaintiff.remove(i) for i in list(set(pname).intersection(set(plaintiff))) if True]
            item['plaintiff'] = plaintiff
            item['pname'] = pname
        y_lawname = self.deal_re(self.y_lawname.search(content))
        causename = self.data_deal(self.get_anyou(content))
        yiju = self.deal_re(self.yiju.search(content))
        judgeresult = self.deal_re(self.judgeresult.search(contents))
        caf = self.deal_re(self.caf.search(content))
        lawyer = self.get_lawyer(content)
        if caf != '':
            caf = caf + '元'
            item['caf'] = caf
        cafperson = self.deal_re(self.cafperson.search(content)).replace('被告', '').replace('被告人', '').replace('原告', '').replace('被上诉人', '')
        courtclaims = self.deal_re(self.courtclaims.search(content))
        judge_demo = self.deal_re(re.search(r'，审判(.*?)' + sortTime, content, re.S))
        if judge_demo != '':
            judge = '审判' + judge_demo
            judge_lists = judge.split('审')
            del judge_lists[0]
            judge_lists = ','.join(['审' + i for i in judge_lists])
            item['judge'] = judge_lists
        item['lawyer'] = lawyer
        item['yiju'] = yiju
        item['sortTime'] = sortTime
        item['wslx'] = response.meta['wslx']
        item['y_lawname'] = y_lawname
        item['causename'] = causename
        item['judgeresult'] = judgeresult
        item['cafperson'] = cafperson
        item['courtclaims'] = courtclaims
        item['caseNo'] = response.meta['caseNo']
        item['postTime'] = response.meta['postTime']
        item['court'] = self.data_deal(self.deal_re(self.court.search(response.text)) + '法院')
        item['title'] = response.meta['title']
        item['caseType'] = caseType
        item['body'] = response.text
        item['province'] = '上海'
        item['detailUrl'] = response.url
        item['crawlTime'] = self.now_time()
        item['MD5'] = self.production_md5(response.text + response.url)
        item['source'] = 'http://www.hshfy.sh.cn/shfy/gweb2017/flws_list.jsp'
        if '该域名不可访问' in item['body']:
            self.send_mqdata(str(response.meta['page_num']))
        else:
            # self.prints(item)
            self.insert(item, 'caipan_new', db_name='adjudicative')


if __name__ == '__main__':
    start_run = ShangHai()
    start_run.run('ShangHai')