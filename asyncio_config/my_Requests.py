

class MyRequests(object):
    def __init__(self, types='GET', url=None, headers=None, data=None, cookies=None, timeout=15, callback=None, meta=None, proxy=None, level=0):
        self.types = types
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout
        self.callback = callback
        self.meta = meta
        self.proxy = proxy
        self.level = level

class MyFormRequests(object):
    def __init__(self, types='POST', url=None, headers=None, data=None, cookies=None, timeout=15, callback=None, meta=None, proxy=None, level=0):
        self.types = types
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout
        self.callback = callback
        self.meta = meta
        self.proxy = proxy
        self.level = level

class MyResponse(object):
    def __init__(self, url=None, headers=None, data=None, cookies=None, meta=None, text=None, content=None, status_code=None, request_info=None, proxy=None):
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.meta = meta
        self.text = text
        self.content = content
        self.status_code = status_code
        self.request_info = request_info
        self.proxy = proxy

if __name__ == '__main__':
    request = MyResponse(url='https://www.baidu.com/', headers='11111', data={'qq':11}, cookies='1231312', meta={'dasda':'111'}, text='qwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', content=b'asdadasddddddddddddddddddddddddddddddddddddddddd')
    print(request.url)