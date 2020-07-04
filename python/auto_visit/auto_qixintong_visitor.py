#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date     : 2020-7-1 22:49:35
# @Author   : Albert Shi
# @Link     : http://blog.csdn.net/albertsh
# @Github   : https://github.com/AlbertGithubHome
__author__ = 'AlbertS'
# @Subject  : 自动浏览网站

import os
import sys
import time
import random
import requests
import browsercookie
from lxml import etree
from queue import Queue
from threading import Thread

sys.path.append(os.path.abspath("../tools/network"))
from agentpool import agentpool
from proxypool import proxypool
#pip install -i https://pypi.doubanio.com/simple pysqlite

class qinxintong_visitor(object):
    def __init__(self, entry_url, user_cookies):
        self.main_url = entry_url
        self.top_target_list = []
        self.main_dir = ''
        self.max_proxy_count = 5
        self.proxy_queue = Queue()
        self.agentpool = agentpool()
        self.user_cookies = user_cookies
        self.proxy_pool_list = [proxypool('https://www.xicidaili.com/nn/', self.max_proxy_count),
            proxypool('https://www.xicidaili.com/nn/', self.max_proxy_count)]

    def collect_company_info(self, dom, cur_level):
        info_list = []
        val = dom.xpath('//*[@id="companyName"]/text()') # 公司名称
        info_list.append(val[0])

        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[1]/td[2]/a/text()') # 企业法人
        info_list.append(val[0].replace('\n', '').strip())
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[3]/td[1]/text()') # 企业类型
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[4]/td[1]/text()') # 注册资本
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[5]/td[1]/text()') # 成立日期
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[4]/td[2]/text()') # 经营状态
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[5]/td[2]/text()') # 核准日期
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[7]/td[1]/text()') # 统一社会信用代码
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[8]/td[1]/text()') # 工商注册号
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[7]/td[2]/text()') # 纳税人识别号
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[8]/td[2]/text()') # 组织机构代码
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[9]/td/text()') # 注册地址
        info_list.append(val[0])
        val = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tr[10]/td/text()') # 经营范围
        info_list.append(val[0])

        self.write_log("收集 [{0}级]【{1}】 详细信息...".format(cur_level, info_list[0] if info_list else ''))
        return info_list


    def collect_company_investment(self, dom, cur_level, parent_company):
        url_list = []
        with open(self.main_dir + '/company_invest_info_' + str(cur_level) +'.txt', 'a', encoding='UTF-8') as outfile:
            name_list = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[14]/table[1]/tr/td[2]/div/a/text()')          # 被投资企业名称
            rate_list = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[14]/table[1]/tr/td[4]/text()')                # 投资比例
            boss_list = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[14]/table[1]/tr/td[3]/a//text()')             # 企业法人
            next_level_url_list = dom.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[14]/table[1]/tr/td[2]/div/a/@href') # 网址
            for name, rate, boss, new_url in zip(name_list, rate_list, boss_list, next_level_url_list):
                next_level_url = self.main_url + new_url
                url_list.append(next_level_url)
                outfile.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(parent_company, name.replace('\n', ''), rate.replace('\n', '').strip(), boss, next_level_url))
                #print('{0}\t{1}\t{2}\t{3}\n'.format(company_name, name, rate, new_url))
        return url_list


    def looking_for_investment(self, cur_level, max_level, url_list):
        next_level_url_list = []
        with open(self.main_dir + '/company_detail_info_' + str(cur_level) +'.txt', 'a', encoding='UTF-8') as file:
            for url in url_list:
                headers = {'User-Agent': self.agentpool.get_random_user_agent(), 'Connection': 'keep-alive'}

                self.write_log('open {0}, level[{1}]\n'.format(url, cur_level), False)
                time.sleep(random.uniform(5.18, 17.26))

                response = requests.get(url, headers=headers, cookies=self.cookies, timeout=60)
                if response.status_code == 200:
                    dom = etree.HTML(response.text)
                    #self.write_log(response.text)
                    info_list = self.collect_company_info(dom, cur_level)
                    file.write('\t'.join(info_list) + '\n')

                    next_level_url_list = []
                    if cur_level < max_level:
                        next_level_url_list = self.collect_company_investment(dom, cur_level, info_list[0] if info_list else '')

        if cur_level <= max_level:
            self.looking_for_investment(cur_level + 1, max_level, next_level_url_list)

    def init_top_target_list(self):
        with open('./1levelcompany.txt', 'r', encoding='UTF-8') as file:
            self.top_target_list = file.read().strip().split('\n')
        self.write_log('一共 {0} 家企业，开始检索信息...\n'.format(len(self.top_target_list)));

    def write_log(self, str_info, console_show=True):
        with open(self.main_dir + '/runtime.log', 'a', encoding='UTF-8') as file:
            file.write(str_info + '\n')
        if console_show: print(str_info)

    def init_cookies(self):
        self.cookies = dict(map(lambda x:x.split('='), self.user_cookies.split(";")))

    def run(self):
        self.main_dir = time.strftime("%Y-%m-%d %H%M%S", time.localtime())
        os.makedirs(self.main_dir)
        self.init_top_target_list()
        self.init_cookies()
        self.looking_for_investment(1, 3, self.top_target_list)

if __name__ == '__main__':
    auto_visitor = qinxintong_visitor('https://www.qixintong.cn',
     'advert=1; utype=2; sessionid=1n6ic4ry8xt75mlr9vlf9z1my9e2g4wz; tel=15321905915')
    auto_visitor.run()
