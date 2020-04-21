# -*- coding: utf-8 -*-
from config.all_config import *


class update_xgl(Manager):
    name = 'update_xgl'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_xgl')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'xgl'""")[0][0]
        all_id = self.select_data(['id'], 'adjudicative', 'xgl', cond="""where id > {last_id}""".format(last_id=last_id))
        # all_id = self.select_data(['id'], 'adjudicative', 'xgl', cond='order by id limit 100')
        self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='xgl'))
        for i in all_id:
            xgl_id = i[0]
            self.send_mqdata(str(xgl_id))


    def parse_only(self, body):
        xgl_id = body
        data = self.select_data(['body', 'title', 'pname', 'person_type', 'court', 'judge', 'caseNo', 'country',
                                 'address', 'execuno', 'execu_unit', 'publication_type', 'certype', 'cerno',
                                 'postTime', 'sortTime', 'sex', 'yiju', 'url', 'url_pdf', 'source', 'MD5'],
                                 'adjudicative', 'xgl', where="""id ={xgl_id}""".format(xgl_id=xgl_id))[0]
        body = data[0]
        title = data[1]
        pname = data[2]
        person_type = data[3]
        court = data[4]
        judge = data[5]
        caseNo = data[6]
        country = data[7]
        address = data[8]
        execuno = data[9]
        execu_unit = data[10]
        publication_type = data[1]
        certype = data[12]
        cerno = data[13]
        postTime = data[14]
        sortTime = data[15]
        sex = data[16]
        yiju = data[17]
        url = data[18]
        url_pdf = data[19]
        source = data[20]
        MD5 = data[21]

        item = {}
        if court:
            code_demo = self.select_data(['code', 'id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
            if code_demo:
                code = code_demo[0][0]
                if code:
                    item['courtname'] = code
                else:
                    code_id = code_demo[0][1]
                    item['courtname'] = 'z'+str(code_id)
            else:
                self.insert({'court': court}, 't_code_court', db_name='el_wash')
                code_id = self.select_data(['id'], 'el_wash', 't_code_court', where="""court='{court}'""".format(court=court))
                item['courtname'] = 'z'+str(code_id)
        item['title'] = title
        item['pname'] = pname
        item['content'] = body
        item['person_type'] = person_type
        item['judge'] = judge
        item['country'] = country
        item['CASENO'] = caseNo
        item['sdate'] = self.parseDate(sortTime)
        item['pdate'] = self.parseDate(postTime)
        item['EXENO'] = execuno
        item['exe_unit'] = execu_unit
        item['pub_type'] = publication_type
        item['CERNO'] = cerno
        item['CERTYPE'] = certype
        item['sex'] = sex
        item['address'] = address
        item['yiju'] = yiju
        item['source'] = source
        item['url'] = url
        item['url_pdf'] = url_pdf
        item['md5'] = MD5
        self.prints(item)
        # self.insert(item, 'rizhi_court_xgl', db_name='el_rizhi')


if __name__ == '__main__':
    start_run = update_xgl()
    start_run.run('update_xgl')