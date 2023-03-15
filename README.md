##初次拉代码，部署本地环境：
- 1、git clone https://gitlab.bailian-ai.com/yuanshaohang/single_process.git
- 2、git checkout dev_new
- 3、single_process/config/settings.py中的log_path改为自己电脑路径；kafka_servers端口用59092
##服务器Python环境
- 用户：bailian
- 项目路径： /home/bailian/single_process
- Python环境名称：py-bailian
- 进入Python环境命令：source /home/bailian/py-bailian/bin/activate
- 启动全量抓取：nohup python -u py文件绝对路径 >> /dev/null 2>&1 &
- log地址：/home/bailian/log_file
##线上更新环境
- 新增爬虫自动注册到检测表内，根据随机数字来进行更新数据
