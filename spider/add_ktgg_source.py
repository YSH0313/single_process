# -*- coding: utf-8 -*-
from config.all_config import *


class add_ktgg_source(Manager):
    name = 'add_ktgg_source'

    def __init__(self):
        Manager.__init__(self, 'ysh_add_ktgg_source')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        # all_id = self.select_data(['id'], 'gulaijing', 'court_ktgg_kid', cond='limit 10')
        # all_id = self.select_data(['id'], 'gulaijing', 'court_ktgg_kid')
        for i in range(632630032, 632808033):
            beizhixing_id = i
            self.send_mqdata(str(beizhixing_id))

    def parse_only(self, body):
        ktgg_id = 1
        md5_demo = self.select_data(['mid'], 'el_rizhi', 'rizhi_court_ktgg', where="""kid ={ktgg_id}""".format(ktgg_id=ktgg_id))
        if len(md5_demo) != 0:
            md5_demo_demo = md5_demo[0]
            if md5_demo_demo:
                md5 = md5_demo_demo[0]
                source_demo = self.select_data(['source'], 'adjudicative', 'ktgg_kt', where="""md5 ='{md5}'""".format(md5=md5))
                if len(source_demo) != 0:
                    source_demo_demo = source_demo[0]
                    if source_demo_demo:
                        source = source_demo_demo[0]
                        self.insert({'id': ktgg_id, 'source': source}, db_name='gulaijing', table='court_ktgg_kid')


if __name__ == '__main__':
    start_run = add_ktgg_source()
    start_run.run('add_ktgg_source')