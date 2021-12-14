#!/usr/bin/env python3
# @version:python3.8
# -*- coding: utf-8 -*-

import re
import requests
from datetime import datetime

url = 'https://s.weibo.com/top/summary'
headers = {
    'Cookie': 'SUB=_2AkMWIiw7f8NxqwJRmP4Tz2jgaYp2ywzEieKgft3gJRMxHRl-yT9jqm5btRB6PaIC1KGRQhNtnU2SE2eOyS_QR2BC8IPB; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhBQ_wfEcqkz5lIPBrDjwqC; _s_tentry=github.com; UOR=github.com,s.weibo.com,github.com; Apache=9984350838163.459.1639458131480; SINAGLOBAL=9984350838163.459.1639458131480; ULV=1639458131487:1:1:1:9984350838163.459.1639458131480:',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
response = requests.get(url, headers=headers, timeout=3).content.decode()
# print(response)

href = re.findall(r'<a href="(/weibo\?q=.*&Refer=top)".*>(.*?)</a>', response)

date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%X")

with open('/demo/weibo_top/result/'+date+'.md', 'a', encoding='utf-8')as f:
    f.write("\r\n")

with open('/demo/weibo_top/result/'+date+'.md', 'a', encoding='utf-8')as f:
    f.write(time)
    f.write("\n"+"---"+"\n")

i = 0
for item in href:
    i += 1
    a, b = item
    url = 'https://s.weibo.com/' + a
    title = b
    # print('['+title+']'+'('+url+')')
    with open('/demo/weibo_top/result/'+date+'.md', 'a', encoding='utf-8')as f:
        f.write(str(i)+'. '+'['+title+']'+'('+url+')'+'\r\n')

print("Completed!")








