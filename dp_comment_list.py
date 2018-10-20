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
import json
import random

# svg转码字典
g_code_dict = {}
g_svg_css_href = ''
# URL
url = 'https://www.dianping.com/shop/77307732'

# 代理
# https://github.com/jhao104/proxy_pool
url_get_proxy = 'http://123.207.35.36:5010/get/'
def getProxy():
    return requests.get(url_get_proxy).content
#print(getProxy())

User_Agent = [
        'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
        'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
        'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
        'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
        ]

def get_page(url):
    header = {'User-Agent': random.choice(User_Agent),
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
    soup = BeautifulSoup(get_page(url), 'lxml')
    print(soup)
    
    print('获取SVG图片对应的CSS链接')
    # 获取SVG图片对应的CSS链接
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#find-all
    css_links = soup.find_all('link', attrs={'rel':'stylesheet', 'href':re.compile("svgtextcss")})[0]
    svg_css_href = css_links['href']
    if svg_css_href.index('//') == 0:
        g_svg_css_href = svg_css_href.replace('//', 'http://')
    print('svg_css_href: ', g_svg_css_href)
    
    print('制作SVG字典')
    # 制作SVG字典
    global g_code_dict
    if (len(g_code_dict.keys()) < 1):
        g_code_dict = analysis(False)
    
    # 获取评论
    comment_list = soup.find_all('p', 'desc')
    for comment in comment_list:
        real_comment = comment_decrypt(comment)
        print(real_comment, end='\n\n')
#    first_comment = comment_item[0]
#    real_comment = comment_decrypt(first_comment)
#    print(real_comment)

error_comment = {}
# 获取并返回完整的评论
def comment_decrypt(comment):
    comments = []
    ret_comment = ''
    global g_code_dict
    global error_comment
    try:
        for content in comment.contents:
            char = ''
            if content.name == 'span':
                class_name = content['class'][0]
                # print(class_name)
                char = g_code_dict[class_name[:3]][class_name[3:]]['char']
            else:
                char = content.string
            if not char:
                char = ''
#                print(content)
            comments.append(char)
#        print(comment)
        ret_comment = ''.join(comments).replace('\xa0', ' ')
    except:
        error_comment = comment
        print('Error', comment)
        return 'comment is empty'
    return ret_comment

# 根据class名称获取对应的汉字
def get_char(class_name):
    global g_code_dict
    try:
        return g_code_dict[class_name[:3]][class_name[3:]]['char']
    except:
        g_code_dict = analysis(False)
        return get_char(class_name)

# 解析CSS并返回字典
def analysis(force):
    global g_code_dict
    if not force:
        f = open('code_dict.json', 'r+')
        g_code_dict = json.loads(f.readline())
        if len(g_code_dict.keys()) < 1:
            g_code_dict = analysis(True)
        return g_code_dict
    
    # SVG 图片对应的CSS内容
    css_content = requests.get(g_svg_css_href).text
    print('解析CSS,并生成字典')
    # 格式化成2016-03-20 11:45:39形式
    print('start at ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    g_code_dict = css_analysis.analysis(css_content)
    print('end   at ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return g_code_dict


if __name__ == "__main__":
    print('Spider Start')
    g_code_dict = analysis(False)
    get_comment(url)

