import redis
import json
import time
import pymysql
from rediscluster import RedisCluster
from config.settings import REDIS_HOST_LISTS, Mysql, redis_connection, IS_INSERT, OTHER_DB, OTHER_Mysql

class Cluster(object):

    def __init__(self):
        self.startup_nodes = REDIS_HOST_LISTS
        if redis_connection != False:
            if len(REDIS_HOST_LISTS) == 1:
                for k, v in REDIS_HOST_LISTS[0].items():
                    self.r = redis.Redis(host=k, port=v, db=0, socket_timeout=None, connection_pool=None,
                                         charset='utf8', errors='strict', decode_responses=True, unix_socket_path=None)
            elif len(REDIS_HOST_LISTS) > 1:
                self.r = RedisCluster(startup_nodes=self.startup_nodes, decode_responses=True)
        if IS_INSERT != False:
            self.db = pymysql.connect(host=Mysql['MYSQL_HOST'], user=Mysql['MYSQL_USER'], password=Mysql['MYSQL_PASSWORD'], port=Mysql['PORT'], db=Mysql['MYSQL_DBNAME'], charset='utf8', use_unicode=True)
            self.cursor = self.db.cursor()
        if OTHER_DB:
            self.other_db = pymysql.connect(host=OTHER_Mysql['MYSQL_HOST'], user=OTHER_Mysql['MYSQL_USER'], password=OTHER_Mysql['MYSQL_PASSWORD'], port=OTHER_Mysql['PORT'], db=OTHER_Mysql['MYSQL_DBNAME'], charset='utf8', use_unicode=True)
            self.other_cursor = self.other_db.cursor()

    def data_deal(self, data):  # 一般数据处理
        if (data == None) or (data == ''):
            data_last = ''
            return data_last
        elif isinstance(data, dict):
            return json.loads(data)
        else:
            return str(data).replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\u3000', '').replace('\\u3000', '').replace('\t', '').replace(' ', '').replace('&nbsp;', '').replace('\\r', '')

    def prints(self, item):
        item_last = {}
        for k, v in item.items():
            if (v == None) or (v == 'None') or (v == ''):
                continue
            if (('time' not in k) or ('Time' not in k)) and (isinstance(v, dict) == False):
                item_last[k] = self.data_deal(v)
            if isinstance(v, dict):
                item_last[k] = str(v)
            if k == 'body':
                item_last[k] = """{body}""".format(body=v)
            elif ('time' in k) or ('Time' in k) or (k.endswith('T')==True):
                item_last[k] = v
        print(json.dumps(item_last, indent=2, ensure_ascii=False))
        print('===========================================================')
        return item_last

    def insert(self, item, table, db_name=None, OTHER_INSERT=False):
        item = self.prints(item)
        field_lists = []
        value_lists = []
        field_num = []
        for k, v in dict(item).items():
            if (v == None) or (v == 'None') or (v == ''):
                continue
            if ('{' and '}') in v:
                field_lists.append("`" + str(k) + "`")
                value_lists.append(str(v))
            else:
                field_lists.append("`" + str(k) + "`")
                value_lists.append(pymysql.escape_string(str(v)))
        [field_num.append('%s') for i in range(1, len(field_lists) + 1)]
        if db_name:
            sql = """INSERT IGNORE INTO `{db_name}`.`{table}` ({fields}) VALUES ({fields_num});""".format(db_name=db_name, table=table, fields=','.join(field_lists), fields_num=','.join(field_num))
        else:
            sql = """INSERT IGNORE INTO `{db_name}`.`{table}` ({fields}) VALUES ({fields_num});""".format(db_name=Mysql['MYSQL_DBNAME'], table=table, fields=','.join(field_lists), fields_num=','.join(field_num))
        if OTHER_INSERT:
            self.other_cursor.execute(sql, tuple(value_lists))
            self.other_db.commit()
        else:
            self.cursor.execute(sql, tuple(value_lists))
            self.db.commit()

    def select_data(self, field_lists, db_name, table, condition=None, where=0, num_id=0, min_id=0, max_id=0, cond=None, OTHER_INSERT=False):
        field_lists_last = []
        for i in field_lists:
            field_lists_last.append("`" + str(i) + "`")
        sq1_all = ''
        if (num_id == 0) and (where==0):
            sq1_all = """SELECT {field_lists} FROM `{db}`.`{table}`;""".format(db=db_name, field_lists=','.join(field_lists_last), table=table)
        if cond != None:
            sq1_all = """SELECT {field_lists} FROM `{db}`.`{table}` {cond};""".format(db=db_name, field_lists=','.join(field_lists_last), table=table, cond=cond)
        if (num_id == 0) and (where!=0):
            sq1_all = """SELECT {field_lists} FROM `{db}`.`{table}` WHERE {where};""".format(db=db_name, field_lists=','.join(field_lists_last), table=table, where=where)
        if num_id != 0:
            sq1_all = """SELECT {field_lists} FROM `{db}`.`{table}` WHERE `wid` = {id};""".format(db=db_name, field_lists=','.join(field_lists_last), table=table, id=num_id)
        if (min_id == 0) and (max_id ==0):
            pass
        if (max_id !=0):
            sq1_all = """SELECT {field_lists} FROM `{db}`.`{table}` WHERE (`id` >= {min}) AND (`id` <= {max});""".format(db=db_name, field_lists=','.join(field_lists_last), table=table, min=min_id, max=max_id)
        if condition:
            sq1_all = """SELECT {condition} {field_lists} FROM `{db}`.`{table}`;""".format(condition=condition, field_lists=','.join(field_lists_last), db=db_name, table=table)
        if condition and cond:
            sq1_all = """SELECT {condition} {field_lists} FROM `{db}`.`{table}` {cond};""".format(condition=condition, field_lists=','.join(field_lists_last), db=db_name, table=table, cond=cond)
        print('\033[1;31;0m{tt}查询字段：\033[0m'.format(tt=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))), sq1_all)
        print('===========================================================')
        if OTHER_INSERT:
            self.other_cursor.execute(sq1_all)
            self.other_db.commit()
            data_all = self.other_cursor.fetchall()
            return data_all
        else:
            self.cursor.execute(sq1_all)
            self.db.commit()
            data_all = self.cursor.fetchall()
            return data_all
    
    def update_item(self, item):
        field_lists_last = []
        for k, v in item.items():
            if ('time' in k) or ('Time' in k) or (k.endswith('T')==True):
                data = "`" + str(k) + "`" + "='{values}'".format(values=pymysql.escape_string(str(v)))
            else:
                data = "`" + str(k) + "`"+"='{values}'".format(values=pymysql.escape_string(str(self.data_deal(v))))
            field_lists_last.append(data)
        print(json.dumps(field_lists_last, indent=2, ensure_ascii=False))
        return field_lists_last

    def update_data(self, item, db_name, table, where=0, OTHER_INSERT=False):
        print('\033[1;31;0m{tt}更新字段：\033[0m'.format(tt=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))))
        item = self.update_item(item)
        update_sql = """UPDATE `{db}`.`{table_name}` SET {field_lists} WHERE {where}""".format(db=db_name, table_name=table, field_lists=','.join(item), where=where)
        if OTHER_INSERT:
            self.other_cursor.execute(update_sql)
            self.other_db.commit()
        else:
            self.cursor.execute(update_sql)
            self.db.commit()
        print(update_sql)
        return


if __name__ == '__main__':
    cl = Cluster()
    a = cl.select_data(['wid'], 'court_cpws_ent', 1)
    print(a)