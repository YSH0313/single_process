# -*- coding: utf-8 -*-
from config.all_config import *


class update_bgt(Manager):
    name = 'update_bgt'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_bgt')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        # last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'bgt'""")[0][0]
        # all_id = self.select_data(['id'], 'adjudicative', 'sf_bgt', cond="""where id > {last_id}""".format(last_id=last_id))
        all_id = self.select_data(['id'], 'adjudicative', 'sf_bgt', cond='order by id limit 100')
        # self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='bgt'))
        for i in all_id:
            bgt_id = i[0]
            self.send_mqdata(str(bgt_id))
    
    def parse_only(self, body):
        bgt_id = body
        data = self.select_data(['sortTime', 'posttime', 'bdate', 'caseNo', 'pname', 'age', 'sex',
                                 'partyType', 'CERNO', 'CERTYPE', 'faren', 'address', 'proposer', 'cause', 'casecause',
                                 'yjdw', 'court', 'yiju', 'status', 'exemoney', 'unexemoney', 'url'],
                                'adjudicative', 'sf_bgt', where="""id ={bgt_id}""".format(bgt_id=bgt_id))[0]
        sortTime = data[0]
        posttime = data[1]
        bdate = data[2]
        caseNo = data[3]
        pname = data[4]
        age = data[5]
        sex = data[6]
        partyType = data[7]
        CERNO = data[8]
        CERTYPE = data[9]
        faren = data[10]
        address = data[11]
        proposer = data[12]
        cause = data[13]
        casecause = data[14]
        yjdw = data[15]
        court = data[16]
        yiju = data[17]
        status = data[18]
        exemoney = data[19]
        unexemoney = data[20]
        url = data[21]

        item = {}
        if court:
            code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court',
                                         where="""court='{court}'""".format(court=court))
            if code_demo:
                code = code_demo[0][0]
                if code:
                    item['court'] = code
                else:
                    code_id = code_demo[0][1]
                    item['court'] = 'z' + str(code_id)
            else:
                self.insert({'court': court}, 't_code_court', db_name='el_wash')
                code_id = self.select_data(['id'], 'el_wash', 't_code_court',
                                           where="""court='{court}'""".format(court=court))
                item['court'] = 'z' + str(code_id)

        if cause:
            xcode_demo = self.select_data(['xcode', 'id'], 'el_wash', 't_code_causename', where="""name='{name}'""".format(name=cause))
            if xcode_demo:
                xcode = xcode_demo[0][0]
                if xcode:
                    item['cause'] = xcode
                else:
                    xcode_id = xcode_demo[0][1]
                    item['cause'] = 'z'+str(xcode_id)
            else:
                self.insert({'name': cause}, 't_code_causename', db_name='el_wash')
                xcode_id = self.select_data(['id'], 'el_wash', 't_code_causename', where="""name='{name}'""".format(name=cause))
                item['cause'] = 'z'+str(xcode_id)

        item['sdate'] = self.parseDate(sortTime)
        item['ptime'] = self.parseDate(posttime)
        item['pname'] = pname
        item['CASENO'] = caseNo
        item['CERNO'] = CERNO
        item['CERTYPE'] = CERTYPE
        item['yiju'] = yiju
        item['faren'] = faren
        item['exemoney'] = exemoney
        item['unexemoney'] = unexemoney
        item['bdate'] = bdate
        item['status'] = status
        item['sqr'] = proposer
        item['address'] = address
        item['url'] = url
        item['age'] = age
        item['sex'] = sex
        item['partyType'] = partyType
        item['casecause'] = casecause
        item['yjdw'] = yjdw
        # self.prints(item)
        self.insert(item, 'rizhi_court_bgt', db_name='el_rizhi')


if __name__ == '__main__':
    start_run = update_bgt()
    start_run.run('update_bgt')