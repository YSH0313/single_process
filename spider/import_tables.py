# -*- coding: utf-8 -*-
from config.all_config import *


class import_tables(Manager):
    name = 'import_tables'

    def __init__(self):
        Manager.__init__(self, 'ysh_import_tables')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        all_id = self.select_data(['id'], 'adjudicative', 'beizhixing_copy1', cond="""limit 100""")
        for i in all_id:
            beizhixing_id = i[0]
            self.send_mqdata(str(beizhixing_id)+'~beizhixing_copy1')

        all_id = self.select_data(['id'], 'adjudicative', 'beizhixing_copy2', cond="""limit 100""")
        for i in all_id:
            beizhixing_id = i[0]
            self.send_mqdata(str(beizhixing_id)+'~beizhixing_copy2')

    def parse_only(self, body):
        demo = body.split('~')
        beizhixing_id = demo[0]
        table_name = demo[1]
        data = self.select_data(['pname', 'age', 'sex', 'partyType', 'idcardNo', 'postTime', 'sortTime', 'caseNo',
                                 'post_type', 'court', 'caseState', 'caseCause', 'thirdParty', 'representativeNo',
                                 'legalRepresentative', 'yjdw', 'yjCode', 'title', 'end_time', 'out_time', 'proposer',
                                 'focusNumber', 'district', 'execMoney', 'body', 'loadTime', 'url', 'source', 'md5'],
                                'adjudicative', table_name, where="""id ={beizhixing_id}""".format(beizhixing_id=beizhixing_id))[0]
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
        title = data[17]
        end_time = data[18]
        out_time = data[19]
        proposer = data[20]
        focusNumber = data[21]
        district = data[22]
        execMoney = data[23]
        body = data[24]
        loadTime = data[25]
        url = data[26]
        source = data[27]
        md5 = data[28]
        item = {}
        item['pname'] = pname
        item['age'] = age
        item['sex'] = sex
        item['partyType'] = partyType
        item['idcardNo'] = idcardNo
        item['postTime'] = postTime
        item['sortTime'] = sortTime
        item['caseNo'] = caseNo
        item['post_type'] = post_type
        item['court'] = court
        item['caseState'] = caseState
        item['caseCause'] = caseCause
        item['thirdParty'] = thirdParty
        item['representativeNo'] = representativeNo
        item['legalRepresentative'] = legalRepresentative
        item['yjdw'] = yjdw
        item['yjCode'] = yjCode
        item['title'] = title
        item['end_time'] = end_time
        item['out_time'] = out_time
        item['proposer'] = proposer
        item['focusNumber'] = focusNumber
        item['district'] = district
        item['execMoney'] = execMoney
        item['body'] = body
        item['loadTime'] = loadTime
        item['url'] = url
        item['source'] = source
        item['md5'] = md5
        self.insert(item, 'beizhixing', db_name='adjudicative')

if __name__ == '__main__':
    start_run = import_tables()
    start_run.run('import_tables')