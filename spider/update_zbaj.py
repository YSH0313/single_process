# -*- coding: utf-8 -*-
from config.all_config import *


class update_zbaj(Manager):
    name = 'update_zbaj'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_zbaj')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        # last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'zbaj'""")[0][0]
        # all_id = self.select_data(['id'], 'adjudicative', 'zbaj', cond="""where id > {last_id}""".format(last_id=last_id))
        all_id = self.select_data(['id'], 'adjudicative', 'zbaj', cond='order by id limit 100')
        # self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='zbaj'))
        for i in all_id:
            zbaj_id = i[0]
            self.send_mqdata(str(zbaj_id))


    def parse_only(self, body):
        zbaj_id = body
        data = self.select_data(['body', 'pid', 'title', 'pname', 'sex', 'address', 'court', 'caseNo', 'postTime', 'lianTime',
                                 'anyou', 'anyouzb', 'sortTime', 'execMoney', 'unnexeMoney', 'idcardNo', 'url', 'source',
                                 'loadtime', 'MD5'], 'adjudicative', 'zbaj', where="""id ={zbaj_id}""".format(zbaj_id=zbaj_id))[0]
        body = data[0]
        pid = data[1]
        title = data[2]
        pname = data[3]
        sex = data[4]
        address = data[5]
        court = data[6]
        caseNo = data[7]
        postTime = data[8]
        lianTime = data[9]
        anyou = data[10]
        anyouzb = data[11]
        sortTime = data[12]
        execMoney = data[13]
        unnexeMoney = data[14]
        idcardNo = data[15]
        url = data[16]
        source = data[17]
        loadtime = data[18]
        MD5 = data[19]

        item = {}
        if court:
            code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
            if code_demo:
                code = code_demo[0][0]
                if code:
                    item['court'] = code
                else:
                    code_id = code_demo[0][1]
                    item['court'] = 'z'+str(code_id)
            else:
                self.insert({'court': court}, 't_code_court', db_name='el_wash')
                code_id = self.select_data(['id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                item['court'] = 'z'+str(code_id)
        item['body'] = body
        item['pid'] = pid
        item['title'] = title
        item['pname'] = pname
        item['sex'] = sex
        item['address'] = address
        # item['court'] = court
        item['caseNo'] = caseNo
        item['postTime'] = postTime
        item['lianTime'] = self.parseDate(lianTime)
        item['anyou'] = anyou
        item['anyouzb'] = anyouzb
        item['sortTime'] = self.parseDate(sortTime)
        item['execMoney'] = execMoney
        item['unnexeMoney'] = unnexeMoney
        item['idcardNo'] = idcardNo
        item['url'] = url
        item['source'] = source
        item['loadtime'] = loadtime
        item['MD5'] = MD5
        # self.prints(item)
        self.insert(item, 'rizhi_court_zbaj', db_name='el_rizhi')


if __name__ == '__main__':
    start_run = update_zbaj()
    start_run.run('update_zbaj')