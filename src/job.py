#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 16:51
# @Author  : 我的名字
# @File    : job.py
# @Description :
import logging
from param import Callback, uuid, paramFactory, Param


# job工厂
class JobFactory:
    # 所有的工场管理器
    jobFactory = None

    # 注册参数类型
    def register(self, name, create):
        self.jobTemplate[name] = create

    def create(self, name):
        if name not in self.jobTemplate:
            logging.critical("没有此类型变量")
            return None
        else:
            return self.jobTemplate[name]()

    def __new__(cls, *args, **kwargs):
        if cls.jobFactory is None:
            cls.jobFactory = object.__new__(cls)
        return cls.jobFactory

    def __init__(self):
        self.jobTemplate = {}


# 注册此对象
jobFactory = JobFactory()


# 基础类
class Job:
    @staticmethod
    def create():
        return None

    name = 'base'
    # 注册对象
    jobFactory.register(name, create.__get__(object))

    # 给参数更新增加的回调：参数值更新时出发，自己内部实用
    class ParamValueCallback(Callback):
        def __init__(self, job, key):
            super().__init__()
            self.job = job
            self.key = key

        def call(self):
            logging.info(str(self.job.uid) + '成员' + self.key + '参数成功修改')
            if self.job.try_work:
                self.job.work()

    class ParamDelCallback(Callback):
        def __init__(self, job, key):
            super().__init__()
            self.job = job
            self.key = key

        def call(self):
            # 解绑列表
            self.job.unbindInputParam(self.key)

    def __init__(self):
        # 固定参数
        # id
        self.uid = uuid.uuid1()
        # 输入参数，需要绑定
        self.inputParams = {}
        # 输出参数
        self.outputParams = {}

        # 需子类定义在_init定义
        self.try_work = False
        # 输入参数类型
        self.inputParamType = {}
        # 默认参数
        self.defaultInput = {}
        # 输出参数
        self.outputParamsType = {}

        # 绑定的回调函数
        self.callbacks = {'start': [], 'end': [], 'del': [], 'bind': [], 'paramValue': {}, 'paramDel': {}}

        # 定义参数
        self._init()

        # 自动构建
        self.build()

    def destroy(self):
        # 触发销毁的回调函数
        for callback in self.callbacks['del']:
            callback.call()

        # 移除自己给绑定参数成语添加的回调函数
        for key, param in self.inputParams.items():
            if self.inputParams[key] and self.inputParams[key] != self.defaultInput[key]:
                self.unbindInputParam(key)

        # 删除自己所对应输出参数
        for key, param in self.outputParams.items():
            value = self.outputParams[key]
            self.outputParams[key].destory()
            self.outputParams[key] = None


    def removeCallback(self, callback, callback_type):
        if callback_type not in self.callbacks:
            logging.error("移除回调函数失败：job中不存在" + callback_type + "类型回调函数")
        else:
            if callback_type == 'param':
                logging.error("移除内置回调函数失败！")
                return
            else:
                self.callbacks[callback_type].remove(callback)


    def addCallback(self, callback, callback_type):
        if callback_type == 'param':
            logging.critical('添加内置回调失败')
            return

        if callback_type not in self.callbacks:
            self.callbacks[callback_type] = []
        self.callbacks[callback_type].append(callback)

    def build(self):
        # 创建输出参数
        for key, param_type in self.outputParamsType.items():
            # 此类参数隶属于Job
            if isinstance(param_type, list):
                self.outputParams[key] = paramFactory.create('rangeList')
                self.outputParams[key].setTypeList(param_type)
            else:
                self.outputParams[key] = paramFactory.create(param_type)

        # 创建默认参数和回调函数
        for key, param_type in self.inputParamType.items():
            self.inputParams[key] = None
            if key not in self.defaultInput:
                if isinstance(param_type, list):
                    self.defaultInput[key] = paramFactory.create('rangeList')
                    self.defaultInput[key].setTypeList(param_type)
                else:
                    self.defaultInput[key] = paramFactory.create(param_type)

            self.callbacks['paramValue'][key] = Job.ParamValueCallback(self, key)
            self.callbacks['paramDel'][key] = Job.ParamDelCallback(self, key)



    def _init(self):
        return False

    # 执行任务
    def _work(self):
        return False

    def jobName(self):
        return Job.name

    def setDefaultValue(self, key, value):
        # 如果设置成功，则更新out
        return self.defaultInput[key].setValue(value)

    # 解绑某个输出key，移除参数更新回调和删除回调
    def unbindInputParam(self, key):
        if key in self.inputParams and self.inputParams[key] and self.inputParams[key] != self.defaultInput[key]:
            # 解除回调绑定
            self.inputParams[key].removeCallback(self.callbacks['paramValue'][key])
            self.inputParams[key].removeCallback(self.callbacks['paramDel'][key])
            self.inputParams[key] = None
        return

    def bindInputParam(self, key, param):
        if key in self.inputParamType:
            if (isinstance(self.inputParamType[key], list) and param.paramType() in self.inputParamType[key]) \
                    or param.paramType() == self.inputParamType[key]:

                if key in self.inputParams and param == self.inputParams[key]:
                    return

                # 解绑改输入
                self.unbindInputParam(key)
                #给当前参数添加回调
                preParam = self.inputParams[key]
                self.inputParams[key] = param
                if self.inputParams[key]:
                    self.inputParams[key].addCallback(self.callbacks['paramValue'][key], 'value')
                    self.inputParams[key].addCallback(self.callbacks['paramDel'][key], 'del')

                # 触发内置回调函数
                for callback in self.callbacks['bind']:
                    # 需要实现此方法
                    callback.call(key, preParam, param)
            else:
                logging.error('job:' + key + ',请检查参数类型')
        else:
            logging.error('job:' + str(self.uid) + ', 请检查参:' + key + '成员是否存在')

    def isReady(self):
        for key in self.inputParamType:
            if key in self.inputParams:
                if self.inputParams[key] is None and key in self.defaultInput:
                    continue
                elif self.inputParams[key].isValid():
                    continue
                else:
                    return False
            elif key in self.defaultInput:
                continue
            else:
                return False
        return True

    def work(self):
        if not self.isReady():
            logging.warning("job参数还未准备好" + str(self.uid))
            return False

        # 将变量修改为默认值
        for key, value in self.defaultInput.items():
            if key not in self.inputParams:
                # 不会绑定会回调函数
                self.inputParams[key] = value

        if 'start' in self.callbacks:
            for callback in self.callbacks['start']:
                callback.call()

        logging.info("开始执行任务：" + str(self.uid))
        state = self._work()
        # if state:
        #     for callback in self.callbacks:
        #         callback.call()
        logging.info("任务：" + str(self.uid) + "执行完毕！")

        if 'end' in self.callbacks:
            for callback in self.callbacks['end']:
                callback.call()
        return state

         

    # def _createParamCallback(self, c_type, key):
    #     if c_type == 'value':
    #         return self.ParamValueCallback(self, key)
    #     elif c_type == 'del':
    #         return self.ParamDelCallback(self, key)
    #     else:
    #         return None
    #
    # def getOrCreateParamCallback(self, key):
    #     r = {}
    #     for c_type, callbacks in self.paramCallback.items():
    #         if key in callbacks:
    #             r[c_type] = callbacks[key]
    #         r[key] = self._createParamCallback(c_type, key)
    #         self.paramCallback[c_type][key] = r[key]
    #     return r

