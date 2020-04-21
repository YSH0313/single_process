import os
import time
from MQ.mq import Mq
from config.settings import Waiting_time


class QueueMonitoring(Mq):
    def __init__(self, queur_name, process_name):
        Mq.__init__(self, queur_name)
        self.process_name = process_name
        self.self_pid = os.getpid()

    def delete_queue(self):
        time.sleep(60)
        reidual_num = self.send_channel_count.method.message_count
        while reidual_num > 0:
            time.sleep(60)
            reidual_num = self.send_channel_count.method.message_count
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '队列', self.queue_name, '未消费完毕')
        if reidual_num == 0:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '队列', self.queue_name, '目前为空，开始监控……')
            time.sleep(Waiting_time)
            reidual_num = self.send_channel_count.method.message_count
            if reidual_num == 0:
                self.process_name.kill()
                # self.channel.queue_delete(queue=self.queue_name)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '队列', self.queue_name, '持续5分钟消息数量未0', '已删除队列')
        print('*******************队列{queue_name}监控完毕*******************'.format(queue_name=self.queue_name))
        print('==========================================================')
        # cmd = 'taskkill -F /pid {pid}'.format(pid=self.self_pid)
        # print(cmd)
        # os.system(cmd)
        return

if __name__ == '__main__':
    queue = QueueMonitoring('ysh_tests', 'send_channel')
    # queue.delete_queue()
    queue.channel.queue_delete(queue='ysh_tests_2')