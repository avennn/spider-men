#! python3
# -*- coding: utf-8 -*-

import os
import time

# 先断开网络连接，后面拨号才能正常
os.system(r"rasphone -h 宽带连接")
# 拨号上网，连路由器不是这样
os.system(r"rasdial 宽带连接 0755168202 88888888")
# 其实可有可无
# time.sleep(3)

# 断开网络
# os.system(r"rasphone -h 宽带连接")
# 断开网络，同上
# os.system(r"rasdial 宽带连接 /disconnect")
