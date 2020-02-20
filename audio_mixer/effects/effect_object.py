# -*- coding:utf-8 -*-
"""
效果器的抽象类型
所有效果器需要继承自此类型，并实现process方法
def process(self, audio_obj):
    return audio_obj
"""
from abc import ABCMeta, abstractmethod


class EffectObject(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process(self, audio_obj):
        return audio_obj

