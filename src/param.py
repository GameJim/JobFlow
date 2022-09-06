#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 15:33
# @Author  : 我的名字
# @File    : param.py
# @Description :

import logging
import uuid
from os import path

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


class ParamFactory:
    # 所有的工场管理器
    paramFactory = None

    # 注册参数类型
    def register(self, p_type, create):
        self.paramTemplate[p_type] = create

    def create(self, p_type):
        if p_type not in self.paramTemplate:
            logging.critical("没有此类型变量")
            return None
        else:
            return self.paramTemplate[p_type]()

    def __new__(cls, *args, **kwargs):
        if cls.paramFactory is None:
            cls.paramFactory = object.__new__(cls)
        return cls.paramFactory

    def __init__(self):
        self.paramTemplate = {}


# 注册此对象
paramFactory = ParamFactory()


class Callback:
    def __init__(self):
        self.uid = uuid.uuid1()
        self.bindFunc = None

    def bindFun(self, func):
        self.bindFunc = func

    def call(self):
        if self.bindFunc is not None:
            self.bindFunc()
        else:
            logging.critical("virtural callback")


class Param:
    @staticmethod
    def create():
        return None

    p_type = None
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def __init__(self):
        self.uid = uuid.uuid1()
        self.value = None
        # 参数值发生改变时del value
        self.callbacks = {'del': [], 'value': []}

    # 无资格销毁任何回调函数，不会主动创建回调函数成员
    def destroy(self):
        for callback in self.callbacks['del']:
            callback.call()

        self.value = None
        self.callbacks = None
        self.delCallbacks = None
        self.owner = None
        self.pf = None

    def paramType(self):
        return Param.p_type

    # 添加回调
    def addCallback(self, callback, cb_type='value'):
        if isinstance(callback, Callback):
            if cb_type == 'value':
                self.callbacks['value'].append(callback)
            elif cb_type == 'del':
                self.callbacks['del'].append(callback)
            else:
                logging('参数中加入未知回调函数')
                if cb_type not in self.callbacks:
                    self.callbacks[cb_type] = []
                self.callbacks['del'].append(callback)
        else:
            logging.error("参数回调函数添加失败，请检查回调函数类型")

    def removeCallback(self, callback):
        if isinstance(callback, Callback):
            for cb_type, callbacks in self.callbacks.items():
                if callback in callbacks:
                    callbacks.remove(callback)
                    return
        else:
            logging.error("参数回调函数移除失败，请检查回调函数类型")

    def checkValue(self, value) -> bool:
        return True

    def isValid(self) -> bool:
        return self.value is not None

    def setValue(self, value):
        if value is None or self.checkValue(value):
            self.value = value
            # 调用回调
            for callback in self.callbacks['value']:
                callback.call()
            return True
        else:
            logging.error('设置参数值失败:' + value)
            return False


# 定义其他类型
class IntParam(Param):
    @staticmethod
    def create():
        return IntParam()

    p_type = 'int'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if isinstance(value, int):
            return True
        return False

    def paramType(self):
        return IntParam.p_type


class BoolParam(Param):
    @staticmethod
    def create():
        return BoolParam()

    p_type = 'bool'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if isinstance(value, bool):
            return True
        return False

    def paramType(self):
        return BoolParam.p_type


class StrParam(Param):
    @staticmethod
    def create():
        return StrParam()

    p_type = 'str'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if isinstance(value, str):
            return True
        return False

    def paramType(self):
        return StrParam.p_type


class FloatParam(Param):
    @staticmethod
    def create():
        return FloatParam()

    p_type = 'float'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if isinstance(value, float):
            return True
        return False

    def paramType(self):
        return FloatParam.p_type


class AbsPathParam(Param):
    @staticmethod
    def create():
        return AbsPathParam()

    p_type = 'aPath'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if path.isabs(value):
            return True
        return False

    def paramType(self):
        return AbsPathParam.p_type


class RelPathParam(Param):
    @staticmethod
    def create():
        return RelPathParam()

    p_type = 'rPath'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if path.isabs(value):
            return False
        return True

    def paramType(self):
        return RelPathParam.p_type


