#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2019-9-29 14:52:44
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : draw extra line on a candle

import datetime
import numpy as np
import pandas as pd
import tushare as ts
import mpl_finance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
from matplotlib.ticker import Formatter
from enum import Enum

# 继承枚举类
class relation_type(Enum):
    NONE  = 0
    UP    = 1
    DOWN  = 3
    OPEN  = 4
    CLOSE = 5

# print(relation_type.OPEN)


stock_code = '600588'

def get_relation(pre_data, cur_data):
    if pre_data == None or cur_data == None:
        return relation_type.NONE
    elif cur_data[0] >= pre_data[0] and cur_data[1] >= pre_data[1]:
        return relation_type.UP
    elif cur_data[0] < pre_data[0] and cur_data[1] < pre_data[1]:
        return relation_type.DOWN
    elif cur_data[0] <= pre_data[0] and cur_data[1] >= pre_data[1]:
        #print(cur_data[0], pre_data[0], cur_data[1], pre_data[1])
        return relation_type.OPEN
    elif cur_data[0] >= pre_data[0] and cur_data[1] <= pre_data[1]:
        return relation_type.CLOSE
    else:
        return relation_type.NONE

def analyze_tendency(low_list, high_list):
    pre_relation = relation_type.UP
    pre_data = (low_list[0], high_list[0])
    xlist = [0]
    ylist = [low_list[0] / 2 + high_list[0]/ 2]

    item_count = len(low_list)
    for n in range(item_count):
        ret_relation = get_relation(pre_data, None if n + 1== item_count else (low_list[n+1], high_list[n+1]))
        #print("real--------------->", ret_relation)
        if ret_relation == relation_type.NONE:
            break
        elif ret_relation == relation_type.UP or ret_relation == relation_type.DOWN:
            next_data = (low_list[n+1], high_list[n+1])

        elif ret_relation == relation_type.OPEN:
            if pre_relation == relation_type.UP:
                next_data = (low_list[n], high_list[n+1])
            else:
                next_data = (low_list[n+1], high_list[n])
            ret_relation = pre_relation
        elif ret_relation == relation_type.CLOSE:
            if pre_relation ==  relation_type.UP:
                next_data = (low_list[n+1], high_list[n])
            else:
                next_data = (low_list[n], high_list[n+1])
            ret_relation = pre_relation

        if ret_relation != pre_relation:
            xlist.append(n)
            ylist.append(pre_data[1] if pre_relation == relation_type.UP else pre_data[0])

        pre_data = next_data
        pre_relation = ret_relation
        #print(pre_relation, n)

    xlist.append(item_count - 1)
    ylist.append(high_list[item_count - 1] if pre_relation == relation_type.UP else low_list[item_count - 1])

    plt.plot(xlist, ylist, color='r')
    print(xlist)
    print(ylist)
    print(item_count)

def update_stock_data():
    df = ts.get_hist_data(stock_code, ktype='5')
    df.to_csv(stock_code+'.csv', columns=['open','high','low','close'])

def draw_candle():
    csv_data = pd.read_csv(stock_code+'.csv', low_memory = False) #防止弹出警告
    dfcvs = pd.DataFrame(csv_data)
    dfcvs.sort_values(by='date', ascending=True, inplace=True)

    interval_quotes = [tuple([i]+list(quote[1:])) for i,quote in enumerate(dfcvs.values)]
    date_quotes = dfcvs.date.values;
    high_quotes = dfcvs.high.values;
    low_quotes = dfcvs.low.values;
    # print(interval_quotes)
    # print(date_quotes)
    # print(low_quotes)
    # print(high_quotes)

    fig, ax = plt.subplots(figsize=(800/72, 450/72))
    fig.subplots_adjust(bottom=0.1)
    mpf.candlestick_ohlc(ax, interval_quotes, colordown='#F5F5F5', colorup='#DCDCDC', width=0.2, alpha=1)

    # #https://matplotlib.org/examples/pylab_examples/date_index_formatter.html
    class MyFormatter(Formatter):
        def __init__(self, fmt='%Y-%m-%d %H:%M'):
            self.fmt = fmt

        def __call__(self, x, pos=0): #x就是x轴的刻度数值，但是是浮点数
            if x<0 or x>=len(date_quotes):
                return ''
            return date_quotes[int(x)][:-3] # slice seconds

    # set xaxix format
    formatter = MyFormatter(date_quotes)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(len(date_quotes)//4)) # 根据数据量控制间隔

    for label in ax.get_xticklabels():
        #label.set_rotation(45)
        label.set_horizontalalignment('center')

    analyze_tendency(low_quotes, high_quotes);
    #plt.plot([0,10,15], [31.25,31.6,31.3], color='r')
    plt.show()


if __name__ == '__main__':
    #update_stock_data()
    draw_candle()