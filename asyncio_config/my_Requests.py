import re
import sys


class MyRequests(object):
    def __init__(self, url, method='GET', headers=None, params=None, data=None, json_params=None, cookies=None,
                 timeout=30, callback=None, proxy=None, level=0, verify_ssl=None, allow_redirects=True, is_file=False,
                 retry_count=0, is_change=False, is_encode=None, ignore_ip=False, is_websource=False, page_click=None,
                 before_do=None, input_box=None, input_text=None, input_click=None, dont_filter=False, encoding=None, **meta):
        self.method = method  # 请求类型
        self.url = url  # 目标url
        self.params = params  # 使用get方式进行post请求时的参数
        self.data = data  # 使用get方式进行post请求时的参数
        self.json_params = json_params  # 使用get方式进行post请求时的参数
        self.headers = headers  # header头
        self.cookies = cookies  # 需要添加的cookie
        self.timeout = 120 if is_file and timeout == 30 else timeout  # 超时时间
        self.callback = callback  # 回调目标函数
        self.meta = {} if not meta.get('meta') else meta.get('meta')  # 需要传递的参数（字典格式）
        self.proxy = proxy  # 需要添加的代理ip
        self.level = level  # 请求优先级
        self.verify_ssl = False if ('https' in url) and (not verify_ssl) else verify_ssl  # 是否禁用网站证书
        self.allow_redirects = allow_redirects  # 是否允许重定向
        self.is_file = is_file  # 是否是文件地址
        self.retry_count = retry_count
        self.is_change = is_change
        self.is_encode = is_encode
        self.ignore_ip = ignore_ip
        self.is_websource = is_websource  # 页面中出现匹配的内容或元素时结束渲染（推荐使用xpath）
        self.page_click = page_click  # 翻页需要点击的按钮位置（xpath路径）
        self.before_do = before_do  # 翻页前需要做的点击操作（xpath路径）
        self.input_box = input_box
        self.input_text = input_text
        self.input_click = input_click
        self.dont_filter = dont_filter  # 是否对当前url进行去重访问
        self.encoding = encoding  # 编码格式


class MyFormRequests(object):
    def __init__(self, url, method='POST', headers=None, params=None, data=None, json_params=None, cookies=None,
                 timeout=30, callback=None, proxy=None, level=0, verify_ssl=None, allow_redirects=True, is_file=False,
                 retry_count=0, is_change=False, is_encode=None, ignore_ip=False, dont_filter=False, encoding=None, **meta):
        self.method = method  # 请求类型
        self.url = url  # 目标url
        self.params = params  # 目标url
        self.data = data  # 进行post请求时的参数
        self.json_params = json_params  # 进行post请求时json的参数
        self.headers = headers  # header头
        self.cookies = cookies  # 需要添加的cookie
        self.timeout = 120 if is_file and timeout == 30 else timeout  # 超时时间
        self.callback = callback  # 回调目标函数
        self.meta = {} if not meta.get('meta') else meta.get('meta')  # 需要传递的参数（字典格式）
        self.proxy = proxy  # 需要添加的代理ip
        self.level = level  # 请求优先级
        self.verify_ssl = False if ('https' in url) and (not verify_ssl) else verify_ssl  # 是否禁用网站证书
        self.allow_redirects = allow_redirects  # 是否允许重定向
        self.is_file = is_file  # 是否是文件地址
        self.retry_count = retry_count
        self.is_change = is_change
        self.is_encode = is_encode
        self.ignore_ip = ignore_ip
        self.dont_filter = dont_filter  # 是否对当前url进行去重访问
        self.encoding = encoding  # 编码格式


class MyResponse(object):
    def __init__(self, log_info: dict = None, url=None, headers=None, content_type=None, data=None, cookies=None,
                 text=None, content=None, status_code=None, xpath=None, request_info=None, proxy=None, level=0, retry_count=0,
                 **meta):
        self.url = url  # 返回请求的的url
        self.data = data  # 返回请求用的data参数信息
        self.headers = headers  # 返回请求的header信息
        self.content_type = content_type  # 返回请求的header信息
        # self.cookies = Cookies(cookies)  # 返回请求的cookies信息
        self.cookies = cookies  # 返回请求的cookies信息
        self.meta = {} if not meta.get('meta') else meta.get('meta')  # 返回请求带过来的参数和值
        self.text = text  # 返回网站的响应体，包括html和json以及其他的任何数据
        self.content = content  # 返回的字节流
        self.status_code = status_code  # 返回响应状态吗
        self.xpath = xpath  # xpath对象
        self.request_info = request_info  # 返回请求体
        self.proxy = proxy  # 返回请求使用的代理
        self.level = level  # 请求优先级
        self.retry_count = retry_count  # 返回请求使用的代理
        self.log_info = {} if not log_info else log_info


class Cookies(object):
    def __init__(self, cookies):
        self.cookies = cookies

    def use_cookie(self):
        cookie_demo = re.compile('Set-Cookie: (.*?);', re.S)
        cookies = '; '.join(cookie_demo.findall(str(self.cookies)))
        return cookies

    def ret_cookies(self):
        return self.cookies


if __name__ == '__main__':
    # request = MyRequests(url='https://www.baidu.com/', headers='11111', meta={'dasda':'111'})
    request = MyResponse(url='https://www.baidu.com/', headers='11111', data={'qq': 11}, cookies='1231312',
                         meta={'dasda': '111'}, text='qwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
                         content=b'asdadasddddddddddddddddddddddddddddddddddddddddd',
                         log_info={'req_id': 20220526170500123, 'params': 'params', 'data': 'data',
                                   'json_params': 'json_params'})
    print(request.log_info)
