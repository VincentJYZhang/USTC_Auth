"""
这个脚本可以查看一卡通信息
包括信息、余额等
仅作参考
"""

from ustc_auth import USTC_Auth

# 直接实例化，已经与服务器建立session
auth = USTC_Auth('SA21******', '***********')  # 填写学号、密码

url = 'https://ecard.ustc.edu.cn/'

# 直接get获取数据
r = auth.get_with_headers(url)

print(r.text) # 打印信息，未格式化，可以自己格式化文本