# class JobFactory:
#     # 所有的工场管理器
#     instance = {}
#     factory = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.factory == None:
#             cls.factory = object.__new__(cls)
#         return cls.factory
#
#     # 定义容器
#     def regist(jobfactory):
#         if isinstance(jobfactory, JobFactory):
#             JobFactory.instance[jobfactory.name] = jobfactory
#         else:
#             logging.error('Job工厂注册失败')
#
#     def __init__(self):
#         self.name = None
#         self.jobs = None
#
#         self._define()
#
#         # 构造函数会注册此类
#         if self.name:
#             JobFactory.regist(self)
#
#     def _define(self):
#         return False
#
#     def _createJob(self, job_name):
#         return None
#
#     def createJob(self, job_name, factory_name=None) -> Job:
#         if factory_name is None:
#             for factory_name, jobFactory in JobFactory.instance.items():
#                 job = jobFactory._createJob(job_name)
#                 if job:
#                     #设置job的名称
#                     job.name = job_name
#                     return job
#             else:
#                 logging.error("创建Job" + job_name + "失败")
#                 return None
#
#         return JobFactory.instance[factory_name]._createJob(job_name)
#
#
# jobFactory = JobFactory()


# class WorkCallback(Callback):
#     def __init__(self, job_id, jf):
#         self.job_id = job_id
#         self.jf = jf
#
#     #尝试启动添加此任务
#     def call(self):
#         ##self.jf.try_job(self.jf)
#         print('任务结束')


# 当绑定参数对象发生变化时触发的更新回调
# 给外部实用
# class BindParamaCallback(Callback):
#     def __init__(self, job, key, pre, cur):
#         self.job = job
#         self.key = key
#         self.pre = pre
#         self.cur = cur
#     def call(self):
#         print(self.job.id + ":" + self.key + "绑定参数从" + str(self.pre) + "变为" + str(self.cur))
#
# class StartWorkCallback(Callback):
#     def __init__(self, job):
#         self.job = job
#
#     def call(self):
#         print("job:" + self.job.id + "开始执行")


# def removeParamCallback(self, key):
#     if type not in self.paramCallback:
#         logging.error("移除回调函数失败：job中不存在" + type + "类型内置回调函数")
#
#     r = {}
#     for t, callbacks in self.paramCallback.items():
#         if key in callbacks:
#             r[t] = callbacks[key]
#             callbacks.pop(key)
#     return r
