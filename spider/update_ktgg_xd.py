# -*- coding: utf-8 -*-
from config.all_config import *


class update_ktgg_xd(Manager):
    name = 'update_ktgg_xd'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_ktgg_xd')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.plaintiff = re.compile(r'原告:(.*?)被告|原告：(.*?)被告', re.S)
        self.plaintiff_1 = re.compile(r'上诉人:(.*?)被上诉人|上诉人：(.*?)被上诉人', re.S)

    def start_requests(self):
        all_id = self.select_data(['kid'], 'xd', 'xd_tmp_ktgg')
        # all_id = self.select_data(['kid'], 'xd', 'xd_tmp_ktgg', cond='order by kid limit 100')
        for i in all_id:
            ktgg_id = i[0]
            # print(ktgg_id)
            self.send_mqdata(str(ktgg_id))
    
    def parse_only(self, body):
        ktgg_id = body
        data = self.select_data(['pname', 'party'], 'el_rizhi', 'rizhi_court_ktgg', where="""kid ={ktgg_id}""".format(ktgg_id=ktgg_id))[0]
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
                    self.prints(item)
                    # self.insert(item, 'rizhi_court_ktgg_ent_copy1', db_name='el_rizhi')

        if party:
            if ('{' and '}') in party:
                party = json.loads(party)
                plaintiff_lists = self.split_str(self.data_deal(party.get('plaintiff')))
                if plaintiff_lists:
                    for i in plaintiff_lists:
                        if i:
                            item['kid'] = ktgg_id
                            item['pname'] = i
                            item['ptype'] = 'p'
                            self.prints(item)
                            # self.insert(item, 'rizhi_court_ktgg_ent_copy1', db_name='el_rizhi')
            elif '原告' in party:
                plaintiff_demo = ''.join(self.deal_re_lists(self.plaintiff.findall(self.data_deal(party))))
                print(plaintiff_demo)
                plaintiff_lists = self.split_str(self.data_deal(plaintiff_demo))
                if plaintiff_lists:
                    for i in plaintiff_lists:
                        if i:
                            item['kid'] = ktgg_id
                            item['pname'] = i
                            item['ptype'] = 'p'
                            self.prints(item)
                            # self.insert(item, 'rizhi_court_ktgg_ent_copy1', db_name='el_rizhi')
            else:
                self.r.sadd('other_data', str(ktgg_id)+'~'+party)


if __name__ == '__main__':
    start_run = update_ktgg_xd()
    start_run.run('update_ktgg_xd')