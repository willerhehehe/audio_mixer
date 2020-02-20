# -*- coding:utf-8 -*-

"""
效果器管理入口
实现目标：
1.初始化实例时选择不同效果
2.调用方法时，接收音频对象，调用效果器处理音频对象，返回音频对象
"""
from audio_mixer.effects.effect_object import EffectObject


class EffectUnit(object):

    def __init__(self, *effect_tools):
        for effect_obj in effect_tools:
            if not isinstance(effect_obj, EffectObject):
                raise TypeError("传入对象不是一个有效的效果器类型")
        self.effect_tools = effect_tools

    def process(self, audio_obj):
        for effect_tool in self.effect_tools:
            audio_obj = effect_tool.process(audio_obj)
        return audio_obj
