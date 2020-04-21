# -*- coding: utf-8 -*-
from config.all_config import *


class beizhixing_null_pname(Manager):
    name = 'beizhixing_null_pname'

    def __init__(self):
        Manager.__init__(self, 'ysh_beizhixing_null_pname')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        all_data = self.select_data(['id', 'url'], db_name='el_rizhi', table='rizhi_court_beizhixing', )
    
    def parse_only(self, body):
        print(body)


if __name__ == '__main__':
    start_run = beizhixing_null_pname()
    start_run.run('beizhixing_null_pname')