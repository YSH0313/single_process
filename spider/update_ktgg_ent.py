# -*- coding: utf-8 -*-
import sys
sys.path.append("/root/shaohang/single_process")
from config.all_config import *


class update_ktgg_ent(Manager):
    name = 'update_ktgg_ent'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_ktgg_ent')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'ktgg_ent'""")[0][0]
        all_id = self.select_data(['kid'], 'el_rizhi', 'rizhi_court_ktgg_copy1', cond="""where kid > {last_id}""".format(last_id=last_id), OTHER_INSERT=True)
        # all_id = self.select_data(['kid'], 'el_rizhi', 'rizhi_court_ktgg_copy1', cond='order by kid limit 100')
        print(all_id)
        self.update_data({'minid':max(all_id)[0]}, 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='ktgg_ent'))
        for i in all_id:
            ktgg_id = i[0]
            self.send_mqdata(str(ktgg_id))

    def parse_only(self, body):
        ktgg_id = body
        data = self.select_data(['pname', 'party'], 'el_rizhi', 'rizhi_court_ktgg_copy1', where="""kid ={ktgg_id}""".format(ktgg_id=ktgg_id), OTHER_INSERT=True)[0]
        pname = data[0]
        party = data[1].replace("'", '"').replace("；", ';').replace("，", ',').replace("None", '""')
        print(pname, party)
        item = {}
        if pname:
            pname_lists = self.split_str(pname)
            for i in pname_lists:
                if i:
                    item['kid'] = ktgg_id
                    item['pname'] = i
                    item['ptype'] = 'd'
                    # self.prints(item)
                    self.insert(item, 'rizhi_court_ktgg_ent_copy1', db_name='el_rizhi', OTHER_INSERT=True)

        if party:
            party = json.loads(party)
            plaintiff_lists = self.split_str(self.data_deal(party.get('plaintiff')))
            if plaintiff_lists:
                for i in plaintiff_lists:
                    if i:
                        item['kid'] = ktgg_id
                        item['pname'] = i
                        item['ptype'] = 'p'
                        # self.prints(item)
                        self.insert(item, 'rizhi_court_ktgg_ent_copy1', db_name='el_rizhi', OTHER_INSERT=True)


if __name__ == '__main__':
    start_run = update_ktgg_ent()
    start_run.run('update_ktgg_ent')