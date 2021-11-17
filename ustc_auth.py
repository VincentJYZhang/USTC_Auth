# -*- coding: utf-8 -*-
"""
USTC_Auth
统一认证平台的爬虫接口，有效性验证于2021.11。


======================

仅供学习交流使用，开发者对使用或不使用本脚本造成的问题不负任何责任。

source: https://github.com/VincentJYZhang/USTC_Auth
Tue Nov 16 2021
"""


import requests
from requests._internal_utils import to_native_string
from requests.compat import is_py3


# USTC的教务网有个问题，他的重定向编码不是utf8，requests库自动解码会出问题
# 这里将requests库里的重定向函数hook出来重写
def get_redirect_target(self, resp):
    """hook requests.Session.get_redirect_target method"""
    if resp.is_redirect:
        location = resp.headers['location']
        if is_py3:
            location = location.encode('latin1')
        encoding = resp.encoding if resp.encoding else 'utf-8'
        return to_native_string(location, encoding)
    return None


def patch():
    requests.Session.get_redirect_target = get_redirect_target




class USTC_Auth(object):
    """
    USTC统一身份认证器
    """


    def __init__(self, user_id, user_pwd, latency = False):
        """
        user_id: 学号
        user_pwd: 密码
        latency: 实例化时是否延迟进行统一认证，
                    True: 先不进行认证，调用auth()进行认证
                    False: 立即进行认证，与服务器的session将立刻建立（default）
        """
        self.__user_id = user_id
        self.__user_pwd = user_pwd

        if latency:
            self.__session = None
        else:
            self.__session = self.auth_session(self.__user_id, self.__user_pwd)


    def get_session(self):
        """
        获取与服务器的session对象
        """
        return self.__session


    def auth_session(self, stu_id, pwd):
        """与服务器建立SESSION
        """
        
        headers = {
            "Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "sec-ch-ua":'" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
            "sec-ch-ua-mobile":"?0",
            "Origin":"https://passport.ustc.edu.cn",
            "Upgrade-Insecure-Requests":"1",
            "DNT":"1",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Sec-Fetch-Site":"same-origin",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-User":"?1",
            "Sec-Fetch-Dest":"document",
            "Referer":"https://passport.ustc.edu.cn"
        }
    
        # 最新的统一登陆系统增加了一个CAS认证，所以前面几步在模拟这个流程
    
        url_raw = "https://passport.ustc.edu.cn/login?service=http%3A%2F%2Fyjs%2Eustc%2Eedu%2Ecn%2Fdefault%2Easp"
        
        url = "https://passport.ustc.edu.cn/login"
    
        s = requests.Session()
    
        r = s.get(url_raw, headers=headers)
    
        import re
    
        pattern = r'name="CAS_LT" value=".+?">'
        index = re.search(pattern, r.text).span()
    
        CAS_LT = r.text[index[0]+21:index[1]-2]
    
        form_data = """model=uplogin.jsp&CAS_LT={}&service=http%3A%2F%2Fyjs.ustc.edu.cn%2Fdefault.asp&warn=&showCode=&username={}&password={}&button=""".format(CAS_LT, stu_id, pwd)
    
        r = s.post(url, headers=headers, data=form_data)
    
        if r.status_code != 200:
            raise Exception('status code: ' + r.status_code)
    
        return s

    
    def auth(self):
        """
        进行统一认证，当latency=True时，调用此函数进行认证
        """
        self.__session = auth_session(self.__user_id, self.__user_pwd)
        return None

    
    def get(self, url, *args, **kwargs):
        patch()
        return self.__session.get(url, *args, **kwargs)    
    

    def post(self, url, *args, **kwargs):
        patch()
        return self.__session.post(url, *args, **kwargs)

    
    def get_with_headers(self, url, *args, **kwargs):
        """
        因为知道很多人懒得写header，所以提供了一个默认的header，不推荐使用
        """

        headers = {
            "Proxy-Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "Origin":"http://yjs.ustc.edu.cn",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer":"http://yjs.ustc.edu.cn/bgzy/m_bgxk_up.asp",
            "Accept-Language":"zh-CN,zh;q=0.9"
        }

        patch()

        return self.__session.get(url, headers = headers, *args, **kwargs)

    def post_with_headers(self, url, *args, **kwargs):
        """
        因为知道很多人懒得写header，所以提供了一个默认的header，不推荐使用
        """

        headers = {
            "Proxy-Connection":"keep-alive",
            "Cache-Control":"max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "Origin":"http://yjs.ustc.edu.cn",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer":"http://yjs.ustc.edu.cn/bgzy/m_bgxk_up.asp",
            "Accept-Language":"zh-CN,zh;q=0.9"
        }

        patch()

        return self.__session.post(url, headers = headers, *args, **kwargs)



if __name__ == "__main__":

    auth = USTC_Auth('SA21******', '*********')
    r = auth.get('xxx.xxx.xxx')
    
