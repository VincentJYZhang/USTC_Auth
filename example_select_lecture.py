"""
这个脚本可以选学术报告
非常简洁方便，仅作参考
初代版本见：https://github.com/VincentJYZhang/USTC_Lecture/blob/main/lecture_select/lecture_select.py
"""

from ustc_auth import USTC_Auth
from urllib import parse


# 直接实例化，已经与服务器建立session
auth = USTC_Auth('SA21******', '***********')  # 填写学号、密码


url = 'http://yjs.ustc.edu.cn/bgzy/m_bgxk_up.asp'

lecture_id = '555' # 学术报告的编号

# 生成urlencode的post data格式
form_data = parse.urlencode({"selectxh": int(lecture_id), "select": "true"})

# 直接post
auth.post_with_headers(url, data = form_data)