class DictParam(Param):
    @staticmethod
    def create():
        return DictParam()

    p_type = 'dict'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if isinstance(value, dict):
            return True
        return False

    def paramType(self):
        return DictParam.p_type


class ListParam(Param):
    @staticmethod
    def create():
        return ListParam()

    p_type = 'list'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        if isinstance(value, list):
            return True

    def paramType(self):
        return ListParam.p_type


class AnyParam(Param):
    @staticmethod
    def create():
        return AnyParam()

    p_type = 'any'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        return True

    def paramType(self):
        return AnyParam.p_type


class UnionParam(Param):
    @staticmethod
    def create():
        return UnionParam()

    p_type = 'union'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    def checkValue(self, value) -> bool:
        return True

    def paramType(self):
        return UnionParam.p_type


class RangeListParam(Param):
    def __init__(self):
        super().__init__()
        self.typeList = None

    @staticmethod
    def create():
        return RangeListParam()

    p_type = 'rangeList'
    # 注册对象
    paramFactory.register(p_type, create.__get__(object))

    # 必须设置组合范围
    def setTypeList(self, typeList):
        self.typeList = typeList

    def checkValue(self, value) -> bool:
        if self.typeList is None:
            return False

        for subType in self.typeList:
            if paramFactory.create(subType).checkValue(value):
                return True

        return False

    def paramType(self):
        return RangeListParam.p_type

# class ParamFactory:
#     # 所有的工场管理器
#     instances = {}
#
#     factory = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.factory == None:
#             cls.factory = object.__new__(cls)
#         return cls.factory
#
#     def regist(paramfactory):
#         if isinstance(paramfactory, ParamFactory):
#             ParamFactory.instances[paramfactory.name] = paramfactory
#         else:
#             logging.error('Param工厂注册失败')
#
#     def __init__(self):
#         self.name = None
#         self.param_types = None
#
#         self._define()
#
#         # 构造函数会注册此类
#         if self.name:
#             ParamFactory.registe(self)
#
#     def _define(self):
#         return False
#
#     def _createParam(self, param_type):
#         return None
#
#     def _checkParam(self, param_type, param):
#         return False
#
#     def getParamTypes(self):
#         return self.param_types
#
#     def checkParam(self, param_type, param, factory_name=None):
#         if isinstance(param_type, list):
#             for sub_type in param_type:
#                 if self.checkParam(sub_type, param, factory_name):
#                     return True
#
#             return False
#
#         if factory_name is None:
#             for factory_name, paramFactory in ParamFactory.instances.items():
#                 if param_type in paramFactory.getParamTypes():
#                     return paramFactory._checkParam(param_type, param)
#             else:
#                 logging.error("创建Param" + param_type + "失败")
#                 return False
#
#         return ParamFactory.instances[factory_name]._checkParam(param_type, param)
#
#     def createParam(self, param_type, factory_name=None) -> Param:
#         if factory_name is None:
#             for factory_name, paramFactory in ParamFactory.instances.items():
#
#                 param = paramFactory._createParam(param_type)
#                 if param:
#                     return param
#             else:
#                 logging.error("创建Param" + param_type + "失败")
#                 return None
#
#         return ParamFactory.instances[factory_name]._createParam(param_type)
#
#
# paramFactory = ParamFactory()


# class BaseParamFactory(ParamFactory):
#     factory = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.factory == None:
#             cls.factory = object.__new__(cls)
#         return cls.factory
#
#     def _define(self):
#         self.name = 'base'
#         self.param_types = ['INT', 'BOOL', 'STRING', 'PATH_ABS', 'PATH_REL', 'LIST']
#
#     def _createParam(self, param_type):
#         return Param(param_type, self)
#
#     def _checkParam(self, param_type, param):
#         if param_type == 'INT':
#             return isinstance(param, int)
#         elif param_type == 'BOOL':
#             return isinstance(param, bool)
#         elif param_type == 'STRING':
#             return isinstance(param, str)
#         elif param_type == 'PATH_ABS':
#             return path.isabs(param)
#         elif param_type == 'PATH_REL':
#             return bool(1 - path.isabs(param))
#         elif param_type == 'LIST':
#             return isinstance(param, list)
#         return False
#
#
# factory = BaseParamFactory()


