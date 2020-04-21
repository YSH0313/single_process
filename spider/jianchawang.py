# -*- coding: utf-8 -*-
from config.all_config import *


class jianchawang(Manager):
    name = 'jianchawang'

    def __init__(self):
        Manager.__init__(self, 'ysh_jianchawang')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.zhang = re.compile('>.*?审.*?判.*?长(.*?)<', re.S)
        self.yuan = re.compile('>.*?审.*?判.*?员(.*?)<', re.S)
        self.plaintiff = re.compile('赔偿请求人：(.*?)，|救助申请人：(.*?)，|公诉机关(.*?)，|原告人:(.*?)，|原告人：(.*?)，|原告人(.*?)，|原告:(.*?)，|原告：(.*?)，|原告(.*?)，|上诉人：(.*?)，|上诉人:(.*?)，|上诉人(.*?)，|申请执行人:(.*?)，|申请执行人：(.*?)，|申请执行人(.*?)，|再审申请人：(.*?)，|再审申请人:(.*?)，|再审申请人(.*?)，', re.S)
        self.pname = re.compile('赔偿义务机关：(.*?)，|被告人(.*?)，|被告:(.*?)，|被告：(.*?)，|被告(.*?)，|被上诉人：(.*?)，|被上诉人:(.*?)，|被上诉人(.*?)，|被执行人：(.*?)，|被执行人:(.*?)，|被执行人(.*?)，|被申请人：(.*?)，|被申请人:(.*?)，|被申请人(.*?)，',re.S)
        self.y_lawname = re.compile('原告.*?代理人:(.*?)，.*?被告|原告.*?代理人：(.*?)，.*?被告', re.S)
        self.b_lawname = re.compile('被告.*?代理人:(.*?)，|被告.*?代理人：(.*?)，', re.S)
        self.judgeresult = re.compile('判决如下：(.*?)审判|裁定如下：(.*?)审判|判决如下:(.*?)审判|裁定如下:(.*?)审判|结果如下：(.*?)审判|结果如下:(.*?)审判|如下调解协议：(.*?)审判|如下调解协议:(.*?)审判|如下协议：(.*?)审判|如下协议:(.*?)审判|协议如下：(.*?)审判|协议如下:(.*?)审判|支付令：(.*?)审判|支付令:(.*?)审判',re.S)
        self.caf = re.compile('案件受理费(.*?)元，', re.S)
        self.cafperson = re.compile('案件受理费.*?元.*?由(.*?)负担', re.S)
        self.courtclaims = re.compile('本院认为，(.*?)，判决如下|本院认为(.*?)判决如下', re.S)
        self.content_demo = re.compile('docText ="(.*?)"', re.S)
        self.content = re.compile("[\u4e00-\u9fa5]+", re.S)
        self.yiju = re.compile("依照(.*?)之规定|依照(.*?)的规定|依照(.*?)规定", re.S)

    def start_requests(self):
        url = 'http://www.ajxxgk.jcy.gov.cn/getFileListByPage'
        for page in range(1, 11879):
            data = {
                "codeId": "",
                "page": str(page),
                "size": "15",
                "fileType": "法律文书公开",
                "channelWebPath": "",
                "channelLevels": "",
                "time": "1"
            }
            request = MyFormRequests(url=url, data=data, callback=self.parse)
            self.send_mqdata(request)
    
    def parse(self, response):
        item = {}
        s = Selector(response=response)
        results = json.loads(response.text).get('results')
        if results:
            content = results.get('hits').get('hits')
            for data in content:
                title = data.get('title')
                postTime = self.deal_re(re.search('(.*?)T', data.get('publishedTimeForDate'), re.S))
                body = data.get('content')
                url = data.get('url')
                court = data.get('channel')[4]['displayName']
                wslx = data.get('domainMetaList')[0]['resultList'][1]['value']
                caseNo = data.get('domainMetaList')[1]['resultList'][0]['value']
                # print(title, postTime, court, wslx, url, body)
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
                sortTime = s.xpath('//*[@id="fontzoom"]/p[14]/span/text()').extract_first('')
                status = ['终结', '终审裁定', '审理完结', '审理中']
                plaintiff = None
                pname = None
                for i in status:
                    if (i in content) == True:
                        plaintiff = self.check_name(
                            self.deal_re_lists(self.plaintiff.findall(content.split(i)[0])))
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
                judgeresult = self.deal_re(self.judgeresult.search(content))
                caf = self.deal_re(self.caf.search(content))
                lawyer = self.get_lawyer(content)
                if caf != '':
                    caf = caf + '元'
                    item['caf'] = caf
                cafperson = self.deal_re(self.cafperson.search(content)).replace('被告', '').replace('被告人',
                                                                                                        '').replace(
                    '原告',
                    '').replace(
                    '被上诉人', '')
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
                item['wslx'] = wslx
                item['y_lawname'] = y_lawname
                item['causename'] = causename
                item['judgeresult'] = judgeresult
                item['cafperson'] = cafperson
                item['courtclaims'] = courtclaims
                item['caseNo'] = caseNo
                item['postTime'] = postTime
                item['court'] = court
                item['title'] = title
                item['caseType'] = caseType
                item['body'] = body
                item['detailUrl'] = url
                item['crawlTime'] = self.now_time()
                item['MD5'] = self.production_md5(str(data) + url)
                item['source'] = 'http://www.ajxxgk.jcy.gov.cn/12309/zjxflws/index.shtml'
                self.prints(item)
                # self.insert(item, db_name='adjudicative', table='caipan_new')


if __name__ == '__main__':
    start_run = jianchawang()
    start_run.run('jianchawang')