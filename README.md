##初次拉代码，部署本地环境：
- 1、git clone git@github.com:YSH0313/single_process.git
- 2、single_process/config/settings.py中的log_path改为自己电脑路径；kafka_servers端口用59092
##必要的环境
- python3.7及以上版本
- rabbitmq
- mysql
##线上更新环境
- 新增爬虫自动注册到检测表内，根据随机数字来进行更新数据
