# -*- coding: utf-8 -*-
import sys
# sys.path.append("/root/shaohang/single_process")
from config.all_config import *


class update_beizhixing(Manager):
    name = 'update_beizhixing'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_beizhixing')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'beizhixing'""")[0][0]
        all_id = self.select_data(['id'], 'adjudicative', 'beizhixing', cond="""where id > {last_id}""".format(last_id=last_id))
        # all_id = self.select_data(['id'], 'adjudicative', 'beizhixing', cond='order by id limit 1000')
        self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='beizhixing'))
        for i in all_id:
            beizhixing_id = i[0]
            self.send_mqdata(str(beizhixing_id))

        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'beizhixing'""")[0][0]
        all_id = self.select_data(['id'], 'adjudicative', 'beizhixing', cond="""where id > {last_id}""".format(last_id=last_id))
        # all_id = self.select_data(['id'], 'adjudicative', 'beizhixing', cond='order by id limit 1000')
        self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='beizhixing'))
        for i in all_id:
            beizhixing_id = i[0]
            self.send_mqdata(str(beizhixing_id))

    def parse_only(self, body):
        beizhixing_id = body
        data = self.select_data(['pname', 'age', 'sex', 'partyType', 'idcardNo', 'postTime', 'sortTime', 'caseNo',
                                 'post_type', 'court', 'caseState', 'caseCause', 'thirdParty', 'representativeNo',
                                 'legalRepresentative', 'yjdw', 'yjCode', 'end_time', 'out_time', 'proposer',
                                 'focusNumber', 'district', 'execMoney', 'url', 'md5', 'source'],
                                'adjudicative', 'beizhixing', where="""id ={beizhixing_id}""".format(beizhixing_id=beizhixing_id))[0]
        pname = data[0]
        age = data[1]
        sex = data[2]
        partyType = data[3]
        idcardNo = data[4]
        postTime = data[5]
        sortTime = data[6]
        caseNo = data[7]
        post_type = data[8]
        court = data[9]
        caseState = data[10]
        caseCause = data[11]
        thirdParty = data[12]
        representativeNo = data[13]
        legalRepresentative = data[14]
        yjdw = data[15]
        yjCode = data[16]
        end_time = data[17]
        out_time = data[18]
        proposer = data[19]
        focusNumber = data[20]
        district = data[21]
        execMoney = data[22]
        url = data[23]
        md5 = data[24]
        source = data[25]

        item = {}
        if court:
            code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
            if code_demo:
                code = code_demo[0][0]
                if code:
                    item['FSS_COURT'] = code
                else:
                    code_id = code_demo[0][1]
                    item['FSS_COURT'] = 'z' + str(code_id)
            else:
                self.insert({'court': court}, 't_code_court', db_name='el_wash')
                code_id = self.select_data(['id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                item['FSS_COURT'] = 'z' + str(code_id)

        if caseCause:
            xcode_demo = self.select_data(['xcode', 'id'], 'el_wash', 't_code_causename', where="""name='{name}'""".format(name=caseCause))
            if xcode_demo:
                xcode = xcode_demo[0][0]
                if xcode:
                    item['caseCause'] = xcode
                else:
                    xcode_id = xcode_demo[0][1]
                    item['caseCause'] = 'z' + str(xcode_id)
            else:
                self.insert({'name': caseCause}, 't_code_causename', db_name='el_wash')
                xcode_id = self.select_data(['id'], 'el_wash', 't_code_causename', where="""name='{name}'""".format(name=caseCause))
                item['caseCause'] = 'z' + str(xcode_id)

        item['FSS_CASENO'] = caseNo
        item['FSS_NAME'] = pname
        item['FSS_STATUS'] = caseState
        item['FSS_MONEY'] = execMoney
        item['FSS_REGNO'] = idcardNo
        item['FSS_LASJ'] = self.parseDate(sortTime)
        item['FSS_ENDDATE'] = self.parseDate(end_time)
        item['FSS_OUTDATE'] = self.parseDate(out_time)
        item['FSS_AREACODE'] = district
        item['FSS_SQR'] = proposer
        item['FSS_FOCUSNB'] = focusNumber
        item['FSS_IDT'] = self.now_time()
        item['age'] = age
        item['sex'] = sex
        item['partyType'] = partyType
        item['postTime'] = self.parseDate(postTime)
        item['post_type'] = post_type
        item['thirdParty'] = thirdParty
        item['representativeNo'] = representativeNo
        item['legalRepresentative'] = legalRepresentative
        item['yjdw'] = yjdw
        item['yjCode'] = yjCode
        item['url'] = url
        item['md5'] = md5
        item['source'] = source
        # self.prints(item)
        self.insert(item, 'rizhi_court_beizhixing', db_name='el_rizhi', OTHER_INSERT=True)


if __name__ == '__main__':
    start_run = update_beizhixing()
    start_run.run('update_beizhixing')