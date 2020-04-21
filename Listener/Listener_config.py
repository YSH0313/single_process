import os
import time
import json
import socket
import datetime
from threading import Timer
from config.Cluster import Cluster
from Listener.start_process import new_process


class Listen(Cluster):
    def __init__(self, num):
        Cluster.__init__(self)
        self.num = num

    def start_run(self):
        sql = """SELECT spider_name, interval_time, incremental, end_time, is_run FROM single_process_listener WHERE `server_name` = '{server_name}'""".format(server_name=socket.gethostbyname(socket.gethostname()))
        self.cursor.execute(sql)
        self.db.commit()
        array = self.cursor.fetchall()
        for i in array:
            try:
                spider_name = i[0]
                interval_time = i[1]
                incremental = i[2]
                end_time = i[3]
                is_run = i[4]
                end_time = datetime.datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '%Y-%m-%d %H:%M:%S')
                if incremental == 'False':
                    continue
                elif (incremental == 'True') and (int((now-end_time).total_seconds()) >= int(interval_time)) and (is_run == 'no'):
                    only_path = os.path.join(os.getcwd(), spider_name+'.py').replace('Listener', 'spider')
                    new_process(only_path, spider_name)
            except json.JSONDecodeError:
                continue
            except ValueError:
                continue
        print('\033[1;31;0m此次监控完成', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\033[0m')
        Timer(self.num, self.start_run).start()


if __name__ == '__main__':
    listen = Listen(10)
    listen.start_run()
    # print(socket.gethostbyname(socket.gethostname()))