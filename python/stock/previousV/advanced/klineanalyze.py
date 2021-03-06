#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2019-10-3 10:13:03
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : analyze k line relation and smooth 

from klinerelation import relation_type
from klinerelation import get_relation

def tendency(low_list, high_list):
    xlist = []
    ylist = []
    pre_relation = relation_type.UP
    pre_data = (low_list[0], high_list[0])
    next_data = (0, 0)
    pre_n = 0
    next_n = 0

    item_count = len(low_list)
    for n in range(item_count):
        ret_relation = get_relation(pre_data, None if n + 1== item_count else (low_list[n+1], high_list[n+1]))
        contain_relation = relation_type.NONE
        #print("real--------------->", ret_relation)
        if ret_relation == relation_type.NONE:
            break
        elif ret_relation == relation_type.UP or ret_relation == relation_type.DOWN:
            next_data = (low_list[n+1], high_list[n+1])
            next_n = n+1

        elif ret_relation == relation_type.OPEN:
            if pre_relation == relation_type.UP:
                next_data = (low_list[n], high_list[n+1])
                next_n = n+1
            else:
                next_data = (low_list[n+1], high_list[n])
                next_n = n+1
            contain_relation = ret_relation
            ret_relation = pre_relation
        elif ret_relation == relation_type.CLOSE:
            if pre_relation ==  relation_type.UP:
                next_data = (low_list[n+1], high_list[n])
                next_n = n
            else:
                next_data = (low_list[n], high_list[n+1])
                next_n = n
            contain_relation = ret_relation
            ret_relation = pre_relation

        #print(n, ret_relation, contain_relation)

        if ret_relation != pre_relation:
            if n == 0:
                xlist.append(n)
                ylist.append(high_list[0])
            else:
                xlist.append(pre_n)
                ylist.append(pre_data[1] if pre_relation == relation_type.UP else pre_data[0])
        elif n == 0:
            xlist.append(n)
            ylist.append(low_list[0])

        pre_data = next_data
        pre_relation = ret_relation
        pre_n = next_n
        #print(pre_relation, n)

    xlist.append(item_count - 1)
    ylist.append(high_list[item_count - 1] if pre_relation == relation_type.UP else low_list[item_count - 1])

    return xlist, ylist

def add2smoothpath(retlistx, retlisty, x, y):
    retlistx.append(x)
    retlisty.append(y)
    return x, y

def smooth(xlist, ylist):
    listlen = len(xlist)
    retlistx = []
    retlisty = []

    if listlen > 0:
        prex, prey = add2smoothpath(retlistx, retlisty, xlist[0], ylist[0])

    n = 1
    while n < listlen:
        if n == listlen - 1:
            prex, prey = add2smoothpath(retlistx, retlisty, xlist[n], ylist[n])
        elif xlist[n] - prex >= 7:
            if n+2 < listlen:
                if (ylist[n] - prey)*(ylist[n+2] - ylist[n]) > 0: # tendency continue
                    n += 1
                # elif n+4 < listlen and (ylist[n] - prey)*(ylist[n+4] - ylist[n]) > 0 : # tendency continue
                #     n += 1
                else:
                    prex, prey = add2smoothpath(retlistx, retlisty, xlist[n], ylist[n])
            else: 
                prex, prey = add2smoothpath(retlistx, retlisty, xlist[n], ylist[n])
        elif xlist[n+1] - xlist[n] < 3:
            n += 1
        elif xlist[n] - prex <= 2 and prex != xlist[0]: # ingore start point
            n += 1
        else:
            prex, prey = add2smoothpath(retlistx, retlisty, xlist[n], ylist[n])
        n += 1
    return retlistx, retlisty

if __name__ == '__main__':
    pass