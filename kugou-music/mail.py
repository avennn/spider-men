#! python3
# -*- coding: utf-8 -*-

from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.header import Header

# 记得修改下面的内容
from_email = 'xxx@163.com'
from_pass = 'sss'
to_email = '123@qq.com'

# 第三方 SMTP 服务
mail_host = 'smtp.163.com'  # 设置服务器
mail_user = from_email  # 用户名
mail_pass = from_pass  # 口令

sender = from_email
receivers = [to_email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

subject = 'python邮件测试'
message = MIMEText('这是通过python自动发送的一封测试邮件...', 'plain', 'utf-8')
message['From'] = from_email
message['To'] = to_email
message['Subject'] = Header(subject, 'utf-8')

if __name__ == '__main__':
  try:
    smtpObj = SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print('测试邮件发送成功')
  except SMTPException as e:
    print(e)
