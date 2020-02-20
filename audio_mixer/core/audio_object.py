# -*- coding:utf-8 -*-
from numpy import ndarray


class AudioObject(object):
    def __init__(self, data, fs):
        self.check_param(data, fs)
        self.data = data
        self.fs = fs

    @staticmethod
    def check_param(data, fs):
        if not isinstance(fs, int):
            raise TypeError("fs不符合规范，采样率必须为int类型")
        if not isinstance(data, ndarray):
            raise TypeError("data不符合规范，data必须为numpy.ndarray类型")