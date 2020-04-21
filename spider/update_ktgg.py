# -*- coding: utf-8 -*-
import sys
# sys.path.append("/root/shaohang/single_process")
from config.all_config import *


class update_ktgg(Manager):
    name = 'update_ktgg'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_ktgg')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        # last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'ktgg_ysh'""")[0][0]
        # all_id = self.select_data(['id'], 'adjudicative', 'ktgg_kt', cond="""where id > {last_id}""".format(last_id=last_id))
        all_id = self.select_data(['id'], 'adjudicative', 'ktgg_kt', cond='where id >= 4494765 and id <= 4494865')
        # self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='ktgg_ysh'))
        for i in all_id:
            ktgg_id = i[0]
            self.send_mqdata(str(ktgg_id))

    def parse_only(self, body):
        ktgg_id = body
        data = self.select_data(['source', 'url', 'body', 'title', 'court', 'posttime', 'sorttime', 'pname',
                                 'plaintiff', 'party', 'courtNum', 'anyou', 'caseNo', 'province', 'organizer', 'judge',
                                 'description', 'md5', 'sign', 'load_time'],
                                'adjudicative', 'ktgg_kt', where="""id ={ktgg_id}""".format(ktgg_id=ktgg_id))[0]

        source = data[0]
        url = data[1]
        body = data[2]
        title = data[3]
        court = data[4]
        posttime = data[5]
        sorttime = data[6]
        pname = data[7]
        plaintiff = data[8]
        party = data[9]
        courtNum = data[10]
        anyou = data[11]
        caseNo = data[12]
        province = data[13]
        organizer = data[14]
        judge = data[15]
        description = data[16]
        md5 = data[17]
        sign = data[18]
        load_time = data[19]

        item = {}
        if court:
            code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
            if code_demo:
                code = code_demo[0][0]
                if code:
                    item['courtcode'] = code
                else:
                    code_id = code_demo[0][1]
                    item['courtcode'] = 'z'+str(code_id)
            else:
                self.insert({'court': court}, 't_code_court', db_name='el_wash')
                code_id = self.select_data(['id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                item['courtcode'] = 'z'+str(code_id)

        if anyou:
            xcode_demo = self.select_data(['xcode', 'id'], 'el_wash', 't_code_causename', where="""name='{name}'""".format(name=anyou))
            if xcode_demo:
                xcode = xcode_demo[0][0]
                if xcode:
                    item['causecode'] = xcode
                else:
                    xcode_id = xcode_demo[0][1]
                    item['causecode'] = 'z'+str(xcode_id)
            else:
                self.insert({'name': anyou}, 't_code_causename', db_name='el_wash')
                xcode_id = self.select_data(['id'], 'el_wash', 't_code_causename', where="""name='{name}'""".format(name=anyou))
                item['causecode'] = 'z'+str(xcode_id)

        item['sdate'] = self.parseDate(sorttime)
        item['CASENO'] = caseNo
        item['pname'] = pname
        item['title'] = title
        item['content'] = body
        item['court'] = court
        item['courtroom'] = courtNum
        item['causename'] = anyou
        item['organizer'] = organizer
        item['judge'] = judge
        if plaintiff:
            if '与' in plaintiff:
                plaintiff = plaintiff.replace('与', ',')
        if pname:
            if '与' in pname:
                pname = pname.replace('与', ',')
        item['party'] = {'plaintiff': self.data_deal(plaintiff), 'pname': self.data_deal(pname)}
        item['mid'] = md5
        item['url'] = url
        item['source'] = source
        # self.prints(item)
        self.insert(item, 'rizhi_court_ktgg', db_name='el_rizhi', OTHER_INSERT=True)


if __name__ == '__main__':
    start_run = update_ktgg()
    start_run.run('update_ktgg')