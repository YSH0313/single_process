# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2023-02-23- 17:11:18
# @Version: 1.0.0
# @Description: 重试装饰器
import time
from functools import wraps
from random import randint
from decorator import decorator


# @decorator
# def loopgenerator(fun_name, *arg, **kwar):
#     def loop(*args, **kwargs):
#         gen_len = len(list(fun_name()))
#         while gen_len:
#             for i in fun_name():
#
#
#     return loop(*arg, **kwar)

class RetryingError(Exception):
    def __init__(self, message):
        self.message = message


def count_time(func):
    def clocked(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        total_time = end - start
        print(f'{func.__name__}方法运行完成，共计{total_time}秒')
        return result

    return clocked


def retrying(**kwar):  # 重试装饰器
    stop_max_attempt_number = 3
    if 'stop_max_attempt_number' in kwar.keys():
        stop_max_attempt_number = kwar.get('stop_max_attempt_number')

    def retr(func):
        def retry(*args, **kwargs):
            num = 0
            while num < stop_max_attempt_number:
                try:
                    try:
                        return func(*args, **kwargs)
                    except:
                        if 'befor_fun' in kwar.keys():
                            befor_fun_name = kwar.get('befor_fun')
                            befor_fun_parm = kwar.get('befor_parmas')
                            if befor_fun_parm:
                                if isinstance(befor_fun_name, str):
                                    args[0].__getattribute__(befor_fun_name)(befor_fun_parm)
                                elif not isinstance(befor_fun_name, str):
                                    args[0].__getattribute__(befor_fun_name.__name__)(befor_fun_parm)
                            elif not befor_fun_parm:
                                if callable(befor_fun_name):
                                    args[0].__getattribute__(befor_fun_name.__name__)()
                                elif isinstance(befor_fun_name, str):
                                    args[0].__getattribute__(befor_fun_name)()
                        return func(*args, **kwargs)
                except:
                    num += 1
                    if num == stop_max_attempt_number:
                        import traceback
                        traceback.print_exc()
            else:
                raise RetryingError(f'重试次数超过{stop_max_attempt_number}次！')

        return retry

    return retr


if __name__ == '__main__':

    class ceshi(object):

        def get_conn(self):
            return 'conn'

        def befor_fun(self, a):
            print(f'{a}, 111')

        def after_fun(self, b):
            print(f'{b}, 222')

        @retrying(stop_max_attempt_number=5, befor_fun='befor_fun', befor_parmas='get_conn')
        def get_random(self):
            int_r = randint(0, 100)
            if int_r > 0:
                print(f"该随机数等于{int_r}")
                raise IOError("该随机数大于0")
            else:
                return int_r


    ce = ceshi()
    # print(f"111,  {ce.get_random(befor_fun=ce.befor_fun, befor_parmas=ce.get_conn)}")
    print(f"111,  {ce.get_random()}")

    # # @loopgenerator
    # def gen_ceshi():
    #     for i in range(100):
    #         yield i
    #
    #
    # gen_len = len(list(gen_ceshi()))
    # while gen_len:
    #     for i in gen_ceshi():
    #         print('11111', i)
    #         gen_len -= 1
    #     time.sleep(1)
