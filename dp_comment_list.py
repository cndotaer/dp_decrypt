#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 23:33:46 2018

@author: cuiguiyang
"""


import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.dianping.com/shop/77307732'
html = ''

# https://github.com/jhao104/proxy_pool
url_get_proxy = 'http://123.207.35.36:5010/get/'
def getProxy():
    return requests.get(url_get_proxy).content

print(getProxy())

def get_page(url):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
              'Cookie': 'navCtgScroll=0; _hc.v=19d6f99d-e06a-6a88-2f2d-f480266333dd.1539873086; _lxsdk_cuid=16687969c33c8-005ab2904888e5-1f396652-1aeaa0-16687969c3388; _lxsdk=16687969c33c8-005ab2904888e5-1f396652-1aeaa0-16687969c3388; s_ViewType=10; _lxsdk_s=1668cbf503c-3da-641-fa2%7C%7C29',
#              'Cache-Control': 'no-cache',
#              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#              'Accept-Encoding': 'gzip, deflate',
#              'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
#              'Connection': 'keep-alive',
              'Host': 'www.dianping.com',
#              'Pragma': 'no-cache',
              'Referer': 'http://www.dianping.com/shop/76859748',
              'Upgrade-Insecure-Requests': '1'
              }
    proxy = getProxy()
    page = requests.get(url, headers=header, proxies={"http": "http://{}".format(proxy)})
    return page.text


def get_comment_all(url):
    soup = BeautifulSoup(get_page(url))
    comment_list = soup.find_all('ul', id='reviewlist-wrapper')
    comment_item = soup.find_all('p', 'desc')
    first_comment = comment_item[0]
    # 获取 SVG 图片对应的CSS内容
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#find-all
    css_links = soup.find_all('link', attrs={'rel':'stylesheet', 'href':re.compile("svgtextcss")})[0]
    svg_css_href = css_links['href']
    if svg_css_href.index('//') == 0:
        svg_css_href = svg_css_href.replace('//', 'http://')
    # SVG 图片对应的CSS内容
    svg_css_content = requests.get(svg_css_href).text
    # 解析CSS并制作字典

def css_analysis(css_content):
    print('解析CSS,并生成字典')
