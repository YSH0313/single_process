# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2020-02-23 09:56:50
# @Version: 1.0.0
# @Description: 创建爬虫

from config.spider_model import production
# my_first为要创建的爬虫名称
# 是否要增量运行（True  or  False）
# 每次增量执行的页码
# 所属人名称
# 备注信息
# 要创建的爬虫路径（路径不存在时自动创建）
production('my_first', True, 5, '用户', '第一个爬虫', 'your_spider/my_first/')