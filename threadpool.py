#!/usr/bin/python
#-*- coding: utf-8 -*-

#/***************************************************************************
#* 
#* Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#* 
#**************************************************************************/
"""
This module is a threadpool with message queue

 * @file threadpool.py
 * @author zhongzhiwei01(com@baidu.com)
 * @date 2014/07/28 10:46:33
 * @brief 
 * 
"""

import Queue
import threading


class ThreadPool(object):
    """
    The thread pool class.
    """
    def __init__(self, thread_num):
        self.task_queue = Queue.Queue()
        self.thread_pool = []
        self.init_thread_pool(thread_num)

    def init_thread_pool(self, thread_num):
        """
        Initialize the thread pool.
        """
        for t in range(0, int(thread_num)):
            self.thread_pool.append(Work(self.task_queue))

    def add_job(self, func, *args, **kargs):
        """
        Add work job to the thread pool.
        """
        self.task_queue.put((func, args, kargs))

    def wait_completion(self):
        """
        Wait for the completion of all the tasks in the task queue.
        """
        self.task_queue.join()


class Work(threading.Thread):
    """
    Work    - do the real job, execute the task in the task queue.

    Attributes:
        work_queue:the real work queue.
    """
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.task_queue = task_queue
        self.start()

    def run(self):
        """
        the get-some-work, do-some-work main loop of worker threads.
        """
        while True:
            fun, args, kargs = self.task_queue.get()
            fun(*args, **kargs)
            self.task_queue.task_done()


