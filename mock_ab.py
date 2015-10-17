#!/usr/bin/env python
#-*- coding:gb18030 -*-

"""
@file mock_ab.py
@author zhongzhiwei01
@date 2015/10/15
@brief 
"""

import getopt
import os
import sys
import time
import urllib2

import threadpool


def usage():
    """
    @brief: 帮助信息
    """
    print Global.USAGE_INFO


class Global(object):
    """
    @brief: 全局宏变量定义
    """
    USAGE_INFO = """
        Usage: python mock_ab.py [OPTION] url_address
        模拟apache benchmark 进行网站压力测试

        OPTIONS:
            -n: 设置ab命令模拟请求的总次数
            -c: 设置ab命令模拟请求的并发数
            -H: 设置ab命令模拟浏览器头信息
            -h: 获取帮助信息
    """
    ERROR_NUM = 0


class MockAb(object):
    """
    @brief: 模拟ab功能类
    """
    def __init__(self, mock_info):
        self.input_params = mock_info
        self.request_number = 1
        self.concurrent_number = 1
        self.visit_header = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
        self.url_addr = None

    def parse_params(self):
        """
        @brief: 解析参数
        """
        if self.input_params.has_key('req_num'):
            self.request_number = self.input_params["req_num"]
        if self.input_params.has_key('conc_num'):
            self.concurrent_number = self.input_params["conc_num"]
        if self.input_params.has_key('header'):
            self.visit_header = self.input_params["header"]
        if self.input_params.has_key('url_addr'):
            self.url_addr = self.input_params["url_addr"]
        else:
            print "url is missing, please check your input!"
            return False
        return True

    def access_work(self, url):
        """
        @brief: 向指定的url网站发送
        Args:
            url: 发送请求的url地址
        """
        try:
            request = urllib2.Request(url)
            request.add_header('User-agent', self.visit_header)
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            Global.ERROR_NUM +=1

    def gen_report(self, used_time):
        """
        @brief: 生成报告
        """
        print "Server Hostname: ", self.url_addr
        print "Concurrency Level: ", self.concurrent_number
        print "Complete requests: ", self.request_number
        print "Failed requests: ", Global.ERROR_NUM
        print "Time taken for tests: ", used_time
        print "Time per request: ", used_time/int(self.request_number)
        print "Requests per second: ", int(self.request_number)/used_time
        

    def run(self):
        """
        @brief: 主流程调用函数
        """
        if not self.parse_params():
            return None
        print "Benchmarking %s (be patient)....." % self.url_addr
        start_time = time.time()
        self.thread_pool = threadpool.ThreadPool(self.concurrent_number)
        for i in range(int(self.request_number)):
            self.thread_pool.add_job(self.access_work, str(self.url_addr))
        self.thread_pool.wait_completion()
        end_time = time.time()
        used_time = end_time - start_time
        print "done"
        self.gen_report(used_time)


def main():
    """
    @brief: 主函数
    """
    short_args = "hc:n:H:"
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_args)
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    mock_info = {}
    for opt, val in opts:
        if opt == "-h":
            usage()
            sys.exit(0)
        elif opt == "-c":
            mock_info["conc_num"] = val
        elif opt == "-n":
            mock_info["req_num"] = val
        elif opt == "-H":
            mock_info["header"] = val
    if len(args) == 1:
        mock_info["url_addr"] = args[0]
        mock_aber = MockAb(mock_info)
        mock_aber.run()
    else:
        print "You must input your url address"
        usage()


if __name__ == "__main__":
    sys.exit(main())
