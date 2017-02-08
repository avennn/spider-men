#! python3
# -*- coding: utf-8 -*-

from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.header import Header

class Mail(object):
  def __init__(self, from_email, from_pass, to_email, subject, message):
    # 记得修改下面的内容
    self.from_email = from_email
    self.from_pass = from_pass
    self.to_email = to_email
    # 第三方 SMTP 服务
    self.mail_host = 'smtp.163.com'  # 设置服务器
    self.mail_user = from_email  # 用户名
    self.mail_pass = from_pass  # 口令

    self.sender = from_email
    self.receivers = [to_email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    self.message = MIMEText(message, 'plain', 'utf-8')
    self.message['From'] = from_email
    self.message['To'] = to_email
    self.message['Subject'] = Header(subject, 'utf-8')
  def send_mail(self):
    try:
      smtpObj = SMTP()
      smtpObj.connect(self.mail_host, 25)
      smtpObj.login(self.mail_user, self.mail_pass)
      smtpObj.sendmail(self.sender, self.receivers, self.message.as_string())
      print('邮件发送成功')
    except SMTPException as e:
      print(e)
