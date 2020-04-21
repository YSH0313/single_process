from config.all_config import *


class ningxia(Manager):
    name = 'ningxia'

    def __init__(self):
        Manager.__init__(self, 'ysh_ningxia')
        self.title_id = re.compile("cpwsDetail\('(.*?)'\)", re.S)
        self.get_contents = re.compile(r'prepend\(unescape\("(.*?)"\)\);', re.S)
        self.plaintiff = re.compile('公诉机关(.*?)，|原告人:(.*?)，|原告人：(.*?)，|原告人(.*?)，|原告:(.*?)，|原告：(.*?)，|原告(.*?)，|上诉人：(.*?)，|上诉人:(.*?)，|上诉人(.*?)，|申请执行人:(.*?)，|申请执行人：(.*?)，|申请执行人(.*?)，|再审申请人：(.*?)，|再审申请人:(.*?)，|再审申请人(.*?)，',re.S)
        self.pname = re.compile('被告人(.*?)，|被告:(.*?)，|被告：(.*?)，|被告(.*?)，|被上诉人：(.*?)，|被上诉人:(.*?)，|被上诉人(.*?)，|被执行人：(.*?)，|被执行人:(.*?)，|被执行人(.*?)，|被申请人：(.*?)，|被申请人:(.*?)，|被申请人(.*?)，',re.S)
        self.y_lawname = re.compile('原告.*?代理人:(.*?)，.*?被告|原告.*?代理人：(.*?)，.*?被告', re.S)
        self.b_lawname = re.compile('被告.*?代理人:(.*?)，|被告.*?代理人：(.*?)，', re.S)
        self.judgeresult = re.compile('判决如下：(.*?)审判|裁定如下：(.*?)审判|判决如下:(.*?)审判|裁定如下:(.*?)审判|结果如下：(.*?)审判|结果如下:(.*?)审判|如下调解协议：(.*?)审判|如下调解协议:(.*?)审判|如下协议：(.*?)审判|如下协议:(.*?)审判|协议如下：(.*?)审判|协议如下:(.*?)审判|支付令：(.*?)审判|支付令:(.*?)审判',re.S)
        self.caf = re.compile('案件受理费(.*?)元，', re.S)
        self.cafperson = re.compile('案件受理费.*?元.*?由(.*?)负担', re.S)
        self.courtclaims = re.compile('本院认为，(.*?)，判决如下|本院认为(.*?)判决如下', re.S)
        self.content_demo = re.compile('docText ="(.*?)"', re.S)
        self.content = re.compile("[\u4e00-\u9fa5]+", re.S)
        self.yiju = re.compile("依照(.*?)之规定|依照(.*?)的规定|依照(.*?)规定", re.S)
        self.check_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': '',
            'Host': '218.95.176.205:8000',
            'Origin': 'http://218.95.176.205:8000',
            'Referer': 'http://218.95.176.205:8000/fymh/4000/cpws.htm?st=0&ssmzyy=&bhxjy=&q=&ajlb=&swzt=&wszl=&jbfy=&ay=&ah=&startCprq=&endCprq=&startFbrq=&endFbrq=&page=7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def start_requests(self):
        for page in range(1, 41):
            self.send_mqdata(str(page))
            # self.send_mqdata(str(1))
        # url = 'http://218.95.176.205:8000/cpws/paperView.htm?wsTypeSign=undefined&id=a1b99f19d140fc494dc8280790df4686&fy=4000'
        # request = MyRequests(url=url, callback=self.get_content)
        # self.send_mqdata(request)

    def parse_only(self, body):
        page = body
        img_url = 'http://218.95.176.205:8000/cpws_yzm.jpg?n=1'
        img_request = MyRequests(url=img_url, callback=self.img_response, meta={'page': page}, level=1)
        self.send_mqdata(img_request)

    def img_response(self, response):
        cookies = response.cookies
        meta = response.meta
        meta['cookie'] = str(cookies).replace('Set-Cookie: ', '').replace('; Path=/', '')
        img_byte = base64.b64encode(response.content)
        img_str = img_byte.decode('ascii')
        data = {'img': img_str}
        json_mod = json.dumps(data)
        decode_url = 'http://127.0.0.1:8008/zqsx'
        decode_requests = MyFormRequests(url=decode_url, data=json_mod, callback=self.check_img, meta=meta, level=2)
        self.send_mqdata(decode_requests)

    def check_img(self, response):
        code = response.text
        check_url = 'http://218.95.176.205:8000/cpws/checkTpyzm.htm'
        che_data = {
            'tpyzm': str(code)
        }
        meta = response.meta
        meta['code'] = code
        self.check_header['Cookie'] = response.meta['cookie']
        request = MyFormRequests(url=check_url, headers=self.check_header, data=che_data, callback=self.check_status, meta=meta, level=3)
        self.send_mqdata(request)

    def check_status(self, response):
        result = json.loads(response.text)
        if result.get('success'):
            print('请求成功', result.get('success'), response.meta['code'])
            self.check_header['Cookie'] = response.meta['cookie']
            url = 'http://218.95.176.205:8000/fymh/4000/cpws.htm?st=0&page={page}&yzm={yzm}'.format(page=response.meta['page'],yzm=str(response.meta['code']))
            request = MyRequests(url=url, callback=self.get_lists, headers=self.check_header, meta=response.meta, level=4)
            self.send_mqdata(request)
        else:
            self.send_mqdata(response.meta['page'])

    def get_lists(self, response):
        meta = response.meta
        s = Selector(response=response)
        table_lists = s.xpath('//*[@class="fd_table_03 "]/tr[position()>1]')
        print('第' + str(response.meta['page']) + '页', str(len(table_lists)) + '条', response.url)
        if len(table_lists) != 0:
            for i in table_lists:
                id_demo = i.xpath('./td[2]/@onclick').extract_first('')
                code = self.deal_re(self.title_id.search(id_demo))
                title = i.xpath('./td[2]/div/h3/a/@title').extract_first('')
                court = i.xpath('./td[4]/div/text()').extract_first('')
                postTime = i.xpath('./td[5]/div/text()').extract_first('')
                caseType = self.get_caseType(title)
                url = 'http://218.95.176.205:8000/cpws/paperView.htm?wsTypeSign=undefined&id={ids}&fy=4000'.format(ids=code)
                # if (postTime == self.getYesterday()) == True:
                meta['title'] = title
                meta['court'] = court
                meta['postTime'] = postTime
                meta['caseType'] = caseType
                request = MyRequests(url=url, callback=self.get_content, meta=meta, level=5)
                self.send_mqdata(request)
                # else:
                #     print('宁夏:暂无新数据')
        else:
            self.send_mqdata(response.meta['page'], level=10)

    def get_content(self, response):
        s = Selector(response=response)
        if response.text != '':
            if '不公开理由：' in response.text:
                item = {}
                wslx = s.xpath('//*[contains(text(),"文书种类：")]/text()').extract_first('').replace('文书种类：', '')
                caseType = s.xpath('//*[contains(text(),"案件类型：")]/text()').extract_first('').replace('案件类型：', '')
                caseNo = s.xpath('//*[contains(text(),"案号：")]/text()').extract_first('').replace('案号：', '')
                sortTime = s.xpath('//*[contains(text(),"裁判日期：")]/text()').extract_first('').replace('裁判日期：', '')
                data = response.text + response.url
                item['caseType'] = response.meta['caseType']
                item['title'] = response.meta['title']
                item['court'] = response.meta['court']
                item['wslx'] = wslx
                item['caseType'] = caseType
                item['caseNo'] = caseNo
                item['sortTime'] = sortTime
                item['body'] = response.text
                item['detailUrl'] = response.url
                item['crawlTime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                item['source'] = 'http://218.95.176.205:8000/fymh/4000/cpws.htm'
                item['MD5'] = self.production_md5(data)
                self.insert(item, db_name='adjudicative', table='caipan_closed')
                # self.prints(item)
            else:
                try:
                    item = {}
                    content = self.replace_html(self.get_contents.search(response.text).groups()[0].encode('latin-1').decode('unicode_escape'))
                    contents = self.replace_other(self.get_contents.search(response.text).groups()[0].encode('latin-1').decode('unicode_escape'))
                    thirdparty = self.get_dsr(contents)
                    lawname = self.get_lawname(contents)
                    pnametext = self.get_pnametext(contents)
                    plaintifftext = self.get_plaintifftext(contents)
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
                    sortTime = self.get_sorttime(content)
                    wslx = self.get_wslx(content[:50])
                    status = ['终结', '终审裁定', '审理完结', '审理中']
                    plaintiff = None
                    pname = None
                    for i in status:
                        if (i in content) == True:
                            plaintiff = self.check_name(self.deal_re_lists(self.plaintiff.findall(content.split(i)[0])))
                            pname = self.check_name(self.deal_re_lists(self.pname.findall(content.split(i)[0])))
                            item['status'] = i
                            item['plaintiff'] = plaintiff
                            item['pname'] = pname
                    if (plaintiff == None) or (pname == None):
                        plaintiff = self.check_name(self.deal_re_lists(self.plaintiff.findall(content)))
                        pname = self.check_name(self.deal_re_lists(self.pname.findall(content)))
                        item['plaintiff'] = plaintiff
                        item['pname'] = pname
                    y_lawname = self.deal_re(self.y_lawname.search(content))
                    causename = self.data_deal(self.get_anyou(content))
                    yiju = self.deal_re(self.yiju.search(content))
                    judgeresult = self.deal_re(self.judgeresult.search(content))
                    caf = self.deal_re(self.caf.search(content))
                    lawyer = self.get_lawyer(content)
                    caseNo = self.data_deal(self.get_caseno(content))
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
                    item['caseNo'] = caseNo
                    item['lawyer'] = lawyer
                    item['yiju'] = yiju
                    item['sortTime'] = sortTime
                    item['wslx'] = wslx
                    item['y_lawname'] = y_lawname
                    item['causename'] = causename
                    item['judgeresult'] = judgeresult
                    item['cafperson'] = cafperson
                    item['courtclaims'] = courtclaims
                    item['postTime'] = response.meta['postTime']
                    item['court'] = response.meta['court']
                    item['title'] = response.meta['title']
                    item['caseType'] = response.meta['caseType']
                    item['body'] = content
                    item['province'] = '宁夏'
                    item['detailUrl'] = response.url
                    item['crawlTime'] = self.now_time()
                    item['MD5'] = self.production_md5(response.text + response.url)
                    item['source'] = 'http://218.95.176.205:8000/fymh/4000/cpws.htm'
                    self.insert(item, db_name='adjudicative', table='caipan_new')
                    # self.prints(item)
                except:
                    pass
        else:
            request = MyRequests(url=response.url, headers=self.check_header, callback=self.get_content, meta=response.meta, level=5)
            self.send_mqdata(request)


if __name__ == '__main__':
    start_run = ningxia()
    start_run.run('ningxia')