# import queue
# import time
# import ctypes
# import inspect
# import threading
# import logging
# from MQ.mq import Mq
# from config.Cluster import Cluster
#
# def _async_raise(tid, exctype):
#
#     """raises the exception, performs cleanup if needed"""
#
#     tid = ctypes.c_long(tid)
#     if not inspect.isclass(exctype):
#         exctype = type(exctype)
#
#     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#
#     if res == 0:
#         raise ValueError("invalid thread id")
#
#     elif res != 1:
#         # """if it returns a number greater than one, you're in trouble,
#         # and you should call it again with exc=NULL to revert the effect"""
#         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#         raise SystemError("PyThreadState_SetAsyncExc failed")
#
# def stop_thread(thread):
#     # print(thread.ident)
#     _async_raise(thread.ident, SystemExit)
#
#
#
# exitFlag = 0
# queueLock = threading.Lock()
# workQueue = queue.Queue(10)
# threads = []
# threadID = 1
#
# class myThread(threading.Thread):
#     def __init__(self, threadID, name, q, queue_name, fun_name):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.q = q
#         self.queue_name = queue_name
#         self.fun_name = fun_name
#
#     def run(self):
#         # print("开启线程：" + self.name)
#         process_data(self.name, self.q, queue_name=self.queue_name, fun_name=self.fun_name)
#         # print("退出线程：" + self.name)
#
# def process_data(threadName, q, queue_name, fun_name):
#     while not exitFlag:
#         queueLock.acquire()
#         if not workQueue.empty():
#             data = q.get()
#             queueLock.release()
#             # print("%s processing %s" % (threadName, data))
#             mq = Mq(queue_name)
#             start_reuests = fun_name()
#             for i in start_reuests:
#                 mq.send_mqdata(i, is_thread=True)
#         else:
#             queueLock.release()
#         time.sleep(1)
#
# def start_th(fun_lists, queue_name, signal=None):
#     threadList = ["Thread-1"]
#     nameList = ["One"]
#     def s():
#         global threadID
#         global exitFlag
#         # 创建新线程
#         for tName in threadList:
#             thread = myThread(threadID, tName, workQueue, queue_name, fun_lists[threadList.index(tName)])
#             thread.start()
#             threads.append(thread)
#             threadID += 1
#
#         # 填充队列
#         queueLock.acquire()
#         for word in nameList:
#             workQueue.put(word)
#         queueLock.release()
#
#         # 等待队列清空
#         while not workQueue.empty():
#             pass
#
#         # 通知线程是时候退出
#         exitFlag = 1
#
#         # 等待所有线程完成
#         for t in threads:
#             t.join()
#         print("退出主线程")
#     total = Mq(queue_name).send_channel_count.method.message_count
#     Breakpoint = None
#     if signal != None:
#         Breakpoint = signal
#         # print('剩余消息总量：', total, '是否断点：', Breakpoint)
#     if signal == None:
#         from config.settings import Breakpoint
#         Breakpoint = Breakpoint
#         # print('剩余消息总量：', total, '是否断点：', Breakpoint)
#     logger = logging.getLogger(__name__)
#     logger.info('剩余消息总量：'+str(total)+',是否断点：'+str(Breakpoint))
#     if len(fun_lists) == 0:
#         raise ('请先生产消息')
#     if (int(total) == 0) and (Breakpoint == True):
#         s()
#     if (int(total) > 0) and (Breakpoint == True):
#         return
#     if (int(total) == 0) and (Breakpoint == False):
#         s()
#     if (int(total) > 0) and (Breakpoint == False):
#         s()
#     print(Mq(queue_name).send_channel_count.method.message_count)
#
#
# def other_thead(fun_lists=None, queue_name=None, signal=None, other_param=None, **kwargs):
#     # print('创建线程成功')
#
#     logger = logging.getLogger(__name__)
#     if fun_lists[0].__name__ == 'shutdown_spider':
#         fun_lists[0](other_param)
#     elif fun_lists[0].__name__ == 'consumer':
#         fun_lists[0](queue_name)
#         logger.info('Consumer thread open ')
#     else:
#         mq = Mq(queue_name)
#         Breakpoint = None
#         if signal != None:
#             Breakpoint = signal
#         if signal == None:
#             from config.settings import Breakpoint
#             Breakpoint = Breakpoint
#         if len(fun_lists) == 0:
#             raise ('请先生产消息')
#         total = mq.send_channel_count.method.message_count
#         logger.info('剩余消息总量：' + str(total) + ',是否断点：' + str(Breakpoint))
#         for funname in fun_lists:
#             if (int(total) == 0) and (Breakpoint == True):
#                 # funname()
#                 start_reuqests = funname()
#                 if start_reuqests:
#                     for i in start_reuqests:
#                         mq.send_mqdata(i, is_thread=True)
#             elif (int(total) > 0) and (Breakpoint == True):
#                 return
#             elif (int(total) == 0) and (Breakpoint == False):
#                 # funname()
#                 start_reuqests = funname()
#                 if start_reuqests:
#                     for i in start_reuqests:
#                         mq.send_mqdata(i, is_thread=True)
#             elif (int(total) > 0) and (Breakpoint == False):
#                 funname()
#                 start_reuqests = funname()
#                 if start_reuqests:
#                     for i in start_reuqests:
#                         mq.send_mqdata(i, is_thread=True)
#         # # print("生产完成")
#         # # print(Mq(queue_name).send_channel_count.method.message_count)
#
# def thread_redis(fun_lists=None, signal=None, other_param=None, key=None):# print('创建线程成功')
#     if fun_lists[0].__name__ == 'shutdown_spider':
#         fun_lists[0](other_param)
#     elif fun_lists[0].__name__ == 'consumer':
#         fun_lists[0](key)
#     else:
#         cl = Cluster()
#         total, key_len = cl.get_len(key[0])
#         Breakpoint = None
#         if signal != None:
#             Breakpoint = signal
#         if signal == None:
#             from config.settings import Breakpoint
#             Breakpoint = Breakpoint
#         if len(fun_lists) == 0:
#             raise ('请先生产消息')
#         logger = logging.getLogger(__name__)
#         logger.info('剩余消息总量：' + str(total) + ',是否断点：' + str(Breakpoint))
#         for funname in fun_lists:
#             if (int(total) == 0) and (Breakpoint == True):
#                 # funname()
#                 start_reuqests = funname()
#                 if start_reuqests:
#                     for i in start_reuqests:
#                         cl.push_task(key=key[0], tasks=i, level=i.__dict__['level'])
#             elif (int(total) > 0) and (Breakpoint == True):
#                 return
#             elif (int(total) == 0) and (Breakpoint == False):
#                 # funname()
#                 start_reuqests = funname()
#                 if start_reuqests:
#                     for i in start_reuqests:
#                         cl.push_task(key=key[0], tasks=i, level=i.__dict__['level'])
#             elif (int(total) > 0) and (Breakpoint == False):
#                 # funname()
#                 start_reuqests = funname()
#                 if start_reuqests:
#                     for i in start_reuqests:
#                         cl.push_task(key=key[0], tasks=i, level=i.__dict__['level'])
#         # print("生产完成")
#         # print(Mq(queue_name).send_channel_count.method.message_count)
#
# def main_thead(fun_lists=None, queue_name=None, signal=None, other_param=None, key=None, **kwargs):
#     # print('创建线程成功')
#     # 创建线程
#     poll = []  # 线程池
#     thead_one = None
#     if queue_name:
#         thead_one = threading.Thread(target=other_thead, args=(fun_lists, queue_name, signal, other_param, ), kwargs=kwargs)
#     elif key:
#         thead_one = threading.Thread(target=thread_redis, args=(fun_lists, signal, other_param, key, ))
#     poll.append(thead_one)  # 线程池添加线程
#     for n in poll:
#         n.start()  # 准备就绪,等待cpu执行
#     return thead_one
#
