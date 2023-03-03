import xlrd
from config.Cluster import Cluster

class Work(Cluster):
    def __init__(self):
        Cluster.__init__(self)
        # pass

    def send_query(self):
        for i in range(1, 17327929):
            sql = """SELECT pname FROM rizhi_court_ktgg_ent WHERE id = {ids}""".format(ids=i)
            self.cursor.execute(sql)
            self.db.commit()
            all_data = self.cursor.fetchone()
            if all_data == None:
                pass
            else:
                for i in all_data:
                    if i == None:
                        continue
                    elif len(i) > 4:
                        continue
                    else:
                        self.r.sadd('pname', i)
                        print(i)

    def send_reids(self):
        workbook = xlrd.open_workbook(r'D:\work\single_process\filed\sx.xlsx')
        data_sheet = workbook.sheets()[0]
        rowNum = data_sheet.nrows  # sheet行数
        for r in range(rowNum):
            rows = data_sheet.row_values(r)
            court = rows[0].split('@')[0]
            url = rows[1].split('htm?')[0]+'htm?sxlx=5&bzxrlx=&jbfy=&bzxrmc=&zjhm='
            data = court+'~'+url
            self.r.sadd('jilin_demo', data)
            print(data)
            while (self.r.scard('jilin_demo')>0):
                data = self.r.spop('jilin_demo')
                self.r.lpush('jilin', data)
            # self.send_mqdata(data)

    def read_txt(self):
        with open(r'D:\work\single_process\filed\url_lists.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
            for i in data:
                print(i)
                self.r.sadd('url_lsist', i.replace('\n', ''))

if __name__ == '__main__':
    work = Work()
    work.read_txt()
