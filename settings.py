# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2020-02-23 09:56:50
# @Version: 1.0.0
# @Description: setting文件

# 并发数
PREFETCH_COUNT = 50

# 最大优先级数
X_MAX_PRIORITY = 15

# 是否开启断点
Breakpoint = True

# 超时时间设置
TIME_OUT = 40

# 最大重试次数
max_request = 4
retry_http_codes = [209, 301, 302, 400, 403, 404, 405, 408, 412, 429, 500, 502, 503, 504, 505, 521]  # 允许重试的状态码

UA_PROXY = False  # 是否开启UA池代理
IS_PROXY = False  # 是否开启代理
IS_SAMEIP = False  # 是否开启同一ip会话
Agent_whitelist = ['127.0.0.1']  # 代理白名单

# 连接redis数据库
REDIS_HOST_LISTS = [{'your_host': 'your_port'}]  # 主机名
# REDIS_PARAMS = {'password': 'password'} # 单机情况下,密码没有的不设置
redis_connection = False  # 是否开启redis连接

# 连接kafka数据库
kafka_servers = {
    'server': 'your_server',  # 外网
    'topic': 'your_topic'
}
kafka_connection = False  # 是否开启kafka连接

# 连接mysql
Mysql = {
    'MYSQL_HOST': 'your_host',
    'MYSQL_DBNAME': 'your_db',
    'MYSQL_USER': 'your_user',
    'MYSQL_PASSWORD': 'your_password',
    'PORT': 'your_port'
}

OTHER_Mysql = {
    'MYSQL_HOST': 'your_host',
    'MYSQL_DBNAME': 'your_db',
    'MYSQL_USER': 'your_user',
    'MYSQL_PASSWORD': 'your_password',
    'PORT': 'your_port'
}
IS_INSERT = False  # 是否开启mysql连接
OTHER_DB = False  # 是否开启第二个数据库连接

# RabbitMQ服务器的地址及各项参数
Rabbitmq = {
    'Sgin': 'ysh',
    'username': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port',
    'max_retries': 3,  # 最大重连次数
    'async_thread_pool_size': 4,  # 异步发送线程池
}
message_ttl = 86400000
Auto_clear = True  # 重启是否自动清空队列
Asynch = True  # 是否开启异步生产
IS_connection = False  # 是否开启Rabbitmq连接
Waiting_time = 50  # 允许队列最大空置时间(秒),切记要比请求超时时间长
Delay_time = 4  # 自动关闭程序最大延迟时间

# custom_settings = {}

log_path = ''  # 日志保存路径
log_level = 'DEBUG'  # 日志级别

# 邮件发送
EMAIL_CONFIG = {
    'email_host': "smtp.163.com",  # 设置服务器
    'email_user': 'yours',  # 用户名
    'email_pass': 'yours',  # 口令
    'email_port': 25,
    'sender': 'yours',  # 发送者
    'receivers': 'yours',  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，发送多人用逗号隔开
}

access_key_id = 'yours'
access_key_secret = 'yours'
bucket_name = 'yours'
endpoint = 'yours'

ES_CONFIG = {
    "host": "your_host",
    "port": "your_port",
    "user": "your_username",
    "password": "your_password"
}  # es连接配置
IS_ES = False  # 是否开启ES连接

secret_id = 'yours'  # cos对象存储id（腾讯云控制台获得）
secret_key = 'yours'  # cos对象存储key（腾讯云控制台获得）
region = 'yours'  # COS区域
cos_bucket = 'yours'  # 对象存储桶名称

MONGO_CONFIG = {
    'MONGODB_HOST': "your_host",
    'MONGODB_PORT': "your_port",
    'MONGODB_BASE': "your_base"
}
MONGO_client = False
