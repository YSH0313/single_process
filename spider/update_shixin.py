# -*- coding: utf-8 -*-
from config.all_config import *


class update_shixin(Manager):
    name = 'update_shixin'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_shixin')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'shixin'""")[0][0]
        all_id = self.select_data(['id'], 'adjudicative', 'shixin', cond="""where id > {last_id}""".format(last_id=last_id))
        # all_id = self.select_data(['id'], 'adjudicative', 'shixin', cond='order by id limit 100')
        self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='shixin'))
        for i in all_id:
            shixin_id = i[0]
            self.send_mqdata(str(shixin_id))

    def parse_only(self, body):
        shixin_id = body
        shixin_data = self.select_data(['pname', 'caseNo', 'casename', 'age',  'sex',  'cardNum',  'court',  'province',
                                        'caseNo_r', 'sorttime', 'reg',  'duty', 'performance',  'fulfilled',
                                        'fulfilled_no',  'disrupt',  'ptime',  'posttype', 'lstatus', 'personname',
                                        'casestatus', 'subject', 'url', 'address', 'source', 'json', 'load_time'],
                                        'adjudicative', 'shixin', where="""id={id}""".format(id=shixin_id))[0]
        pname = shixin_data[0]
        caseNo = shixin_data[1]
        casename = shixin_data[2]
        age = shixin_data[3]
        sex = shixin_data[4]
        cardNum = shixin_data[5]
        court = shixin_data[6]
        province = shixin_data[7]
        caseNo_r = shixin_data[8]
        sorttime = shixin_data[9]
        reg = shixin_data[10]
        duty = shixin_data[11]
        performance = shixin_data[12]
        fulfilled = shixin_data[13]
        fulfilled_no = shixin_data[14]
        disrupt = shixin_data[15]
        ptime = shixin_data[16]
        posttype = shixin_data[17]
        lstatus = shixin_data[18]
        personname = shixin_data[19]
        casestatus = shixin_data[20]
        subject = shixin_data[21]
        url = shixin_data[22]
        address = shixin_data[23]
        source = shixin_data[24]
        json = shixin_data[25]
        load_time = shixin_data[26]


        item = {}
        if court:
            code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
            if code_demo:
                code = code_demo[0][0]
                if code:
                    item['FSX_ZXFY'] = code
                else:
                    code_id = code_demo[0][1]
                    item['FSX_ZXFY'] = 'z'+str(code_id)
            else:
                self.insert({'court': court}, 't_code_court', db_name='el_wash')
                code_id = self.select_data(['id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                item['FSX_ZXFY'] = 'z'+str(code_id)

        ptime = self.parseDate(ptime)
        sorttime = self.parseDate(sorttime)
        item['id'] = shixin_id
        item['FSX_NAME'] = pname
        item['FSX_LB'] = posttype
        item['FSX_SEX'] = sex
        item['FSX_AGE'] = age
        item['FSX_SFZH_ALL'] = cardNum
        item['FSX_FRDB'] = personname
        item['FSX_AH'] = caseNo
        item['FSX_SF'] = province
        item['FSX_ZXYJ'] = caseNo_r
        item['FSX_LASJ'] = sorttime
        item['FSX_ZCZXDW'] = reg
        item['FSX_LXQK'] = performance
        item['FSX_SXJTQX'] = disrupt
        item['FSX_SXWS'] = duty
        item['FSX_FBDATE'] = ptime
        item['FSX_performed'] = fulfilled
        item['FSX_unperform'] = fulfilled_no
        item['FSX_CASENAME'] = casename
        item['FSX_LSTATUS'] = lstatus
        item['FSX_CASESTATUS'] = casestatus
        item['FSX_SUBJECT'] = subject
        item['FSX_URL'] = url
        item['FSX_ADDRESS'] = address
        item['FSX_SOURCE'] = source
        item['FSX_BODY'] = json
        if load_time:
            item['FSX_IDT'] = str(datetime.strptime(self.parseDate(load_time), "%Y-%m-%d").date())
        # self.prints(item)
        self.insert(item, 'rizhi_shixin', db_name='el_rizhi')


if __name__ == '__main__':
    start_run = update_shixin()
    start_run.run('update_shixin')