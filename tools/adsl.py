#! python3
# -*- coding: utf-8 -*-

import os, time, re

Max = 50  # 设置下载次数，每个地址的下载次数；
g_adsl_account = {"name": "Tenda_15FC40", "username": "0755168202", "password": "88888888"}


class Adsl(object):
  # ==============================================================================
  # __init__ : name: adsl名称
  # ==============================================================================
  def __init__(self):
    self.name = g_adsl_account["name"]
    self.username = g_adsl_account["username"]
    self.password = g_adsl_account["password"]

  # ==============================================================================
  # set_adsl : 修改adsl设置
  # ==============================================================================
  def set_adsl(self, account):
    self.name = account["name"]
    self.username = account["username"]
    self.password = account["password"]

  # ==============================================================================
  # connect : 宽带拨号
  # ==============================================================================
  def connect(self):
    cmd_str = '''C:\Windows\System32\\rasdial.exe %s %s %s''' % (self.name, self.username, self.password)
    os.system(cmd_str)
    time.sleep(20)

  # ==============================================================================
  # disconnect : 断开宽带连接
  # ==============================================================================
  def disconnect(self):
    cmd_str = '''C:\Windows\System32\\rasdial.exe %s /disconnect''' % self.name
    os.system(cmd_str)

  # ==============================================================================
  # reconnect : 重新进行拨号
  # ==============================================================================
  def reconnect(self):
    self.disconnect()
    self.connect()


# for i in range(Max):
#     file_object = open('D:\code\urls.txt', "r")
#     cmd_run_wget = '''D:\wget\wget.exe --tries=2 --user-agent="Mozilla/5.0 (Linux; U; Android 4.2.1; zh-CN; MI 3 Build/JOP40D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.9.457 U3/0.8.0 Mobile Safari/533.1" -O D:\download-apk\download-%s.apk %s '''
#     for url_line in file_object.readlines():
#         patt = re.search("http.*\/(.*\.apk)", url_line)
#         file_name = patt.group(1)
#         os.system(cmd_run_wget % (file_name, url_line))
#     file_object.close()
#
#     a = Adsl()
#     a.reconnect()

a = Adsl()
a.reconnect()
