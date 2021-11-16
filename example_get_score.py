"""
这是个获取研究生网成绩表的例子
非常简便，仅作参考
"""


from ustc_auth import USTC_Auth


# 直接实例化，已经与服务器建立session
auth = USTC_Auth('SA21******', '***********')  # 填写学号、密码

url = 'http://yjs.ustc.edu.cn/score/m_score.asp'

# 直接get获取数据
r = auth.get_with_headers(url)

print(r.text) # 打印各项成绩，未格式化，可以自己格式化文本
