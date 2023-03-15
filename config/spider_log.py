# -*- coding: utf-8 -*-
import sys
import logging
from settings import log_path, log_level

"""
format参数值说明：
%(name)s：   打印Logger的名字
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序的文件名
%(funcName)s: 打印日志的当前函数
%(lineno)d:  打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d:  打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息
"""

class NoParsingFilter(logging.Filter):
  def filter(self, record):
    if record.name.startswith('asyncio_config.manager'):
      return False
    return True

logging.getLogger("root").setLevel(logging.WARNING)
class SpiderLog(object):
    name = None
    def __init__(self, custom_settings=None):
        if custom_settings:
            for varName, value in custom_settings.items():
                s = globals().get(varName)
                if s:
                    globals()[varName] = value
        self.pages = sys.argv[1] if len(sys.argv) > 1 else None
        self.path_name = self.name if not self.pages else self.name + '_add'
        # self.logger = logging.getLogger("mainModule.sub")
        self.logger = logging.getLogger(__name__)
        # self.logger.propagate = False
        # self.logger.addFilter(NoParsingFilter())
        level_map = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG,
                     'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
        if log_path:
            format_file = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                                           datefmt="%Y-%m-%d %H:%M:%S")  # 设置日志格式
            if sys.platform == 'linux':
                format_str = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")  # 设置日志格式
            else:
                format_str = logging.Formatter('\033[5;33;1m%(asctime)s\033[0m \033[5;32;1m[%(name)s]\033[0m \033[5;35;1m%(levelname)s:\033[0m \033[5;36;1m%(message)s\033[0m', datefmt="%Y-%m-%d %H:%M:%S")  # 设置日志格式
            self.logger.setLevel(level_map[log_level])  # 设置屏幕日志级别
            if self.pages:
                pass
            else:
                console = logging.StreamHandler()  # 往屏幕上输出
                console.setFormatter(format_str)  # 设置屏幕上显示的格式
                self.logger.addHandler(console)  # 把屏幕对象加到logger里

            th = logging.FileHandler(filename=log_path+'/{spider_name}.log'.format(spider_name=self.path_name), mode='w', encoding='utf-8')
            th.setFormatter(format_file)  # 设置文件里写入的格式
            self.logger.addHandler(th)  # 把对象加到logger里

        else:
            # print('没有')
            logging.basicConfig(level=level_map[log_level],
                                format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")

    def func(self):
        self.logger.info("Start print log")
        self.logger.info('这是一个测试')
        self.logger.debug("Do something")
        self.logger.warning("Something maybe fail.")
        # try:
        #     open("sklearn.txt", "rb")
        # except (SystemExit, KeyboardInterrupt):
        #     raise
        # except Exception:
        #     self.logger.error("Faild to open sklearn.txt from logger.error", exc_info=True)
        self.logger.info("Finish")


if __name__ == "__main__":
    spider_log = SpiderLog()
    spider_log.func()
