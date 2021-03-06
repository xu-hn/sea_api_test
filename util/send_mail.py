# coding = utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SendMail:

    def __init__(self, mail_host):
        self.mail_host = mail_host

    def send(self, title, content, sender, auth_code, receivers):
        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message["Subject"] = title
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用ssl发信，端口一般是465
            smtp_obj.login(sender, auth_code)  # 登录
            smtp_obj.sendmail(sender, receivers, message.as_string())
            print("Mail 发送成功")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 第三方 SMTP 服务
    mail = SendMail("smtp.163.com")
    sender = "x13436502588@163.com"
    receivers = ['350152004@qq.com']
    title = "sea 测试报告"
    content = """
    测试环境
    """

    # 授权码不是邮箱登录密码，网易邮箱可以通过 "设置"->客户端授权秘密，自己注册和用自己的授权码
    auth_code = "FFIJSXPDXNCOTGLT"
    mail.send(title, content, sender, auth_code, receivers)
