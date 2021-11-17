"""
这个脚本可以查看东区大礼堂上映电影的情况
包括日期票价余票等信息
仅作参考

代码输出示例：

名称            简介            日期            余票            开始时间        结束时间        票价        
长津湖           176分钟丨历史  10月29日        0               19:00           21:56           0.00      
老师·好          110分钟丨剧情  09月10日        464             18:30           20:20           0.00      
1921             137分钟丨历史  07月02日        138             15:00           17:17           0.00      
共产党宣言       150分钟丨历史  暂无场次      
我的姐姐         127分钟丨剧情  05月07日        858             18:30           20:37           5.00
"""


from ustc_auth import USTC_Auth
from bs4 import BeautifulSoup


def get_movie_ids(html_data):
    """
    从HTML页面中取出电影id列表
    """

    import re

    pattern = r'<div class="swiper-slide" data-id="\d+?"><img'

    movie_list = re.findall(pattern, html_data)

    return [movie[35:-6] for movie in movie_list]


def get_movie_details(html_data):
    """
    从HTML页面中提取电影细节
    """

    soup = BeautifulSoup(html_data, 'html.parser')

    movie_details = []

    movie_details.append(soup.div.div.a.h1.text)
    movie_details.append(soup.div.div.a.p.text)

    try:
        movie_details.append(soup.find('div', class_='date').p.text)
        movie_details.append(soup.find('div', class_='date').span.text[2:-1])
        movie_details.append(soup.find('div', class_='time').b.text)
        movie_details.append(soup.find('div', class_='time').span.text[:-2])
        movie_details.append(soup.find('div', class_='price').text[2:-25])
    except Exception:
        movie_details.append('暂无场次')

    return movie_details




# 直接实例化，已经与服务器建立session
auth = USTC_Auth('SA21******', '***********')  # 填写学号、密码

url = 'http://ghticket.ustc.edu.cn/'

# 直接get获取数据
r = auth.get_with_headers(url)

id_list = get_movie_ids(r.text)

# 打印
print("%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t"
    %('名称','简介','日期','余票','开始时间','结束时间','票价'))

for movie_id in id_list:
    r = auth.get_with_headers('http://ghticket.ustc.edu.cn/film_libraries/' + movie_id + '/ajaxshows')
    for detail in get_movie_details(r.text):
        print("%-10s"%detail, end='\t')
    print()

