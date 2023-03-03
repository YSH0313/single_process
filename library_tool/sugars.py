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



@decorator
def retrying(fun_name, stop_max_attempt_number=3, *ar, **kwar):  # 重试装饰器
    def retr(*args, **kwargs):
        num = 0
        while num < stop_max_attempt_number:
            try:
                try:
                    return fun_name(*args, **kwargs)
                except:
                    if 'befor_fun' in kwargs.keys():
                        befor_fun_name = kwargs.get('befor_fun')
                        befor_fun_parm = kwargs.get('befor_parmas')
                        if isinstance(befor_fun_parm, str):
                            args[0].__getattribute__(befor_fun_name)(befor_fun_parm)
                        elif isinstance(befor_fun_parm, object):
                            befor_fun_name = kwargs.get('befor_fun').__name__
                            befor_fun_parm = kwargs.get('befor_parmas').__name__
                            args[0].__getattribute__(befor_fun_name)(args[0].__getattribute__(befor_fun_parm)())

                    return fun_name(*args, **kwargs)
            except:
                num += 1
                if num == stop_max_attempt_number:
                    import traceback
                    traceback.print_exc()
        else:
            print(f'重试次数超过{stop_max_attempt_number}次！')

    if 'after_fun' in kwar.keys():
        after_fun_name = kwar.get('after_fun')
        after_fun_parm = kwar.get('after_parmas')
        if isinstance(after_fun_parm, str):
            ar[0].__getattribute__(after_fun_name)(after_fun_parm)
        elif isinstance(after_fun_parm, object):
            after_fun_name = kwar.get('befor_fun').__name__
            after_fun_parm = kwar.get('befor_parmas').__name__
            ar[0].__getattribute__(after_fun_name)(ar[0].__getattribute__(after_fun_parm)())

    return retr(*ar, **kwar)


if __name__ == '__main__':

    # class ceshi(object):
    #
    #     def get_conn(self):
    #         return 'conn'
    #
    #     def befor_fun(self, a):
    #         print(f'{a}, 111')
    #
    #     def after_fun(self, b):
    #         print(f'{b}, 222')
    #
    #     @retrying(stop_max_attempt_number=5)
    #     def get_random(self, **kwargs):
    #         int_r = randint(0, 100)
    #         if int_r > 0:
    #             print(f"该随机数等于{int_r}")
    #             raise IOError("该随机数大于0")
    #         else:
    #             return int_r
    #
    #
    # ce = ceshi()
    # # print(f"111,  {ce.get_random(befor_fun=ce.befor_fun, befor_parmas=ce.get_conn)}")
    # print(f"111,  {ce.get_random(befor_fun='befor_fun', befor_parmas='get_conn')}")

    # @loopgenerator
    def gen_ceshi():
        for i in range(100):
            yield i


    gen_len = len(list(gen_ceshi()))
    while gen_len:
        for i in gen_ceshi():
            print('11111', i)
            gen_len -= 1
        time.sleep(1)