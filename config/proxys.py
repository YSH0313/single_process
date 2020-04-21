import aiohttp
import requests
import json
import random
import asyncio
import time

s = requests.session()
url = 'http://117.50.2.184:88/ippool'
# url = 'http://10.9.21.91:88/ippool'
def rand_choi_pool_response():
    try:
        response = s.get(url=url)
        return response
    except:
        return False

def rand_choi_pool():
    response = rand_choi_pool_response()
    while response == False:
        response = rand_choi_pool_response()
    ippool = json.loads(response.text)['ippool']
    proxy_demo = random.choice(ippool)
    proxies = {
        'http': proxy_demo,
        'https': proxy_demo.replace('http', 'https'),
    }
    # print(proxies)
    return proxies

def proxy_ip():
    # return 'http://127.0.0.1:8888'
    response = rand_choi_pool_response()
    while response == False:
        response = rand_choi_pool_response()
    ippool = json.loads(response.text)['ippool']
    proxy = random.choice(ippool)
    return proxy

async def asy_rand_choi_pool_response():  # 适用于aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url)
            res = await response.read()
            return res.decode('utf-8')
    except:
        return False

ip_lists = []
update=time.time()
async def asy_rand_choi_pool():
    # return 'http://127.0.0.1:8888'
    global ip_lists
    global update
    if (len(ip_lists) == 0) or (time.time()-update>=60):
        response = await asy_rand_choi_pool_response()
        while response == False:
            response = await asy_rand_choi_pool_response()
        ippool = json.loads(response)['ippool']
        ip_lists = ippool
    if len(ip_lists) != 0:
        proxy = ip_lists.pop()
        return proxy

if __name__ == '__main__':
    for i in range(3):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asy_rand_choi_pool())