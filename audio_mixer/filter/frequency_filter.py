# -*- coding:utf-8 -*-
"""
滤波器模块
接受audio_obj对象，返回滤波后的audio_obj对象
1. 低通滤波器
2. 高通滤波器
3. 带通滤波器

后续添加：
1.如果数据过短，频率阈值不能过高，后期需增加相关判断
"""
from scipy.fftpack import fft, ifft
import numpy as np

from audio_mixer.common_tools.numfrq_transfer import frq2num
from audio_mixer.common_tools.fft_data_divide import fft_data_divide

from audio_mixer.filter.filter_object import FliterObject


class LowPassFrqFilter(FliterObject):

    def __init__(self, frq_threshold, include_threshold=True):
        self.frq_threshold = frq_threshold
        self.include_threshold = include_threshold

    def frq_filter(self, data, fs):
        data_length = len(data)
        num = frq2num(self.frq_threshold, data_length, fs)
        fft_data = fft(data, axis=0)  # axis=0代表按列fft
        fft_part1, fft_part2 = fft_data_divide(fft_data)
        if self.include_threshold:
            fft_part1[num+1:] = 0
            fft_part2[:-num] = 0
        else:
            fft_part1[num:] = 0
            fft_part2[:-(num-1)] = 0
        filtered_fft_data = np.concatenate((fft_part1, fft_part2))
        filtered_data = ifft(filtered_fft_data, axis=0)
        return filtered_data.real

    def process(self, audio_obj):
        audio_obj.data = self.frq_filter(audio_obj.data, audio_obj.fs)
        return audio_obj


class HighPassFrqFilter(FliterObject):

    def __init__(self, frq_threshold, include_threshold=True):
        self.frq_threshold = frq_threshold
        self.include_threshold = include_threshold

    def frq_filter(self, data, fs):
        data_length = len(data)
        num = frq2num(self.frq_threshold, data_length, fs)
        fft_data = fft(data, axis=0)  # axis=0代表按列fft
        fft_part1, fft_part2 = fft_data_divide(fft_data)
        if self.include_threshold:
            fft_part1[:num] = 0
            fft_part2[-(num-1):] = 0
        else:
            fft_part1[:num+1] = 0
            fft_part2[-num:] = 0
        filtered_fft_data = np.concatenate((fft_part1, fft_part2))
        filtered_data = ifft(filtered_fft_data, axis=0)
        return filtered_data.real

    def process(self, audio_obj):
        audio_obj.data = self.frq_filter(audio_obj.data, audio_obj.fs)
        return audio_obj


class BandPassFrqFilter(FliterObject):

    def __init__(self, start_frq, end_frq, include_sfrq=True, include_efrq=True):
        self.start_frq = start_frq
        self.end_frq = end_frq
        self.include_sfrq = include_sfrq
        self.include_efrq = include_efrq

    def frq_filter(self, data, fs):
        data_length = len(data)
        snum = frq2num(self.start_frq, data_length, fs)
        enum = frq2num(self.end_frq, data_length, fs)
        fft_data = fft(data, axis=0)
        fft_part1, fft_part2 = fft_data_divide(fft_data)
        if self.include_sfrq and self.include_efrq:  # 双闭
            fft_part1[enum + 1:] = 0
            fft_part1[:snum] = 0
            fft_part2[:-enum] = 0
            fft_part2[-(snum - 1):] = 0
        elif self.include_sfrq and not self.include_efrq:  # 左闭右开
            fft_part1[enum:] = 0
            fft_part1[:snum] = 0
            fft_part2[:-(enum-1)] = 0
            fft_part2[-(snum - 1):] = 0
        elif not self.include_sfrq and self.include_efrq:  # 左开右闭
            fft_part1[enum + 1:] = 0
            fft_part1[:snum+1] = 0
            fft_part2[:-enum] = 0
            fft_part2[-snum:] = 0
        else:  # 双开
            fft_part1[enum:] = 0
            fft_part1[:snum+1] = 0
            fft_part2[:-(enum-1)] = 0
            fft_part2[-snum:] = 0
        filtered_fft_data = np.concatenate((fft_part1, fft_part2))
        filtered_data = ifft(filtered_fft_data, axis=0)
        return filtered_data.real

    def process(self, audio_obj):
        audio_obj.data = self.frq_filter(audio_obj.data, audio_obj.fs)
        return audio_obj


if __name__ == "__main__":
    pass