#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 23:33:46 2018

@author: cuiguiyang
"""


import requests
from bs4 import BeautifulSoup
import re
import css_analysis
import time


# svg转码字典
_code_dict = {}
_svg_css_href = ''
# URL
url = 'https://www.dianping.com/shop/77307732'

# 代理
# https://github.com/jhao104/proxy_pool
url_get_proxy = 'http://123.207.35.36:5010/get/'
def getProxy():
    return requests.get(url_get_proxy).content
#print(getProxy())

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


def get_comment(url):
    # 获取SVG图片对应的CSS链接
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#find-all
    css_links = soup.find_all('link', attrs={'rel':'stylesheet', 'href':re.compile("svgtextcss")})[0]
    svg_css_href = css_links['href']
    if svg_css_href.index('//') == 0:
        _svg_css_href = svg_css_href.replace('//', 'http://')
    
    # 制作SVG字典
    if (len(_code_dict.keys()) < 1):
        _code_dict = analysis()
    
    # 获取评论
    soup = BeautifulSoup(get_page(url))
    comment_item = soup.find_all('p', 'desc')
    first_comment = comment_item[0]
    real_comment = comment_decrypt(first_comment)
    print(real_comment)



# 获取并返回完整的评论
def comment_decrypt(comment):
    comments = []
    ret_comment = ''
    for content in comment.contents:
        if content.name == 'span':
            class_name = content['class'][0]
            print(class_name)
            char = _code_dict[class_name[:3]][class_name[3:]]['char']
            comments.append(char)
        else:
            comments.append(content.string)
    ret_comment = ''.join(comments).replace('\xa0', ' ')
    print(ret_comment)
    return ret_comment

# 根据class名称获取对应的汉字
def get_char(class_name):
    try:
        return _code_dict[class_name[:3]][class_name[3:]]['char']
    except:
        _code_dict = analysis()
        return get_char(class_name)

# 解析CSS并返回字典
def analysis():
    # SVG 图片对应的CSS内容
    css_content = requests.get(_svg_css_href).text
    print('解析CSS,并生成字典')
    # 格式化成2016-03-20 11:45:39形式
    print('start at ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    _code_dict = css_analysis.analysis(css_content)
    print('end   at ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return _code_dict


if __name__ == "__main__":
    print('Hello Python')

