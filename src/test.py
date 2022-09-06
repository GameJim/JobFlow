import logging
# class JobFactory:
#     # 所有的工场管理器
#     instance = None
#     d = []
#     def __init__(self):
#         self.name = None
#         self.Jobs = None
#
#         self._define()
#         if(self.instance != JobFactory.instance):
#             JobFactory.d.append(self.instance)
#         #
#         # #构造函数会注册此类
#         # JobFactory.appendParmFactory(self)
#
#     def __new__(cls, *args, **kwargs):
#         if cls.instance == None:
#             cls.instance = object.__new__(cls)
#         return cls.instance
#
#
#     def _define(self):
#         return False
#
# class BaseJobFactory(JobFactory):
#     instance = None
#
#     def _define(self):
#         return True
#
#     def __new__(cls, *args, **kwargs):
#         if cls.instance == None:
#             cls.instance = object.__new__(cls)
#         return cls.instance
#
# jf = JobFactory()
# print(jf)
#
# jf2 = BaseJobFactory()
# print(jf2)
#
# jf3 = BaseJobFactory()
# print(jf3)
#
# print(jf)
# print(jf._define())
# print(jf2._define())
# print(jf3._define())
#
# print(len(JobFactory.d))

# import osJob
# from param import paramFactory as pf
# from job import jobFactory as jf
# from jobFlow import JobFlow

# jobflow = JobFlow()
#
# rp_job = jf.createJob('file_c')
# src = pf.createParam('PATH_ABS')
# dst = pf.createParam('STRING')
# rp_rule = pf.createParam('OS_CUSTOM_RR')
# rp_rule.setValue(osJob.ReplaceRule.REPLACE_RULE_SRC)
#
# src.setValue('D:\\workspace\\code\\GEarth\\GEarth\\include')
# dst.setValue('E:\data\\dst')
#
# jobflow.addParam(dst)
# jobflow.addParam(src)
# jobflow.addParam(rp_rule)
#
# rp_job.bindInputParam('rp_rule', rp_rule)
# rp_job.bindInputParam('src', src)
# rp_job.bindInputParam('dst', dst)
#
# rp_job.setDefaultValue('match_rule', osJob.MatchRule.MATCH_RULE_NAME_EXT)
# rp_job.setDefaultValue('match_str','(.*)\.h')
# jobflow.addJob(rp_job)
#
# jobflow.start()


# from enum import StrEnum
# class MatchRule(StrEnum):
#     # 将内容拷贝至另一个文件夹目录
#     MATCH_RULE_NONE = 'MATCH_RULE_NONE'
#     MATCH_RULE_NAME_ALL = 'MATCH_RULE_NAME_ALL'  #文件名称
#     MATCH_RULE_EXT_ALL = 'MATCH_RULE_EXT_ALL'   #文件后缀
#     MATCH_CONTEXT_RE_ALL = 3 #基于文件内容
#
#     #只允许第一层
#     MATCH_RULE_NAME_FIRST = 1  #文件名称
#     MATCH_RULE_EXT_FIRST = 2  #文件后缀
#     MATCH_CONTEXT_RE_FIRST = 6 #基于文件内容
#
#
# k = MatchRule.MATCH_RULE_NAME_FIRST
# print(k.value)
# print(MatchRule.MATCH_RULE_NAME_ALL.name)


# import re
# print(re.match('(.*)\.png','ssd.png'))


# class Callback:
#     def __init__(self):
#         addCall =[]
#         removeCall = []
#
#     def addSetCall(self,func):
#         self.addSetCall(func)
#
# class B:
#     def call(self):
#         print("被回调")

from param import paramFactory
import osJob
from job import jobFactory

job = jobFactory.create('pathMerge')

base = paramFactory.create('aPath')
base.setValue('E:/data')

rPath = paramFactory.create('rPath')
rPath.setValue('src/1/b.txt')

job.bindInputParam('base', base)
job.bindInputParam('path_r', rPath)

job.work()

