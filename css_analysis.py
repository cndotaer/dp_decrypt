#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 23:20:32 2018

@author: cuiguiyang
"""

from bs4 import BeautifulSoup
import requests
import re


def test():
    css_content = '.df-Y5KQ{background:-574.0px -427.0px;}span[class^="ol-"]{width: 12px;height: 30px;margin-top: -12px;background-image: url(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/1129eab0599a3a0e593a786e74013f04.svg);background-repeat: no-repeat;display: inline-block;vertical-align: middle;}.df-EryH{background:-350.0px -1687.0px;}'
    
    # http://www.runoob.com/python/python-reg-expressions.html
    # https://www.cnblogs.com/whaozl/p/5462865.html
    # http://www.runoob.com/python/python-strings.html
    #res = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{3})', css_content)
    #print(res.groupdict())
    
    #pattern_prefix = re.compile(r'(\S{2}(?=-\S{4}{))')
    #result_prefix = pattern_prefix.findall(css_content)
    
    pattern_prefix = re.compile(r'(?<=class\^=\")\S{3}')
    result_prefix = pattern_prefix.findall(css_content)
    print('前缀：', result_prefix)
    
    p_svg_href = re.compile(r'(?<=url\()(\S{1,}(?=\);background))')
    result_svg_href = p_svg_href.findall(css_content)
    print('背景：', result_svg_href)
    dict_svg = {}
    for index, prefix in enumerate(result_prefix):
        href = result_svg_href[index]
        print(prefix, href)
        # 获取SVG图片内容
        try:
            print(dict_svg[prefix])
        except:
            dict_svg[prefix] = {}
            dict_svg[prefix]['y'] = []
        svg_content = requests.get('http:' + href).text
        print('svg', svg_content)
        soup = BeautifulSoup(svg_content)
        for text in soup.find_all('text', 'textStyle'):
            dict_svg[prefix]['y'].append(text['y'])
            dict_svg[prefix][text['y']] = {}
            dict_svg[prefix][text['y']] = text.string
            print(text['y'], text.string)
    print(dict_svg['ol-']['y'])
    
    
    pattern_char = re.compile(r'(\S{4}(?={background))')
    result_char = pattern_char.findall(css_content)
    print(result_char)
    dict_char = {}
    for char in result_char:
        print('char', char)
        r_prefix = r'\S{2}(?=\-' + char + ')'
        prefix = re.compile(r_prefix).findall(css_content)[0]
    #    print('prefix', prefix, end=' ')
        try:
            print('prefix', dict_char[prefix])
        except:
            print('{} not exist', prefix)
            dict_char[prefix] = {}
        
        dict_char[prefix][char] = {}
        r_position_x = r'(?<=' + char + '{background:-)\d{1,}'
        x = re.compile(r_position_x).findall(css_content)[0]
        print('position_x',x , end=' ')
        dict_char[prefix][char]['x'] = x
        
        r_position_y = r'(?<=' + char + '{background:-\d{3}.\dpx -)\d{1,4}|(?<=' + char + '{background:-\d{2}.\dpx -)\d{1,4}|(?<=' + char + '{background:-\d{1}.\dpx -)\d{1,4}'
        y = re.compile(r_position_y).findall(css_content)[0]
        print('position_y', y)
        dict_char[prefix][char]['y'] = y
    print(dict_char)
    print(dict_char['df'].keys())
    
    # 解析css中的位置
    #pattern_position_x = re.compile(r'(\d{1,}.\d{1,}(?=px -))')
    #result_position_x = pattern_position_x.findall(css_content)
    #pattern_position_y = re.compile(r'(\d{1,}.\d{1,}(?=px;}))')
    #result_position_y = pattern_position_y.findall(css_content)


    # 获取SVG图片内容
    svg_content = requests.get('http:' + result_svg_href[0]).text
    print('svg', svg_content)
    dict_svg = {}
    soup = BeautifulSoup(svg_content)
    for text in soup.find_all('text', 'textStyle'):
        print(text['y'], text.string)



def analysis(css_content):
    print('css analysis...')
    svg_dict = svg_analysis(css_content)
    print(svg_dict)
    css_dict = css_analysis(css_content, svg_dict)
    print(css_dict)
    return css_dict


def svg_analysis(css_content):
    pattern_prefix = re.compile(r'(?<=class\^=\")\S{3}')
    result_prefix = pattern_prefix.findall(css_content)
#    print('前缀：', result_prefix)
    
    p_svg_href = re.compile(r'(?<=url\()(\S{1,}(?=\);background))')
    result_svg_href = p_svg_href.findall(css_content)
#    print('背景：', result_svg_href)
    dict_svg = {}
    for index, prefix in enumerate(result_prefix):
        href = result_svg_href[index]
#        print(prefix, href)
        # 获取SVG图片内容
        try:
            dict_svg[prefix]
        except:
            dict_svg[prefix] = {}
            dict_svg[prefix]['y'] = []
        svg_content = requests.get('http:' + href).text
        print('svg', svg_content)
        soup = BeautifulSoup(svg_content)
        for text in soup.find_all('text', 'textStyle'):
            dict_svg[prefix]['y'].append(text['y'])
            dict_svg[prefix][text['y']] = {}
            dict_svg[prefix][text['y']] = text.string
#            print(text['y'], text.string)
#    print(dict_svg['ol-']['y'])
    return dict_svg


def css_analysis(css_content, svg_dict):
    pattern_char = re.compile(r'(\S{4}(?={background))')
    result_char = pattern_char.findall(css_content)
#    print(result_char)
    dict_char = {}
    for char in result_char:
#        print('char', char)
        r_prefix = r'\S{3}(?=' + char + '{)'
        prefix = re.compile(r_prefix).findall(css_content)[0]
        # print('prefix', prefix, end=' ')
        try:
            dict_char[prefix]
        except:
#            print('{} not exist', prefix)
            dict_char[prefix] = {}
        
        dict_char[prefix][char] = {}
        r_position_x = r'(?<=' + char + '{background:-)\d{1,}'
        x = re.compile(r_position_x).findall(css_content)[0]
#        print('position_x',x , end=' ')
        dict_char[prefix][char]['x'] = x
        
        r_position_y = r'(?<=' + char + '{background:-\d{3}.\dpx -)\d{1,4}|(?<=' + char + '{background:-\d{2}.\dpx -)\d{1,4}|(?<=' + char + '{background:-\d{1}.\dpx -)\d{1,4}'
        y = re.compile(r_position_y).findall(css_content)[0]
#        print('position_y', y)
        dict_char[prefix][char]['y'] = y
        dict_char[prefix][char]['char'] = code_decrypt(svg_dict, prefix, char, x, y)
#    print(dict_char)
#    print(dict_char['df'].keys())
    return dict_char

def code_decrypt(svg_dict, prefix, code, x, y):
    line = ''
#    print(svg_dict)
    try:
        svg_dict[prefix]
    except:
        return ''
    for code_y in svg_dict[prefix]['y']:
        if int(code_y) >= int(y):
            line = code_y
            break
    index = int(int(x) / 14)
#    print(index)
    return svg_dict[prefix][line][index]
    



#analysis(css_content)
