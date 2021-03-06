#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2019-4-1 14:07:57
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : 在图标中设置中文内容

import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.arange(1, 18)
    y = 8*x + 7
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title("中文表头简单测试")
    plt.xlabel("x 轴")
    plt.ylabel("y 轴")

    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()