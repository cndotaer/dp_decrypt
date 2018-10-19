#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 23:20:32 2018

@author: cuiguiyang
"""

from bs4 import BeautifulSoup
import requests
import re

css_content = '.df-Y5KQ{background:-574.0px -427.0px;}span[class^="ol-"]{width: 12px;height: 30px;margin-top: -12px;background-image: url(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/1129eab0599a3a0e593a786e74013f04.svg);background-repeat: no-repeat;display: inline-block;vertical-align: middle;}.df-EryH{background:-350.0px -1687.0px;}'

# http://www.runoob.com/python/python-reg-expressions.html
# https://www.cnblogs.com/whaozl/p/5462865.html
# http://www.runoob.com/python/python-strings.html
#res = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{3})', css_content)
#print(res.groupdict())

pattern_prefix = re.compile(r'(\S{2}(?=-\S{4}{))')
result_prefix = pattern_prefix.findall(css_content)

pattern_prefix = re.compile(r'(?<=class\^=\")\S{3}')
result_prefix = pattern_prefix.findall(css_content)
print('前缀：', result_prefix)

p_svg_href = re.compile(r'(?<=url\()(\S{1,}(?=\);background))')
result_svg_href = p_svg_href.findall(css_content)
print('背景：', result_svg_href)


pattern_char = re.compile(r'(\S{4}(?={background))')
result_char = pattern_char.findall(css_content)
print(result_char)
for char in result_char:
    r_prefix = r'\S{2}(?=\-' + char + ')'
    print('prefix', re.compile(r_prefix).findall(css_content), end=' ')
    r_position_x = r'(?<=' + char + '{background:-)\d{1,}'
    print('position_x', re.compile(r_position_x).findall(css_content), end=' ')
    
    r_position_y = r'(?<=' + char + '{background:-\d{3}.\dpx -)\d{1,4}|(?<=' + char + '{background:-\d{2}.\dpx -)\d{1,4}|(?<=' + char + '{background:-\d{1}.\dpx -)\d{1,4}'
    print('position_y', re.compile(r_position_y).findall(css_content))


#pattern_position = re.compile(r'((\d{1,}.\d{1,}(?=px;}))|(\d{1,}.\d{1,}(?=px -)))')
#result_position = pattern_position.findall(css_content)

pattern_position_x = re.compile(r'(\d{1,}.\d{1,}(?=px -))')
result_position_x = pattern_position_x.findall(css_content)

pattern_position_y = re.compile(r'(\d{1,}.\d{1,}(?=px;}))')
result_position_y = pattern_position_y.findall(css_content)


# 获取SVG图片内容
svg_content = requests.get('http:' + result_svg_href[0]).text
print('svg', svg_content)
soup = BeautifulSoup(svg_content)
for text in soup.find_all('text', 'textStyle'):
    print(text['y'], text.string)
