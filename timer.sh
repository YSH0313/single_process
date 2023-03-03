#!/bin/bash
cd /home/yuanshaohang/py-yuan/
source /home/yuanshaohang/py-yuan/bin/activate
#python /home/yuanshaohang/single_process/spider/bailian_work/zhaoxun_chengdu.py 50 &
nohup python -u /home/yuanshaohang/single_process/spider/bailian_work/zhaoxun_chengdu_gc.py 50 >> /home/yuanshaohang/log_file/first_spider.log 2>&1 &