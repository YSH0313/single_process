# 项目简介
single_process是一款可以帮助你快速开发一个网络爬虫应用的一套异步并发框架，他提供了许多内置方法，
让你的开发代码更加的简洁，爬虫代码更加规范，方便维护，除此以外还可以多线程并发的做一些数据处理的工作，
更多功能可以添加开发者的微信（YSH026-）进行沟通。

## 开始使用

### 前置条件
    - python3.7及以上版本
    - rabbitmq或者redis队列
    - 执行my_sh目录下的spiderlist_monitor.sql文件，用来生成爬虫注册表
### 安装说明
    - git clone https://github.com/YSH0313/single_process.git
    - 将settings.py中的各项配置改为自己配置信息

### 测试运行
- 执行spider文件夹下的first_spider.py，如果正常运行并打印出了相应的信息，说明部署成功

### 创建爬虫
- 1、打开Production_spider.py文件，根据里面的提示填写信息，完成后运行即可创建
#### 示例：
- `production("my_first", True, 5, "用户", "第一个爬虫", "your_spider/my_first/")`
- 2、找到对应的爬虫文件进行相应的代码书写

### item配置
- 在items.py文件中配置自己爬虫所需要的字段
- 要符合类似于下面这样的结构，且必须继承SingleItem父类
- ```
  class BiddingItem(SingleItem):
        def __init__(self):
            sele.name = None
  ```