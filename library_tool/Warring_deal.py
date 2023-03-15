import os
import time
import pymysql
from email_sender.msgutils import send_mail

Mysql = {
    'MYSQL_HOST': 'aliyun-rds-qdb.bl-ai.com',
    'MYSQL_DBNAME': 'spider_frame',
    'MYSQL_USER': 'yuanshaohang',
    'MYSQL_PASSWORD': 'yhHoRatHtG8',
    'PORT': 3306
}


class Warring_deal(object):
    def __init__(self):
        self.db = pymysql.connect(host=Mysql['MYSQL_HOST'], user=Mysql['MYSQL_USER'], password=Mysql['MYSQL_PASSWORD'],
                                  port=Mysql['PORT'], db=Mysql['MYSQL_DBNAME'], charset='utf8', use_unicode=True)
        self.cursor = self.db.cursor()

    def now_time(self, is_date=False):  # 获取现在时间
        if is_date == False:
            now_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return now_time
        now_time = str(time.strftime("%Y-%m-%d", time.localtime()))
        return now_time

    def Find1(self, target, array):
        # 不存在数组则直接返回
        if not array:
            return False
        # 二维数组的行
        row = len(array)
        # 二维数组的列
        col = len(array[0])
        # 二层循环遍历二维数组
        for i in range(row):
            for j in range(col):
                # 如果目标值等于数组中的值，则找到
                if target == array[i][j]:
                    return True
        # 数组遍历结束后仍未找到
        return False

    def list2table(self, list_data):
        if list_data:
            row_data = ''
            for k, v in enumerate(list_data):
                row_data += f"""<tr>
                                    <td>{k+1}</td>
                                    <td>{v[0]}</td>
                                    <td>{v[1]}</td>
                                    <td>{v[2]}</td>
                                </tr>"""
            table = f'''<table border="1px" style="border-collapse: collapse; align-content: center; text-align: center">
                            <thead>
                                <tr>
                                    <th>序号</th>
                                    <th style="width: 250px">爬虫名称</th>
                                    <th style="width: 200px">结束时间</th>
                                    <th style="width: 700px">异常信息</th>
                                </tr>
                            </thead>{row_data}
                        </table>'''
            return table
        else:
            return '没有数据'

    def warring_deal(self):
        sql = f"""select spider_name, end_time, baifenbi from Warring_deal where add_time = '{self.now_time(is_date=True)}'"""
        self.cursor.execute(sql)
        self.db.commit()
        data = self.cursor.fetchall()
        if len(data) == 0:
            return
        elif len(data) > 0:
            message_list_yuan = {'to_addr': "yuanshaohang@bailian.ai", 'messages': []}
            message_list_liu = {'to_addr': "liuqingchuan@bailian.ai", 'messages': []}
            for i in data:
                spider_name = i[0]
                end_time = i[1]
                baifenbi = i[2]
                owner_sql = f"""select owner from spiderlist_monitor where spider_name='{spider_name}'"""
                self.cursor.execute(owner_sql)
                self.db.commit()
                owner = self.cursor.fetchone()[0]
                exec_info = f'数据异常，错误数据占比：{baifenbi}'
                if baifenbi == '0':
                    exec_info = f'程序异常，报错信息超过100次'
                message = [spider_name, end_time, exec_info]
                if owner == '袁少航' and not self.Find1(spider_name, message_list_yuan['messages']):
                    message_list_yuan['messages'].append(message)
                elif owner != '袁少航' and not self.Find1(spider_name, message_list_liu['messages']):
                    message_list_liu['messages'].append(message)
            print(self.list2table(message_list_yuan.get('messages')))
            print('========================================================')
            print(self.list2table(message_list_liu.get('messages')))
            if message_list_yuan.get('messages'):
                send_mail(title='爬虫异常报警', message=self.list2table(message_list_yuan['messages']), to_addr=message_list_yuan['to_addr'])
            if message_list_liu.get('messages'):
                send_mail(title='爬虫异常报警', message=self.list2table(message_list_liu['messages']), to_addr=message_list_liu['to_addr'])


if __name__ == '__main__':
    Warring_deal = Warring_deal()
    Warring_deal.warring_deal()
