import os
import re
import requests
from datetime import datetime

cookies = {
    'SUB': '_2A25Jjop5DeRhGeBL6FMR-CrEyDiIHXVq_fyxrDV8PUNbmtANLW_FkW9NRzPQ6EWCJ39WF_nBElMJpRCvLxVp629F',
}
response = requests.get('https://s.weibo.com/top/summary', cookies=cookies, timeout=3).text

href = re.findall(r'<a href="(/weibo\?q=.*&Refer=top)" target="_blank">(.*?)</a>[\s]*<span> (.*?)</span>', response)
# 时间格式，用于命名
date = datetime.now().strftime("%Y-%m-%d")
# 储存原始数据
for item in href:
    baseurl, title, index = item
    url = 'https://s.weibo.com/'+baseurl
    with open('./weibo_data/'+date+'-origin.md', 'a')as f:
        f.write('['+title+']'+'('+url+')'+' '+index+"\r\n")
# 从本地读取原始数据并去掉空元素
with open('./weibo_data/'+date+'-origin.md', 'r')as f:
    datalist = f.read().split('\n')
if '' in datalist:
    while '' in datalist:
        datalist.remove('')
# 新建字典暂存
counts = {}
for k in range(len(datalist)):
    t = datalist[k].split(']')[0].split('[')[1]   # 标题
    d = datalist[k].split(' ')[-1]  # 热度
    u = datalist[k].split('](')[1].split(')')[0]  # 链接
    # 以热度为键
    counts[int(d)] = u+', '+t
# 热度降序
items = list(counts.items())
items.sort(key=lambda x: int(x[0]), reverse=True)
# 获取相同标题的键
repeatindex = []
for i in range(len(items)):
    for k in range(i+1, len(items)):
        if items[i][1].split(', ')[-1] == items[k][1].split(', ')[-1]:
            repeatindex.append(items[k][0])
# 去重
for i in set(repeatindex):
    counts.pop(i)
# 储存整理好的数据，按热度降序
if os.path.exists('./result/'+date+'.md'):
    os.remove('./result/'+date+'.md')
index = 0
for i in sorted(counts, reverse=True):
    index += 1
    with open('./result/'+date+'.md', 'a')as f:
        f.write(str(index)+'. '+'['+counts[i].split(', ')[1]+']'+'('+counts[i].split(', ')[0]+')'+' '+str(i)+"\r")
item_start = """
# 今日热门搜索  
"""
item_end = """
# 声明 
本项目的所有数据来源均来自 [新浪微博热搜榜](https://s.weibo.com/top/summary)  
"""
with open('./result/'+date+'.md', 'r+')as f:
    content = f.read()
if os.path.exists('./README.md'):
    os.remove('./README.md')
with open('./README.md', 'a')as f:
    f.write(item_start+content+item_end)
print("Completed")
print(date)
