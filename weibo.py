# coding=gbk
import os
import re
import requests
from datetime import datetime

'''
1. 爬取数据
2. 去重数据
    把每次爬取的数据储存在本地（.txt）
        需定期删除该文件
    每次运行程序都从本地读取数据
    使用字典（dict）的方式再次整理数据 可以达到去重目的
    使用sort+lambda排序
    将整理的数据储存在本地（.md）
3. 上传数据（git）
'''

url = 'https://s.weibo.com/top/summary'
headers = {
    'Cookie': 'SUB=_2AkMWIiw7f8NxqwJRmP4Tz2jgaYp2ywzEieKgft3gJRMxHRl-yT9jqm5btRB6PaIC1KGRQhNtnU2SE2eOyS_QR2BC8IPB; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhBQ_wfEcqkz5lIPBrDjwqC; _s_tentry=github.com; UOR=github.com,s.weibo.com,github.com; Apache=9984350838163.459.1639458131480; SINAGLOBAL=9984350838163.459.1639458131480; ULV=1639458131487:1:1:1:9984350838163.459.1639458131480:',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
response = requests.get(url, headers=headers, timeout=3).content.decode()
href = re.findall(r'<a href="(/weibo\?q=.*&Refer=top)".*>(.*?)</a>', response)
index = re.findall(r'<span> (.*?)</span>', response)

# 去掉index列表中的空元素
if '' in index:
    while '' in index:
        index.remove('')

date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%X")

# 将数据储存到本地...有点乱
for item in index:
    with open('/demo/weibo_data/'+'index_{}.txt'.format(date), 'a', encoding='utf-8')as f:
        f.write(item+',')
for item in href:
    a, title = item
    url = 'https://s.weibo.com/' + a
    with open('/demo/weibo_data/'+'title_{}.txt'.format(date), 'a', encoding='utf-8') as f:
        f.write(title+',')
    with open('/demo/weibo_data/'+'url_{}.txt'.format(date), 'a', encoding='utf-8') as f:
        f.write(url+',')

# 读取本地数据文件
with open('/demo/weibo_data/'+'index_{}.txt'.format(date), 'r', encoding='utf-8') as f:
    indexlist = f.read()
dex = indexlist.split(',')
dex.pop(-1)
print(len(dex))
with open('/demo/weibo_data/'+'title_{}.txt'.format(date), 'r', encoding='utf-8') as f:
    titlelist = f.read()
t = titlelist.split(',')
t.pop(-1)
print(len(t))
with open('/demo/weibo_data/'+'url_{}.txt'.format(date), 'r', encoding='utf-8') as f:
    urllist = f.read()
u = urllist.split(',')
u.pop(-1)
print(len(u))

# 去重并排序
counts = {}
for i in range(len(t)):
    counts[t[i]] = '('+u[i]+')'+' '+dex[i]
items = list(counts.items())
items.sort(key=lambda x: int(x[1].split(' ')[-1]), reverse=True)
# 由于是遍历写入数据，so 只能这样..
if not os.path.exists('/demo/weibo_top/result/'+date+'.md'):
    os.system(r"touch {}".format('/demo/weibo_top/result/'+date+'.md'))
os.remove('/demo/weibo_top/result/'+date+'.md')
for i in range(len(items)):
    tt, uu = items[i]
    with open('/demo/weibo_top/result/'+date+'.md', 'a', encoding='utf-8')as f:
        f.write(str(i+1)+'. '+'['+tt+']'+uu+"\r\n")

print("completed")

