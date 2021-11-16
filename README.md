# USTC_Auth
USTC统一认证平台的爬虫接口，有效性验证于2021.11

## 使用教程


### 实例化 `USTC_Auth`

`auth = USTC_Auth(user_id, user_pwd, latency = False)`

1. 填写学号、密码
2. `latency`提供延迟认证功能
    * False: 默认，直接建立session
    * True: 延迟建立session，实例化时未与服务器建立session，然后通过auth()函数建立

### 认证 `auth()`

只有实例化时选择`latency = True`时，需要手动执行`auth()`函数建立session；否则不需要

```
auth = USTC_Auth(user_id, user_pwd, latency = True)
auth.auth()
```

### `get/post`方法

与requests库的get/post方法一致。

```
r = auth.get('xxx.xxx.xxx', headers=headers)
r = auth.post('xxx.xxx.xxx', headers=headers, data=data)
```


### 获得session

取出session，可以做进一步的扩展：`my_session = auth.get_session()`

### 示例

```
from ustc_auth import USTC_Auth

# 直接实例化，已经与服务器建立session（默认）
auth = USTC_Auth('SA21******', '*********')  # 填写学号、密码

# get和post方法和requests库里的使用方法相同
r = auth.get('xxx.xxx.xxx', headers=headers)
r = auth.post('xxx.xxx.xxx', headers=headers, data=data)

r = auth.get_with_headers(url)   # 提供了一个默认的header
r = auth.post_with_headers(url)  # 提供了一个默认的header


my_session = auth.get_session()  # 取出session，可以做进一步的扩展


# 也可以延迟建立session，实例化时未与服务器建立session，然后通过auth()函数建立
auth = USTC_Auth('SA21******', '*********', latency = True)  # 填写学号、密码
auth.auth() # 与服务器建立session
```

## 应用实例

`example.py`里提供了一个小例子，可以看到非常简洁易操作。


---

方便的话给个Star呗~
