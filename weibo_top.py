import os
import re
import requests
from datetime import datetime

url = 'https://s.weibo.com/top/summary'
headers = {
    'Cookie': 'SINAGLOBAL=9984350838163.459.1639458131480; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWO7Xc2TqZUpUycnXX6JX6G5JpX5KMhUgL.Foqfe0271hBRe0B2dJLoI05LxK.L1KnLB.qLxKnLBK-LB.qLxK-L1K5LBKMLxKqL12zL1h.LxKqL12zL1hLaUJYt; UOR=github.com,s.weibo.com,github.com; ALF=1671167985; SSOLoginState=1639631986; SCF=AhYJZS5_n-2dh-fzeiiEVulWxpdZqWntw9i3SlVXNoxUG7nVw525cA-RvYIjqDnhJz3aOcJm4ub12l960WyxyIk.; SUB=_2A25MvrwiDeRhGeBL6FMR-CrEyDiIHXVvzarqrDV8PUNbmtAKLWrukW9NRzPQ6E6AXRvm1lK42mH2xgs76kKYLLtk; _s_tentry=login.sina.com.cn; Apache=8670087538783.595.1639631987208; ULV=1639631987217:8:8:8:8670087538783.595.1639631987208:1639562719229',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
response = requests.get(url, headers=headers, timeout=3).content.decode()
href = re.findall(r'<a href="(/weibo\?q=.*&Refer=top)" target="_blank">(.*?)</a>[\s]*<span> (.*?)</span>', response)

date = datetime.now().strftime("%Y-%m-%d")

for item in href:
    baseurl, title, index = item
    url = 'https://s.weibo.com/'+baseurl
    with open('/demo/weibo_data/'+date+'-origin.md', 'a', encoding='utf-8')as f:
        f.write('['+title+']'+'('+url+')'+' '+index+"\r\n")

with open('/demo/weibo_data/'+date+'-origin.md', 'r', encoding='utf-8')as f:
    datalist = f.read().split('\n')

if '' in datalist:
    while '' in datalist:
        datalist.remove('')

counts = {}
for i in range(len(datalist)):
    t = datalist[i].split(']')[0].split('[')[1]
    d = datalist[i].split(' ')[-1]
    u = datalist[i].split('](')[1].split(')')[0]
    counts[t] = '('+u+')'+' '+d

items = list(counts.items())
items.sort(key=lambda x: int(x[1].split(' ')[-1]), reverse=True)
if os.path.exists('/demo/weibo_top/result/'+date+'.md'):
    os.remove('/demo/weibo_top/result/'+date+'.md')
for i in range(len(items)):
    tt, ud = items[i]
    with open('/demo/weibo_top/result/'+date+'.md', 'a', encoding='utf-8')as f:
        f.write(str(i+1)+'. '+'['+tt+']'+ud+"\r\n")

print("Completed")






