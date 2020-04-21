import queue
import time
import json
import sys
import requests
import threading
from MQ.mq import Mq

exitFlag = 0
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

class myThread(threading.Thread):
    def __init__(self, threadID, name, q, fun_name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.fun_name = fun_name

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q, fun_name=self.fun_name)
        print("退出线程：" + self.name)

def process_data(threadName, q, fun_name):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s" % (threadName, data))
            fun_name()
        else:
            queueLock.release()
        time.sleep(1)

def start_th(fun_lists, queue_name, signal=None):
    threadList = ["Thread-1"]
    nameList = ["One"]
    def s():
        global threadID
        global exitFlag
        # 创建新线程
        for tName in threadList:
            thread = myThread(threadID, tName, workQueue, fun_lists[threadList.index(tName)])
            thread.start()
            threads.append(thread)
            threadID += 1

        # 填充队列
        queueLock.acquire()
        for word in nameList:
            workQueue.put(word)
        queueLock.release()

        # 等待队列清空
        while not workQueue.empty():
            pass

        # 通知线程是时候退出
        exitFlag = 1

        # 等待所有线程完成
        for t in threads:
            t.join()
        print("退出主线程")
    total = Mq(queue_name).send_channel_count.method.message_count
    Breakpoint = None
    if signal != None:
        Breakpoint = signal
        print('剩余消息总量：', total, '是否断点：', Breakpoint)
    if signal == None:
        from config.settings import Breakpoint
        Breakpoint = Breakpoint
        print('剩余消息总量：', total, '是否断点：', Breakpoint)
    if len(fun_lists) == 0:
        raise ('请先生产消息')
    if (int(total) == 0) and (Breakpoint == True):
        s()
    if (int(total) > 0) and (Breakpoint == True):
        return
    if (int(total) == 0) and (Breakpoint == False):
        s()
    if (int(total) > 0) and (Breakpoint == False):
        s()
