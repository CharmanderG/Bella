#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2018-03-17 16:12:05
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : record the prcess of python library learning

# 本文主要记录python各种包和库的学习过程，方便之后学习和安装
# 
# 备注：正常安装（速度慢）：pip install 包名
# 
#       快速安装（靠镜像）：pip install -i https://pypi.doubanio.com/simple 包名


import pytesseract
# 与（ORC）光学字符识别有关，全称为Optical Character Recognition，
# 简单来说就是识别图片上的文字，一开始接触于百万英雄答题外挂，用于截取答题页面截图后，
# 分析识别图片上的文字，后来又在黑板客爬虫游戏中应用，用于动态验证码识别

from aip import AipOcr
# 同样是用于识别图片文字的，来源于百度的api。
# 如果已安装pip，执行pip install baidu-aip即可；如果已安装setuptools，执行python setup.py install即可。
# 第一次使用是在2018-03-28 20:48:36，用于和pytesseract识别图片做对比

from PIL import Image
# 一开始是在廖雪峰老师的Python教程上学到的，主要是用来处理图片的，可以做旋转、模糊二值化等等。
# PIL：Python Imaging Library，已经是Python平台事实上的图像处理标准库了。PIL功能非常强大，但API却非常简单易用。
# 由于PIL仅支持到Python 2.7，加上年久失修，于是一群志愿者在PIL的基础上创建了兼容的版本，名字叫Pillow，
# Pillow支持最新Python 3.x，又加入了许多新特性，因此，我们可以直接安装使用Pillow。
# Python 2.7安装PIL，在Debian/Ubuntu Linux下直接通过apt安装：$ sudo apt-get install python-imaging。
# Python 2.7安装PIL，Windows平台就去PIL官方网站下载exe安装包。[url](http://pythonware.com/products/pil/)
# Python 3.x安装PIL,如果安装了Anaconda，Pillow就已经可用了。否则，需要在命令行下通过pip安装：$ pip install pillow
# 
# 补充一下由bytes数组直接转换成Image对象的方法，时间2018-05-03 13:53
#    从网上下载图片bytes，直接转换成Image对象
#    from PIL import Image
#    import requests
#    import io
#
#    image_data = requests.get(target_url).content
#    stream = io.BytesIO(image_data)
#    img = Image.open(stream)
#    img.show();

import base64
# 这个模块也是从廖雪峰老师的Python教程上可是接触的，主要负责对字符串进行base64的编码和解码工作
# 第一次正式使用应该是做一道程序员闯关题目，其中有一道题是将一副图片的数据进行了base64的编码
# 然后进行进制转换，最后以二进制空缺的形式显示作为题目入口，想想确实有点难度
# 问题解析过程：https://blog.csdn.net/albertsh/article/details/53214913
# 解题源码：https://github.com/AlbertGithubHome/Bella/blob/master/python/1111.segmentfault.com/01decode.py
# 时间：2016年11月18日 12:04:09

from functools import reduce
# 话说这个模块我之前已经没有印象了，后来发现同样出于廖雪峰老师之手。
# 通常和map函数连用，如果你没有听过map/reduce，那么Hadoop总该听说过了吧，这两者的思想是一致的
# 第一次实际使用同样是解决上边这道题，如果不用这个库，代码会很长，用了之后代码量锐减。
# 这这个例子中主要是用它把所有的单个字母串联到一起，这种情况使用map/reduce刚刚好。
# 很奇怪map这个函数为什么不在functools中
# 问题解析过程：https://blog.csdn.net/albertsh/article/details/53214913
# 解题源码：https://github.com/AlbertGithubHome/Bella/blob/master/python/1111.segmentfault.com/01decode.py
# 时间：2016年11月18日 12:04:09

import string
# 之前应该使用过这个库，不过已经忘记了什么时间使用过，最近一次使用时间(2018-04-13 13:45:26)
# 目的是参加一个Python Challenge的第1关，其中有一个字符串映射的过程，本来我是使用map/reduce解决的
# 转换后提示内容告诉我可以使用函数string.maketrans()建立转换表，但是这道题目的版本应该有点早
# Python3.4已经没有string.maketrans()了，取而代之的是内建函数: bytearray.maketrans()、bytes.maketrans()、str.maketrans()
# maketrans() 方法用于创建字符映射的转换表，对于接受两个参数的最简单的调用方式
# 第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。两个字符串的长度必须相同，为一一对应的关系
# 但是还有一点，我发现即使不使用import string，也可以调用函数str.maketrans()，现在还没弄明白原因。

