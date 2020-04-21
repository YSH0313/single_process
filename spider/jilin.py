from config.all_config import *


class jilin(Manager):
    name = 'jilin'

    def __init__(self):
        Manager.__init__(self, 'ysh_jilin')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.total = re.compile('查询到<em>(.*?)</em>个', re.S)
        self.code = re.compile(r"javascript:zxsxDetail\('(.*?)'\);", re.S)
        self.fy = re.compile(r"fymh/(.*?)/zxgk", re.S)

    def start_requests(self):
        update_allurl = self.select_data(['id', 'url'], 'el_rizhi', 'rizhi_court_beizhixing',
                                         where="""(FSS_NAME = '') and (FSS_CASENO = '') and (url like '%susong51%')""")
        for i in update_allurl:
            update_id = i[0]
            url = i[1]
            img_request = MyRequests(url=url, meta={'update_id': update_id}, callback='parse_only')
            self.send_mqdata(img_request)

    def parse_only(self, response):
        #     data_demo = body.split('~')
        #     court = data_demo[0]
        #     url = data_demo[1]
        #     cishu = data_demo[2]
        #     host = self.get_host(url)
        #     img_url = 'http://{host}/susong51/cpws_yzm.jpg?n=1'.format(host=host)
        #     img_request = MyRequests(url=img_url, callback='img_response', meta={'court': court, 'url': url, 'cishu': cishu, 'host': host, 'source': url}, level=1)
        #     self.send_mqdata(img_request)
        #
        # def img_response(self, response):
        #     img_byte = base64.b64encode(response.content)
        #     img_str = img_byte.decode('ascii')
        #     data = {'img': img_str}
        #     json_mod = json.dumps(data)
        #     decode_url='http://127.0.0.1:8009/zqsx'
        #     cookies = response.cookies
        #     cookies_lists = []
        #     for k, v in cookies.items():
        #         cookies_lists.append(str(v).replace('Set-Cookie: ', ''))
        #     img_header = {
        #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #         'Accept-Encoding': 'gzip, deflate',
        #         'Accept-Language': 'zh-CN,zh;q=0.9',
        #         'Cache-Control': 'max-age=0',
        #         'Connection': 'keep-alive',
        #         'Host': 'www.xjcourt.gov.cn',
        #         'Upgrade-Insecure-Requests': '1',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
        #     }
        #     img_header['Cookie'] = ';'.join(cookies_lists)
        #     response.meta['headers'] = img_header
        #     decode_requests = MyFormRequests(url=decode_url, data=json_mod, headers=img_header, callback='check_status', meta=response.meta, level=2)
        #     self.send_mqdata(decode_requests)
        #
        # def check_status(self, response):
        #     code = response.text
        #     if len(code) == 5:
        #         print(code)
        #         check_url = 'http://{host}/susong51/cpws/checkTpyzm.htm'.format(host=response.meta['host'])
        #         che_data = {
        #             'tpyzm': str(code)
        #         }
        #         response.meta['code'] = code
        #         request = MyFormRequests(url=check_url, data=che_data, headers=response.meta['headers'], callback='status', meta=response.meta, level=3)
        #         self.send_mqdata(request)
        #     else:
        #         print('验证码出现问题，重回队列')
        #         self.send_mqdata(response.meta['court']+'~'+response.meta['url']+'~0')
        #
        # def status(self, response):
        #     status = json.loads(response.text)['success']
        #     print(status)
        #     if status == True:
        #         urls = response.meta['url']+'&yzm={yzm}'.format(yzm=str(response.meta['code']))
        #         if '&page=' not in response.meta['url']:
        #             pages_request = MyRequests(url=urls, headers=response.meta['headers'], callback='get_pages', meta=response.meta, level=1)
        #             self.send_mqdata(pages_request)
        #         request = MyRequests(url=urls, headers=response.meta['headers'], callback='get_lists', meta=response.meta, level=4)
        #         self.send_mqdata(request)
        #     else:
        #         print('打码错误，重回队列')
        #         self.send_mqdata(response.meta['court']+'~'+response.meta['url']+'~0')

        # def get_pages(self, response):
        #     if '没有搜索到被执行人信息' in response.text:
        #         print('没有搜索到被执行人信息，重回队列')
        #         self.send_mqdata(response.meta['court']+'~'+response.meta['url']+'~0')
        #     if '没有搜索到被执行人信息' not in response.text:
        #         total = self.deal_re(self.total.search(response.text))
        #         print(total)
        #         if total != '':
        #             pages = ceil(int(total)/10)
        #             for page in range(2, pages+1):
        #                 url = response.meta['url']+'&page={page}'.format(page=page)
        #                 self.send_mqdata(response.meta['court']+'~'+url+'~0')

        # def get_lists(self, response):
        #     s = Selector(response=response)
        #     table_lists = s.xpath('//table[@class="fd_table_03 "]/tr[position()>1]')
        #     if len(table_lists) == 0:
        #         self.send_mqdata(response.meta['court']+'~'+response.meta['url']+'~0')
        #     if len(table_lists) != 0:
        #         print('成功')
        #         for i in table_lists:
        #             code = self.deal_re(self.code.search(i.xpath('./td[2]/@onclick').extract_first('')))
        #             fy = self.deal_re(self.fy.search(response.meta['source']))
        #             url = 'http://{host}/susong51/pub/zxgk/detail.htm?bh={bh}&fy={fy}'.format(host=response.meta['host'], bh=code, fy=fy)
        #             request = MyRequests(url=url, headers=response.meta['headers'], callback='get_content', meta=response.meta, level=5)
        #             self.send_mqdata(request)

        # def get_content(self, response):
        item = {}
        s = Selector(text=response.text)
        pname = s.xpath('//div[contains(text(), "被执行人姓名/名称")]/parent::td/following-sibling::td/div/text()').extract_first('')
        partyType = s.xpath('//div[contains(text(), "被执行人类型")]/parent::td/following-sibling::td/div/text()').extract_first('')
        idcardNo = s.xpath('//div[contains(text(), "证件号码")]/parent::td/following-sibling::td/div/text()').extract_first('')
        sex = s.xpath('//div[contains(text(), "被执行人性别")]/parent::td/following-sibling::td/div/text()').extract_first('')
        age = s.xpath('//div[contains(text(), "被执行人年龄")]/parent::td/following-sibling::td/div/text()').extract_first('')
        caseNo = s.xpath('//div[contains(text(), "案号")]/parent::td/following-sibling::td/div/text()').extract_first('')
        sortTime = s.xpath('//div[contains(text(), "立案日期")]/parent::td/following-sibling::td/div/text()').extract_first('')
        court = self.data_deal(s.xpath('//div[contains(text(), "执行法院")]/parent::td/following-sibling::td/div/text()').extract_first(''))
        caseState = s.xpath('//div[contains(text(), "案件状态")]/parent::td/following-sibling::td/div/text()').extract_first('')
        execMoney = s.xpath('//div[contains(text(), "申请执行标的金额")]/parent::td/following-sibling::td/div/text()').extract_first('')
        yjCode = s.xpath('//div[contains(text(), "执行依据文书编号")]/parent::td/following-sibling::td/div/text()').extract_first('')
        yjdw = s.xpath('//div[contains(text(), "经办机构（做出执行依据单位）")]/parent::td/following-sibling::td/div/text()').extract_first('')
        postTime = s.xpath('//div[contains(text(), "发布日期")]/parent::td/following-sibling::td/div/text()').extract_first('')
        if (caseNo == '') and (pname == '') and (response.status_code == 200):
            img_request = MyRequests(url=response.url, callback='parse_only')
            self.send_mqdata(img_request)
        elif (caseNo != '') and (pname != '') and (response.status_code == 200):
            if court:
                code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                print(code_demo)
                if code_demo:
                    code = code_demo[0][0]
                    if code:
                        print(code)
                        item['FSS_COURT'] = code
                    else:
                        code_id = code_demo[0][1]
                        print(code_id)
                        item['FSS_COURT'] = 'z' + str(code_id)
                else:
                    self.insert({'court': court}, 't_code_court', db_name='el_wash')
                    code_id = self.select_data(['id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                    item['FSS_COURT'] = 'z' + str(code_id)

            item['FSS_CASENO'] = caseNo
            item['FSS_NAME'] = pname
            item['FSS_STATUS'] = caseState
            item['FSS_MONEY'] = execMoney
            item['FSS_REGNO'] = idcardNo
            item['FSS_LASJ'] = self.parseDate(sortTime)
            item['FSS_IDT'] = self.now_time()
            item['age'] = age
            item['sex'] = sex
            item['partyType'] = partyType
            item['postTime'] = self.parseDate(postTime)
            item['yjdw'] = yjdw
            item['yjCode'] = yjCode
            # item['url'] = response.url
            item['md5'] = self.production_md5(response.url + response.text)
            self.update_data(item, db_name='el_rizhi', table='rizhi_court_beizhixing',
                             where="""id = {update_id}""".format(update_id=response.meta['update_id']))
            # self.prints(item)


if __name__ == '__main__':
    start_run = jilin()
    start_run.run('jilin')