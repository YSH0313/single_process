# 项目简介
single_process是一款可以帮助你快速开发一个网络爬虫应用的一套异步并发框架，他提供了许多内置方法，
让你的开发代码更加的简洁，爬虫代码更加规范，方便维护，除此以外还可以多线程并发的做一些数据处理的工作，
更多功能可以添加开发者的微信（YSH026-）进行沟通。

## 开始使用

### 前置条件
    - python3.7及以上版本
    - rabbitmq或者redis队列，最新版本新增了基于内存的优先级队列（默认优先使用内存优先级队列）
    - 执行my_sh目录下的spiderlist_monitor.sql文件，用来生成爬虫注册表
### 安装说明
    - git clone https://github.com/YSH0313/single_process.git
    - pip install -r requirements.txt
    - 将settings.py中的各项配置改为自己配置信息

### 项目结构
    ├── Jenkinsfile  # 用于分布式一件部署项目
    ├── MQ  # Rabbitmq队列管理模块
    ├── Production_spider.py  # 创建爬虫模板脚本
    ├── README.md  # README.md
    ├── __init__.py
    ├── asyncio_config  # 核心引擎及请求类和返回体
    ├── config  # 基础继承类及爬虫模版
    ├── get_code  # 验证码训练模块
    ├── items.py  # item模块用于定义字段
    ├── js  # 常用js库
    ├── library_tool  # 工具类
    ├── middleware  # 中间件
    ├── my_sh  # 自定义shell脚本
    ├── requirements.txt  # 依赖
    ├── run.py
    ├── settings.py  # 配置文件
    └── spider  # 任务目录
        ├── __init__.py
        └── first_spider.py  # 具体爬虫文件


### 测试运行
- 执行spider文件夹下的first_spider.py，如果正常运行并打印出了相应的信息，说明部署成功

### 创建爬虫
- 1、打开Production_spider.py文件，根据里面的提示填写信息，完成后运行即可创建
#### 示例：
- `production("my_first", True, 5, "[开发者]", "第一个爬虫", "your_spider/my_first/", kernel=1)`
- production具体参数请自行进入源码部分查看，每一项参数都有相应说明，上述示例中【kernel=1】为队列模式选项，默认为3表示优先使用内存作为优先级队列
- 在spider目录下找到对应的爬虫文件进行相应的代码书写

### item配置
- 在items.py文件中配置自己爬虫所需要的字段
- 要符合类似于下面这样的结构，且必须继承SingleItem父类
- ```
  class BiddingItem(SingleItem):  # BiddingItem为item名称
        def __init__(self):
            sele.name = None  # 这里表示我们有一个name字段预占位
  ```