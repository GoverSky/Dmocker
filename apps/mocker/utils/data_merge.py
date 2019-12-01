#-*- coding: utf-8 -*-
# @Time    : 2019/7/11 19:46
# @File    : data_merge.py
# @Author  : 守望@天空~

from __future__ import absolute_import, unicode_literals
from  jsonpath_rw_ext import parse
from .data_generater import *

import re

def take_data(reg, data):
    """
    从已有数据中提取数据
    :param reg:  数据路径
    :param data:  数据源，dict
    :return: 提取的数据
    """
    text = reg[1:].split('.')
    for i in text:
        if isinstance(data, list) and i.isdigit():
            data = data[int(i)]
        elif isinstance(data,dict):
            data = data[i]
        else:
            return None
    return data

def isAllZh(s):
    '包含汉字的返回TRUE'
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False

def find_path(json,key):
    jsonpath_expr = parse('$..*[?(*="{}")]'.format(key))
    tmp = [match for match in jsonpath_expr.find(json)]
    result = []
    for row in tmp:
        e = filter(lambda a:a[1]==key, row.value.items())
        col = list(e)[0][0]
        if isAllZh(col):
            col = '["%s"]' %col
        result.append( ".".join((str(row.full_path),col)))
    return result

def get_value(json,jsonpath):
    data = [i.value for i in parse(jsonpath).find(json)]
    if data:
        return data[0]
    else:
        return ""

def data_associate(data,fromdata={}):
    """
    用于数据生成与关联
    :param data: 元数据数据
    :param fromdata: 关联数据源
    :return: 生成后的数据s
    """
    if isinstance(data,list):
        result = []
        for i in data:
            result.append(data_associate(i,fromdata))

    elif isinstance(data,dict):
        result = {}
        for key, value in data.items():
            if isinstance(value,(dict,list)):
                result[key]=data_associate(value,fromdata)

            elif isinstance(value,(str,str)):
                if value:
                    if value.startswith('m$'):
                        # 从已有数据中提取
                        result[key]=take_data(value[1:],fromdata)
                    elif value.startswith('m@'):
                        # 根据mock规则生成数据
                        reg = re.compile(u"[\(\),@]")
                        args_text = re.split(reg, value)
                        while u"" in args_text:
                            args_text.remove(u"")
                        text='%s%s' %(args_text[1][0].upper(),args_text[1][1:])
                        args = args_text[2:]
                        try:
                            method =eval(text)
                            # method = getattr(__builtins__,text,False)
                            result[key]=method(*args)()
                        except:
                            result[key] = value
                    else:
                        result[key]=value
                else:
                    result[key] = value
            else:
                result[key] = value
    else:
        result=None
    return result

if __name__ == '__main__':
    data1= {"status":{"测试数据":123123}}
    data2 = {'status': 'm$status.测试数据',u"time":u"m@datetime('%Y%m%d%H%M%S')",u"result":
        {u"id":'m@float(20,30,6-4)','name':'m@cname','telephone':'m@telephone',u"date":u"m@datetime(%Y-%m-%d)",u"ip":u"m@ip",u"title":u"m@cname"}}

    # print( str(data_associate(data=data2,fromdata=data1)).decode("str_escape"))
    print(get_value(data1,"status.['测试数据']"))
    print(take_data("$status.测试数据",data1))
