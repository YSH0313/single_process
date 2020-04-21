# -*- coding: utf-8 -*-

# 并发数
PREFETCH_COUNT = 60

# 最大优先级数
X_MAX_PRIORITY = 10

# 是否开启断点
Breakpoint = True

# 超时时间设置
TIME_OUT = 40

# 最大重试次数
max_request = 4

IS_PROXY = True  # 是否开启代理
IS_SAMEIP = True  # 是否开启同一ip会话

# 连接redis数据库
REDIS_HOST_LISTS = [{'127.0.0.1': '6379'}] #主机名
# REDIS_PARAMS = {"password": 'password'} # 单机情况下,密码没有的不设置
redis_connection = True  # 是否开启redis连接


# 连接mysql
Mysql = {
    "MYSQL_HOST": '117.50.3.204',
    # "MYSQL_HOST": '10.9.81.15',
    "MYSQL_DBNAME": "adjudicative",
    # "MYSQL_DBNAME": "el_rizhi",
    "MYSQL_USER": "lym",
    "MYSQL_PASSWORD": "Elements123",
    "PORT": 3306,
}
# Mysql = {
#     'MYSQL_HOST': "127.0.0.1",
#     'MYSQL_DBNAME': "adjudicative",
#     'MYSQL_USER': "root",
#     'MYSQL_PASSWORD': "root",
#     'PORT': 3306
# }

OTHER_Mysql = {
    "MYSQL_HOST": '10.9.189.128',
    "MYSQL_DBNAME": "el_rizhi",
    "MYSQL_USER": "lym",
    "MYSQL_PASSWORD": "Ku7a37Pa",
    "PORT": 3306,
}
IS_INSERT = True  # 是否开启mysql连接
OTHER_DB = False  # 是否开启第二个数据库连接

# 连接rabbitmq
# Rabbitmq = {
#     'user': "wander",
#     'password': "Elements123",
#     'host': '10.9.21.213'
# }
Rabbitmq = {
    'user': "wander",
    'password': "Elements123",
    'host': '117.50.7.101'
}
# Rabbitmq = {
#     'user': "guest",
#     'password': "guest",
#     'host': '127.0.0.1'
# }
IS_connection = True  # 是否开启Rabbitmq连接
Waiting_time = 30  # 允许队列最大空置时间