# 定义相关参
# def regist(paramfactory):
#     if isinstance(paramfactory, ParamFactory):
#         ParamFactory.instances[paramfactory.name] = paramfactory
#     else:
#         logging.error('Param工厂注册失败')
#
# def __init__(self):
#     self.name = None
#     self.param_types = None
#
#     self._define()
#
#     # 构造函数会注册此类
#     if self.name:
#         ParamFactory.regist(self)
#
# def _define(self):
#     return False
#
# def _createParam(self, param_type):
#     return None
#
# def _checkParam(self, param_type, param):
#     return False
#
# def getParamTypes(self):
#     return self.param_types
#
# def checkParam(self, param_type, param, factory_name=None):
#     if isinstance(param_type, list):
#         for sub_type in param_type:
#             if self.checkParam(sub_type, param, factory_name):
#                 return True
#
#         return False
#
#     if factory_name is None:
#         for factory_name, paramFactory in ParamFactory.instances.items():
#             if param_type in paramFactory.getParamTypes():
#                 return paramFactory._checkParam(param_type, param)
#         else:
#             logging.error("创建Param" + param_type + "失败")
#             return False
#
#     return ParamFactory.instances[factory_name]._checkParam(param_type, param)
#
# def createParam(self, param_type, factory_name=None) -> Param:
#     if factory_name is None:
#         for factory_name, paramFactory in ParamFactory.instances.items():
#
#             param = paramFactory._createParam(param_type)
#             if param:
#                 return param
#         else:
#             logging.error("创建Param" + param_type + "失败")
#             return None
#
#     return ParamFactory.instances[factory_name]._createParam(param_type)


# from enum import IntEnum
# from os import path
# import logging
#
# class Callback():
#     def call(self):
#         logging.critical("virtural callback")
#
# class ParamterType:
#     CustomType = []
#     PT_ABS_PATH = 0
#     PT_REL_PATH = 1
#     PT_INT = 10
#     PT_BOOL = 11
#     PT_STRING = 13
#     PT_INT_ENUM = 100
#     PT_INT_STRING = 101
#     PT_CUSTOM = 1000
#
# class Paramter():
#     p_id = None
#     p_type = ParamterType.PT_CUSTOM
#     p_value = None
#     callbacks = []
#
#     def __init__(self, p_id, p_type=ParamterType.PT_INT_STRING):
#         self.p_id = p_id
#         self.p_type = p_type
#         self.p_value = None
#         #参数值发生改变时
#         self.callbacks= []
#         self.owberJobID = None
#
#     def setOwnerJob(self, jobID):
#         self.owberJobID = jobID
#
#     def isValid(self):
#         if self.p_value:
#             return True
#         return False
#
#     def checkValue(self, value):
#         if self.p_type == ParamterType.PT_ABS_PATH:
#             return path.isabs(value)
#         elif self.p_type == ParamterType.PT_REL_PATH:
#             return bool(1-path.isabs(value))
#         return False
#
#     #添加回调
#     def addValueChangeCallback(self, callback):
#         if isinstance(callback):
#             self.callbacks.append(callback)
#         else:
#             logging.error("参数回调函数添加失败，请检查回调函数类型")
#
#     def removeValueChangeCallback(self, callback):
#         if isinstance(callback):
#             self.callbacks.remove(callback)
#         else:
#             logging.error("参数回调函数添加失败，请检查回调函数类型")
#
#     def strValue(self, value):
#         return str(value)
#
#     def setValue(self, value):
#         if (value is None or self.checkValue(value)) and self.p_value != value:
#             self.p_value = value
#             #调用回调
#             for callback in self.callbacks:
#                 callback.call()
#         else:
#             logging.error('设置参数值失败:' + self.strValue(value))
