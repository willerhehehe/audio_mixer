# -*- coding:utf-8 -*-

"""
滤波器管理入口
实现目标：
1.初始化实例时选择不同滤波方法
2.调用方法时，接收音频对象，调用滤波器处理音频对象，返回音频对象
"""
from audio_mixer.filter.filter_object import FliterObject


class FilterUnit(object):

    def __init__(self, *filter_tools):
        for filter_obj in filter_tools:
            if not isinstance(filter_obj, FliterObject):
                raise TypeError("传入对象不是一个有效的滤波器类型")
        self.filter_tools = filter_tools

    def process(self, audio_obj):
        for filter_tool in self.filter_tools:
            audio_obj = filter_tool.process(audio_obj)
        return audio_obj
