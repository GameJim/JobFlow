#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 16:12
# @Author  : 管理器
# @File    : jobFlow.py
# @Description :

from enum import IntEnum
from queue import Queue
import logging
import uuid
import threading


class JobFlow:
    def __init__(self):
        self.uid = uuid.uuid1()

        self.params = {}
        self.jobs = {}

        self.state = False
        self.thread = None

        # 任务队列
        self.jobQueue = Queue()

        # 回调函数param job  del
        self.callbacks = {'start': [], 'stop': [], 'cancel': [], 'del': [], 'addParam': [], 'removeParam': [], \
                          'addJob': [], 'removeJob': []}


    def destory(self):
        for callback in self.callbacks['del']:
            callback.call()

        #移除所有数据
        self.params = {}
        self.jobs = {}

    def addCallback(self, callback, callback_type=None):
        if callback_type not in self.callbacks:
            self.callbacks[callback_type] = []
        self.callbacks[callback_type].append(callback)

    def removeCallback(self, callback, callback_type=None):
        if callback_type not in self.callbacks:
            logging.error("JobFlow移除任务失败")
        self.callbacks[callback_type].remove(callback)

    def addParam(self, param):
        # 保证不会出现重复的
        self.params[param.uid] = param
        for callback in self.callbacks['addParam']:
            callback.call(param)

    def addJob(self, job):
        # 保证不会出现重复的
        self.jobs[job.uid] = job
        job.jf = self

        for callback in self.callbacks['addJob']:
            callback.call(job)

    def removeParam(self, param):
        # 保证不会出现重复的
        self.params.remove(param)
        for callback in self.callbacks['removeParam']:
            callback.call(param)

    def removeJob(self, job):
        # 保证不会出现重复的
        self.removeJob.remove(job)
        for callback in self.callbacks['removeJob']:
            callback.call(job)

    def startJobs(self, endJobs):
        logging.info("****************************************************")
        logging.info("开始执任务流：" + str(self.uid))

        while not self.jobQueue.empty() and self.state is True:
            job = self.jobQueue.get()
            # 取出工作，如果工作准备ok，则执行工作
            if job.uid in endJobs:
                continue

            if job.isReady():
                job.work()
            else:
                self.put(job)  # 后面再执行任务

        logging.info("任务流：" + str(self.uid) + "执行完毕")
        logging.info("****************************************************")
        self.state = False
        self.thread = None

    def start(self, startJobs=[], endJobs=[]):
        # 将所有任务标记为自动启动
        self.state = True
        for job in self.jobs:
            job.try_work = True

        # 创建任务池，构成任务优先队列,如果没有待执行任务，则收集任务池
        if self.jobQueue is None or self.jobQueue.empty():
            self.jobQueue = Queue()
            if (len(startJobs)) > 0:
                for job_id in startJobs:
                    self.jobQueue.put(self.jobs[job_id])
            else:  # 遍历查找所有准备ok的job
                for job_id, job in self.jobs.items():
                    if job.isReady():
                        self.jobQueue.put(job)

        if self.thread is None:
            self.thread = threading.Thread(name='t1', target=JobFlow.startJobs, args=(self, endJobs), daemon=False)
            self.thread.start()
        else:
            logging.info("正在执行任务！")

        for callback in self.callbacks['start']:
            callback.call()

        return True

    def stop(self):
        self.state = False
        for job in self.jobs:
            job.try_work = False
        for callback in self.callbacks['stop']:
            callback.call()

    def cancel(self):
        self.state = False
        for job in self.jobs:
            job.try_work = False
        self.jobQueue = None
        for callback in self.callbacks['cancel']:
            callback.call()
