# -*- coding: utf-8 -*-
from config.all_config import *


class add_beizhixing_source(Manager):
    name = 'add_beizhixing_source'

    def __init__(self):
        Manager.__init__(self, 'ysh_add_beizhixing_source')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        all_id = self.select_data(['id'], 'gulaijing', 'court_execute_id', cond='limit 10')
        # all_id = self.select_data(['id'], 'gulaijing', 'court_execute_id')
        for i in all_id:
            beizhixing_id = i[0]
            self.send_mqdata(str(beizhixing_id))
    
    def parse_only(self, body):
        beizhixing_id = body
        md5_demo = self.select_data(['md5'], 'el_rizhi', 'rizhi_court_beizhixing', where="""id ={beizhixing_id}""".format(beizhixing_id=beizhixing_id))
        if len(md5_demo) != 0:
            md5_demo_demo = md5_demo[0]
            if md5_demo_demo:
                md5 = md5_demo_demo[0]
                source_demo = self.select_data(['source'], 'adjudicative', 'beizhixing', where="""md5 ='{md5}'""".format(md5=md5))
                if len(source_demo) != 0:
                    source_demo_demo = source_demo[0]
                    if source_demo_demo:
                        source = source_demo_demo[0]
                        self.update_data({'source': source}, 'gulaijing', 'court_execute_id', where="""id={beizhixing_id}""".format(beizhixing_id=beizhixing_id))


if __name__ == '__main__':
    start_run = add_beizhixing_source()
    start_run.run('add_beizhixing_source')