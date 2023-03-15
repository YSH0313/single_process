#!/usr/bin/python3
import ssl
import smtplib
from settings import EMAIL_CONFIG
from email.mime.text import MIMEText
from email.header import Header


class SendMail(object):
    def __init__(self):
        # 第三方 SMTP 服务
        self.email_host = EMAIL_CONFIG['email_host']  # 设置服务器
        self.email_user = EMAIL_CONFIG['email_user']  # 用户名
        self.email_pass = EMAIL_CONFIG['email_pass']  # 口令
        self.sender = EMAIL_CONFIG['sender']  # 发送者
        self.password = EMAIL_CONFIG['password']  # 发送者
        self.sender_nikename = None
        self.recipient_nikename = None
        self.theme = None
        self.email_port = EMAIL_CONFIG['email_port']
        self.receivers = EMAIL_CONFIG['receivers']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，发送多人用逗号隔开

    def edit_content(self, contents):
        msg = MIMEText(contents, 'plain', 'utf-8')  # 编辑要发送的内容
        msg['From'] = Header('异常爬虫报警', 'utf-8')  # 发件人
        msg['To'] = Header(self.receivers, 'utf-8')  # 收件人
        msg['Subject'] = self.theme  # 邮件的主题，也可以说是标题
        return msg

    def send_mail(self, contents):
        smtp = smtplib.SMTP(host=self.email_host, port=self.email_port)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        smtp.starttls(context=context)
        smtp.login(self.sender, self.password)  # 登录邮箱
        print('login!')
        try:
            smtp.sendmail(self.sender, self.receivers, self.edit_content(contents).as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
            print('success')
        except smtplib.SMTPException:
            print('error')
        finally:
            smtp.quit()  # 发送完毕后退出 smtp

        smtpObj = smtplib.SMTP()
        smtpObj.connect(self.email_host, self.email_port)  # 25 为 SMTP 端口号
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(self.email_user, self.email_pass)  # 登录账户
        smtpObj.sendmail(self.sender, self.receivers.split(','), self.edit_content(contents).as_string())  # 发送邮件，多人发送时转化接收者为列表状态
        print("\033[1;34;0m*******************邮件发送成功*********************\033[0m")

if __name__ == '__main__':
    send = SendMail()
    send.theme = '请查看是否成功'
    send.send_mail('你好，请查看是否成功!!!')
