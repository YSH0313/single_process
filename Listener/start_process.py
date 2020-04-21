import os
import time
import datetime
import subprocess
from asyncio_config.manager import Manager
from multiprocessing import Process, Lock
from Listener.stop_work import QueueMonitoring


pool = []
def new_process(path, spider_name):
    starttime = datetime.datetime.now()
    p = Process(target=start_process, args=(path, spider_name, starttime,))  # 创建进程
    p.start()  # 启动进程
    pool.append(p)
    print('全部进程数：', len(pool))
    for i in pool:
        if i.is_alive() == False:
            pool.remove(i)
    print('存活进程数：', len(pool))

def start_process(path, spider_name, starttime):
    l = Lock()
    l.acquire()  # 锁住
    print('\033[1;31;0m', path + ' 程序开始运行\033[0m', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # os.system('python {path} &'.format(path=path))
    process_name = subprocess.Popen('python {path} &'.format(path=path))
    QueueMonitoring('ysh_' + spider_name, process_name).delete_queue()
    l.release()  # 释放
    Manager('ysh_' + spider_name).close_spider(spider_name)
    endtime = datetime.datetime.now()
    print('\033[1;31;0m{spider_name}总用时:\033[0m'.format(spider_name=spider_name), endtime - starttime, '分')
    return


if __name__ == '__main__':
    process = len(os.popen('tasklist | findstr python').readlines())
    print('本机python总进程数', process)
