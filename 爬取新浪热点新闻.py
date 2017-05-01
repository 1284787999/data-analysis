#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author;Tsukasa

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pandas as pd

#生产js网页 1-20
appendurl_new = []
url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1491844351564'
for i in range(1,31):
    appendurl_new.append((url.format(i)))
#生产js网页里面带的url
url_js = []
for url_new in appendurl_new:
    res = requests.get(url_new)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for a in jd['result']['data']:
        url_js.append(a['url'])


#解析url
def content(newsurl):
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')
    header = soup.select('h1')[0].text    #标题
    text = '\n\t'.join([p.text.strip() for p in soup.select('#artibody p ')[:-1]])  #内文文章
    editor = soup.select('#artibody p ')[-1].text.lstrip('责任编辑：')
    timesource = soup.select('.time-source')[0].contents[0].strip()   #timesource and dt 时间
    dt = datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    dt = dt.strftime('%Y-%m-%d\t%H:%M')
    madesource = soup.select('.time-source')[0].contents[1].text.strip()    #发布来源
    print(header,'\n',dt,madesource,'\n\t',text,'\n责任编辑：',editor,'\n\n\n\n')    #       #

def pandas_to_csv(pd_list):
    pd_look = pd.DataFrame(pd_list)
    pd_look.to_csv('房天下.csv',mode='a+',header=False)


#爬取首页url
res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
newslist = []
soup = BeautifulSoup(res.text,'html5lib')
for news in soup.select('.news-item'):
    if len(news.select('h2')) > 0:
        htmlurl = news.select('a')[0]['href']
        newslist.append(htmlurl)

for end in url_js + newslist:
    pandas_to_csv(content(end))







