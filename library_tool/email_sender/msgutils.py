# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2020-02-23 09:56:50
# @Version: 1.0.0
# @Description: SDK接口发送报警及邮件
import requests
import os


def send_weixin(message, users, agentid=None):
    burl = "{你的路由}/weixin?"
    url = f"{burl}to_user={users}&message={message}"
    if agentid:
        url = url + f"&agentid={agentid}"
    resp = requests.get(url=url)
    if resp.status_code == 200:
        return True
    return False


def send_mail(title, message, to_addr, message_type="html", from_name='爬虫异常报警', from_user="{example@xx.com}",
              attach_list=None):
    send_url = "{你的路由}/email/send"
    param = {
        "from_name": from_name,
        "from_user": from_user,
        "to_user": to_addr,
        "title": title,
        # "cc": cc_addr,
        "message": message,
        "message_type": message_type,
        "s": "zlbx_c"
    }

    _files = {}
    # 构造附件
    try:
        for fname in attach_list:
            if os.path.exists(fname):
                _files[os.path.basename(fname)] = open(fname, 'rb')
    except Exception as e:
        pass
    if _files:
        response = requests.post(url=send_url, data=param, files=_files)
    else:
        response = requests.post(url=send_url, data=param)
    if response.status_code == 200:
        return True
    return False


if __name__ == '__main__':
    to_addr = "{发送者邮箱}"
    send_mail(title='收到邮件了吗', message='邮件已发送请查收', to_addr=to_addr)