import requests
# 从开始了解爬虫时接触了这个库，对于发送get、post请求非常方便，最近一次使用时间是(2018-04-14 16:01:15)
# 目的是参加一个Python Challenge的第2关，其中有一步是为了获取网页内容所以引入了requests库，直接发送get请求
# response = requests.get(target_url)即可，获取内容直接response.content就能得到
# 之前还用urllib，不过相比较来说还是这个比较简单，不过需要单独安装pip install requests，限制大了一些
# requests 是用Python语言编写，基于 urllib，采用 Apache2 Licensed 开源协议的 HTTP 库。
# 它比 urllib 更加方便，可以节约我们大量的工作，完全满足 HTTP 测试需求。
# requests 的哲学是以 PEP 20 的习语为中心开发的，所以它比 urllib 更加 Pythoner。更重要的一点是它支持 Python3 哦！
#    Beautiful is better than ugly.(美丽优于丑陋)
#    Explicit is better than implicit.(清楚优于含糊)
#    Simple is better than complex.(简单优于复杂)
#    Complex is better than complicated.(复杂优于繁琐)
#    Readability counts.(重要的是可读性)

import urllib
from urllib.request import urlopen
from urllib.parse import urlencode
# 这个网络请求库接触较早，第一个图片爬虫就使用了这个库，当时还没有看过多少Python代码，基本上是刚接触Python的时候
# urllib模块是python自带的，直接调用就好，相比于requests来说的好处是不用安装，不过使用起来麻烦一点
# 在网上找到一篇比较python3 urllib和requests模块区别的文章https://www.cnblogs.com/znyyy/p/7868511.html，说的比较好
# 不过总体来说就是越方便的库，就越失去了灵活性，对于特殊情况不太好处理
# 
# urllib+正则：无第三方依赖
# requests+BeautifulSoup：library
# scrapy：框架
# 
# 从上往下抽象程度增加，方便程度增加。“路怎么走，你们自己选啊。”

import re
# 开始接触Python的时候就用过这个正则表达式库，不过总是一知半解，用的时候找到之前的代码一粘贴就结束了
# 结果今天（2018-04-16 17:04:17）在使用正则表达式解析网页（做python challenge）时把自己给坑了
# 原来我一直没弄清楚匹配函数的区别，导致我使用了re.match来匹配所有符合条件的子串，结果悲剧了，一直没结果
# 在此特别记录一下匹配函数的区别，防止以后再犯错误
# re.match(pattern, string[, flags]): 从首字母开始开始匹配，string如果包含pattern子串，则匹配成功，返回Match对象，
#   失败则返回None，若要完全匹配，pattern要以$结尾。
# 
# re.search(pattern, string[, flags]) : 若string中包含pattern子串，则返回Match对象，否则返回None，
#   注意，如果string中存在多个pattern子串，只返回第一个。
# 
# re.findall(pattern, string[, flags]): 返回string中所有与pattern相匹配的全部字串，返回形式为数组。
# 
# re.finditer(pattern, string[, flags]): 返回string中所有与pattern相匹配的全部字串，返回形式为迭代器。

import pickle
# 这个库我确信之前没有用过，今天（2018-04-25 20:20:20）参加python challenge时第一次使用，
# 结果发现很早以前就在python教程里看过了！这个库的作用是对python对象进行序列化，序列化之后就可以保存到文件，
# 同时可以通过反序列化将文件中内存重新还原成与原来的对象，之前看这个库的时候肯定只是看看，没有写代码，要不然不能
# 一点印象也没有，反序列化的函数有pickle.load(file)和pickle.loads(bytes)，前者的参数是一个打开的文件，而后者就是
# 一个bytes数组，比如request返回的对象content，配合使用可以直接将网络资源反序列化

import zipfile
# 这个库确实是我第一次使用，今天（2018-05-02 12:11:59）参加python challenge用来解压一个zip文件
# 其实这个库除了解压还有很多其他的操作，都是关于zip文件的，参考https://www.cnblogs.com/sun-haiyu/p/7082063.html
# 最常用法：zip_file = zipfile.ZipFile('channel.zip') 打开zip文件
# zip_file.extractall('./channel')将zip文件全部解压到目录'./channel'中

import bz2
# 前几天使用了zip压缩文件，今天（2018-05-04 16:30:12）又接触到了新的压缩类型bz2，这是一种常用的压缩格式
# 同样是在进行python challenge时使用到的，根据我的推断应该是压缩的字节流起始字节是BZ，因为我解压的两个bytes都是这样的
# 
#    username_bytes = b'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084'
#    password_bytes = b'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08'
#    
#    print("username:", bz2.decompress(username_bytes))
#    print("password:", bz2.decompress(password_bytes))
# 
# 使用非常方便，直接调用方法decompress，将需要解压的内容传入即可
# 在python challenge第8关，使用到了bz2，并且写了一个函数str2bytes，用来解决将文件中的BZh91AY&SYA\xaf\x82\r字符串，转成16进制
# 原来花费了很多时间都没有搞定，这次自定义实现了
# 
# def str2bytes(str_content):
#    result_list = [];
#    pos = 0
#    str_content = str_content.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
#    content_len = len(str_content)
#    while pos < content_len:
#        if str_content[pos] == '\\' and pos + 3 < content_len and str_content[pos + 1] == 'x':
#            sub_str = str_content[pos + 2: pos + 4]
#            result_list.append(int(sub_str, 16))
#            pos = pos + 4
#        else:
#            result_list.append(ord(str_content[pos]))
#            pos = pos + 1
#    return bytes(result_list)

