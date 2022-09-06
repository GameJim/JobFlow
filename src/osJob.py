from job import jobFactory, Job
import shutil, os, logging


class PathMerge(Job):
    @staticmethod
    def create():
        return PathMerge()

    name = 'pathMerge'
    # 注册对象
    jobFactory.register(name, create.__get__(object))

    def _init(self):
        # 定义
        self.inputParamType['base'] = ['aPath']
        self.inputParamType['path_r'] = ['rPath']

        self.outputParamsType['result'] = ['aPath']

        return True

    def _work(self):
        path = os.path.join(self.inputParams['base'].value, self.inputParams['path_r'].value)
        return self.outputParams['result'].setValue(path)

    def jobName(self):
        return PathMerge.name








# from job import JobFactory, Job
# from param import ParamFactory, Param, paramFactory
# from enum import IntEnum
# import shutil, os, logging
# import re
# from stat import ST_ATIME, ST_CTIME, ST_MTIME
#
# class ReplaceRule(IntEnum):
#     REPLACE_RULE_SRC = 1  # 直接使用源进行替换
#     REPLACE_RULE_LATEST = 2  # 保留最新的文件
#     REPLACE_RULE_OLD = 3  # 保留久版本
#
#
# class CopyRule(IntEnum):
#     # 将内容拷贝至另一个文件夹目录
#     COPY_RULE_DIFF = 1
#     COPY_RULE_REPLACE = 2
#     COPY_RULE_ALL = 3
#
#
# class MatchRule(IntEnum):
#     # 将内容拷贝至另一个文件夹目录
#     MATCH_RULE_NONE = 100,  # 文件名称
#     MATCH_RULE_NAME = 1,  # 文件名称
#     MATCH_RULE_EXT = 2,  # 文件后缀
#     MATCH_RULE_NAME_EXT = 3  # 文件夹里的内容
#     MATCH_RULE_CONTEXT = 4  # 文件内容
#
#
# def _checkFile(file_path, match_rule=None, match_str=None):
#     s = None
#     if match_rule == None or match_str == None or match_rule == MatchRule.MATCH_RULE_NONE:
#         return True
#     elif match_rule == MatchRule.MATCH_RULE_NAME:
#         s = os.path.basename(file_path)
#     elif match_rule == MatchRule.MATCH_RULE_EXT:
#         s = os.path.splitext(file_path)[1]
#     elif match_rule == MatchRule.MATCH_RULE_NAME_EXT:
#         s = os.path.basename(file_path) + os.path.splitext(file_path)[1]
#     elif match_rule == MatchRule.MATCH_RULE_CONTEXT:
#         logging.critical("匹配文本内容暂为实现")
#     r = re.match(match_str, s)
#     if r:
#         return True
#     return False
#
#
# class IOParamFactory(ParamFactory):
#     factory = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.factory == None:
#             cls.factory = object.__new__(cls)
#         return cls.factory
#
#     def _define(self):
#         self.name = 'io'
#         self.param_types = ['OS_CUSTOM_RR', 'OS_CUSTOM_CR', 'OS_CUSTOM_MR']
#
#     def _createParam(self, param_type):
#         return Param(param_type, self)
#
#     def _checkParam(self, param_type, param):
#         if param_type == 'OS_CUSTOM_RR':
#             return isinstance(param, ReplaceRule)
#         elif param_type == 'OS_CUSTOM_CR':
#             return isinstance(param, CopyRule)
#         elif param_type == 'OS_CUSTOM_MR':
#             return isinstance(param, MatchRule)
#         return False
#
#
# paramFactory = IOParamFactory()
#
#
# class OSJobFactory(JobFactory):
#     factory = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.factory == None:
#             cls.factory = object.__new__(cls)
#         return cls.factory
#
#     def _define(self):
#         self.name = 'os'
#         self.jobs = ['file_r', 'file_c', 'file_pick', 'path_m', 'cmd']
#
#     def _copyFileDiff(source, target, level=None, match_rule=None, match_str=None):
#         if level is not None and level == 0:
#             return
#
#         if os.path.isdir(source) and os.path.isfile(target):
#             return
#
#         # 都是文件夹递归替换
#         if os.path.isdir(source) and os.path.isdir(target):
#             file = os.listdir(source)
#             for f in file:
#                 sub_s_path = os.path.join(source, f)
#                 sub_d_path = os.path.join(target, f)
#
#                 sublevel = level
#                 if sublevel is not None:
#                     sublevel = sublevel - 1
#
#                 if os.path.isdir(sub_s_path) and not os.path.exists(sub_d_path):
#                     os.mkdir(sub_d_path)
#
#                 OSJobFactory._copyFileDiff(sub_s_path, sub_d_path, sublevel, match_rule, match_str)
#             return
#
#         if os.path.isfile(source) and os.path.exists(target):
#             return
#         try:
#             # 进行规则检测
#             if not _checkFile(source, match_rule, match_str):
#                 return
#
#             shutil.copy(source, target)
#
#             # 关键步骤:保留修改时间,ST_MTIME:修改时间,ST_CTIME:文件访问时间,windows下
#             file_stat = os.stat(source)
#             os.utime(target, (file_stat[ST_CTIME], file_stat[ST_MTIME]))
#
#         except IOError as e:
#             print("Unable to copy file. %s" % e)
#         except:
#             print("Unexpected error")
#
#     def _replaceFile(source, target, rp_rule, level=None, match_rule=None, match_str=None):
#         if level is not None and level == 0:
#             return
#         # w文件夹 到 文件
#         if os.path.isdir(source) and os.path.isfile(target):
#             return
#
#         if os.path.exists(target) is False:
#             return
#
#         # 都是文件夹递归替换
#         if os.path.isdir(source) and os.path.isdir(target):
#             file = os.listdir(source)
#             sublevel = level
#             if sublevel is not None:
#                 sublevel = sublevel - 1
#
#             for f in file:
#                 real_url = os.path.join(source, f)
#                 OSJobFactory._replaceFile(real_url, os.path.join(target, f), sublevel, rp_rule, sublevel)
#             return
#
#         # 文件和文件夹
#         if os.path.isdir(target):
#             name = os.path.basename(source)
#             target = os.path.join(target, name)
#             OSJobFactory._replaceFile(source, target, rp_rule)
#             return
#
#         # 文件 和 文件
#         if rp_rule == ReplaceRule.REPLACE_RULE_SRC:
#             # 进行规则检测
#             if not _checkFile(source, match_rule, match_str):
#                 return
#             try:
#                 shutil.copy(source, target)
#                 # 关键步骤:保留修改时间,ST_MTIME:修改时间,ST_CTIME:文件访问时间,windows下
#                 file_stat = os.stat(source)
#                 os.utime(target, (file_stat[ST_CTIME], file_stat[ST_MTIME]))
#             except IOError as e:
#                 print("Unable to copy file. %s" % e)
#             except:
#                 print("Unexpected error")
#         elif rp_rule == ReplaceRule.REPLACE_RULE_LATEST:
#             try:
#                 modify_time_src = os.path.getmtime(source)
#                 modify_time_target = os.path.getmtime(target)
#                 if modify_time_target >= modify_time_src:
#                     return
#                 else:
#                     shutil.copy(source, target)
#             except:
#                 logging.critical("failed to replace file")
#
#     def _createJob(self, job_name):
#         if job_name not in self.jobs:
#             return None
#         if job_name == 'file_r':
#             return self.ReplaceFile()
#         elif job_name == 'file_c':
#             return self.CopyFile()
#         elif job_name == 'path_m':
#             return self.PathMerge()
#         elif job_name == 'cmd':
#             return None
#
#     class ReplaceFile(Job):
#         def _init(self):
#             # 定义
#             self.inputParamType['src'] = ['PATH_ABS', 'PATH_REL']
#             self.inputParamType['dst'] = ['PATH_ABS', 'PATH_REL', 'STRING']
#             self.inputParamType['rp_rule'] = 'OS_CUSTOM_RR'
#
#             self.inputParamType['match_rule'] = ['OS_CUSTOM_MR']
#             self.inputParamType['match_str'] = 'STRING'
#
#             # 设置默认值
#             self.defaultInput['rp_rule'] = paramFactory.createParam(self.inputParamType['rp_rule'])
#             self.defaultInput['rp_rule'].setValue(ReplaceRule.REPLACE_RULE_LATEST)
#
#             # 设置默认值
#             self.defaultInput['match_rule'] = paramFactory.createParam(self.inputParamType['match_rule'])
#             self.defaultInput['match_rule'].setValue(MatchRule.MATCH_RULE_NONE)
#             # 设置默认值
#             self.defaultInput['match_str'] = paramFactory.createParam(self.inputParamType['match_str'])
#             self.defaultInput['match_str'].setValue('*')
#             return True
#
#         def _work(self):
#             OSJobFactory._replaceFile(self.inputParams['src'].value, self.inputParams['dst'].value, \
#                                       self.inputParams['rp_rule'].value)
#             return True
#
#     class CopyFile(Job):
#         def _init(self):
#             # 定义
#             self.inputParamType['src'] = ['PATH_ABS', 'PATH_REL']
#             self.inputParamType['dst'] = ['PATH_ABS', 'PATH_REL', 'STRING']
#             self.inputParamType['rp_rule'] = ['OS_CUSTOM_RR']
#             self.inputParamType['cp_rule'] = ['OS_CUSTOM_CR']
#             self.inputParamType['sub'] = ['BOOL']
#
#             self.inputParamType['match_rule'] = ['OS_CUSTOM_MR']
#             self.inputParamType['match_str'] = 'STRING'
#
#             # 设置默认值
#             self.defaultInput['rp_rule'] = paramFactory.createParam(self.inputParamType['rp_rule'])
#             self.defaultInput['rp_rule'].setValue(ReplaceRule.REPLACE_RULE_LATEST)
#             # 设置默认值
#             self.defaultInput['match_rule'] = paramFactory.createParam(self.inputParamType['match_rule'])
#             self.defaultInput['match_rule'].setValue(MatchRule.MATCH_RULE_NONE)
#             # 设置默认值
#             self.defaultInput['match_str'] = paramFactory.createParam(self.inputParamType['match_str'])
#             self.defaultInput['match_str'].setValue(None)
#
#             # 设置默认值
#             self.defaultInput['cp_rule'] = paramFactory.createParam(self.inputParamType['cp_rule'])
#             self.defaultInput['cp_rule'].setValue(CopyRule.COPY_RULE_ALL)
#
#             # 设置默认值
#             self.defaultInput['sub'] = paramFactory.createParam(self.inputParamType['sub'])
#             self.defaultInput['sub'].setValue(False)
#             return True
#
#         def _work(self):
#             if not self.inputParams['sub'].value or not os.path.isdir(self.inputParams['src'].value):
#                 if CopyRule.COPY_RULE_REPLACE & self.inputParams['cp_rule'].value == CopyRule.COPY_RULE_REPLACE:
#                     OSJobFactory._replaceFile(self.inputParams['src'].value, self.inputParams['dst'].value, \
#                                               self.inputParams['rp_rule'].value, level=None, \
#                                               match_str=self.inputParams['match_str'].value,
#                                               match_rule=self.inputParams['match_rule'].value)
#                 if CopyRule.COPY_RULE_DIFF & self.inputParams['cp_rule'].value == CopyRule.COPY_RULE_DIFF:
#                     OSJobFactory._copyFileDiff(self.inputParams['src'].value, self.inputParams['dst'].value, level=None, \
#                                                match_str=self.inputParams['match_str'].value,
#                                                match_rule=self.inputParams['match_rule'].value)
#             else:  # 子文件夹形式
#                 if not os.path.isdir(self.inputParams['dst'].value):
#                     return
#
#
#                 name = os.path.basename(self.inputParams['src'].value)
#                 sub_path = os.path.join(self.inputParams['dst'].value, name)
#                 if not os.path.exists(sub_path):
#                     os.mkdir(sub_path)
#
#                 if CopyRule.COPY_RULE_REPLACE & self.inputParams['cp_rule'].value == CopyRule.COPY_RULE_REPLACE:
#                     OSJobFactory._replaceFile(self.inputParams['src'].value, sub_path, \
#                                               self.inputParams['rp_rule'].value, level=None, \
#                                               match_str=self.inputParams['match_str'].value,
#                                               match_rule=self.inputParams['match_rule'].value)
#                 if CopyRule.COPY_RULE_DIFF & self.inputParams['cp_rule'].value == CopyRule.COPY_RULE_DIFF:
#                     OSJobFactory._copyFileDiff(self.inputParams['src'].value, sub_path, level=None, \
#                                                match_str=self.inputParams['match_str'].value,
#                                                match_rule=self.inputParams['match_rule'].value)
#
#             return True
#
#     # 生成绝对路径
#     class PathMerge(Job):
#         def _init(self):
#             # 定义
#             self.inputParamType['base'] = ['PATH_ABS']
#             self.inputParamType['path_r'] = ['PATH_REL']
#
#             self.outputParamsType['path_a'] = ['PATH_ABS']
#
#             return True
#
#         def _work(self):
#             path = os.path.join(self.inputParamType['base'], self.inputParamType['path_r'])
#             return self.outputParams['path_a'].setValue(path)
#
#         # 生成绝对路径
#     # 提取文件到指定目录，替换规则
#     # class PickFile(Job):
#     #     def _createParams(self):
#     #         # 定义
#     #         self.inputParamatersType['src'] = ['PATH_ABS', 'PATH_REL', 'STRING']
#     #         self.inputParamatersType['dst'] = ['PATH_ABS', 'STRING']
#     #
#     #         self.inputParamatersType['rp_rule'] = ['OS_CUSTOM_RR']
#     #         self.inputParamatersType['cp_rule'] = ['OS_CUSTOM_CR']
#     #
#     #         self.inputParamatersType['match_rule'] = 'OS_CUSTOM_MR'
#     #         self.inputParamatersType['match_str'] = 'LIST'
#     #
#     #         # 设置默认值
#     #         self.defaultInput['match_rule'] = paramFactory.createParam(self.inputParamatersType['match_rule'])
#     #         self.defaultInput['match_rule'].setValue(MatchRule.MATCH_RULE_NAME_ALL)
#     #
#     #         # 设置默认值
#     #         self.defaultInput['rp_rule'] = paramFactory.createParam(self.inputParamatersType['rp_rule'])
#     #         self.defaultInput['rp_rule'].setValue(ReplaceRule.REPLACE_RULE_LATEST)
#     #
#     #         # 设置默认值
#     #         self.defaultInput['cp_rule'] = paramFactory.createParam(self.inputParamatersType['cp_rule'])
#     #         self.defaultInput['cp_rule'].setValue(CopyRule.COPY_RULE_ALL)
#     #
#     #         return True
#     #
#     #     def _work(self):
#     #         #创建数据存储的文件夹
#     #         if not os.path.exists(self.inputParamatersType['dst'].p_value):
#     #             os.makedirs(self.inputParamatersType['dst'].p_value)
#
#
# osJobFactory = OSJobFactory()
