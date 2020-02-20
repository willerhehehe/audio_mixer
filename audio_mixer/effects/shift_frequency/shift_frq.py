# -*- coding:utf-8 -*-
from scipy.fftpack import fft, ifft
import numpy as np

from audio_mixer.effects.effect_object import EffectObject


class ShiftFrqTool(EffectObject):
    """
    移频工具(接受参数：左声道移频频率，右声道移频频率)
    输入音频信号对象audio_obj，返回移频后的音频信号对象
    音频信号对象:audio_obj（具有至少两个属性，audio_obj.data及audio_obj.fs）
    audio_obj.data: 双声道音频数据，
    信号长度:n（不限）
    type(audio_obj.data) >>> <class 'numpy.ndarray'>
    audio_obj.data.shape >>> (n, 2)  # n行2列，分别对应左右声道
    """

    def __init__(self, shift_frq_left=0, shift_frq_right=0):
        self.sfl = shift_frq_left
        self.sfr = shift_frq_right

    @staticmethod
    def get_frq_shift_nums(n, fs, shift_frq):
        """
        根据采样率和移频量，计算数据需要的移频点数，计算公式(不为整数时取四舍五入):
        return = shift_frq*n/fs
        :param n: fft变换的长度，也既数据长度
        :param fs:
        :param shift_frq:
        :return: 采样点右移数
        """
        return round(shift_frq * n / fs)

    def fft_data_shift(self, fs, fft_data, shift_frq):
        """
        Frequency Domain data shifted, 经过fft变换后的数据平移shift_num个点，将经过fft变换后的数列分为左右部分，
        左半部分右移shift_num，右半部分左移shift_num，超出部分去掉，不足部分补0。
        eg1: 若参数为fft_data = [1,2,3,4,5,6], shift_num=2 ,则返回 [0,0,1,6,0,0]; 其中1代表0Hz
        eg2: 若参数为fft_data = [1,2,3,4,5,6,7], shift_num=3, 则返回[0,0,1,2,7,0,0]; 其中1代表0Hz
        :param fft_data: 需要移频的数据
        :param shift_frq: 需要移频的频率
        :return: 平移后的数据
        """
        n = len(fft_data)
        shift_num = self.get_frq_shift_nums(n, fs, shift_frq)
        if type(fft_data) is not np.ndarray:
            fft_data = np.array(fft_data)
        if fft_data.dtype == 'complex':
            zero = np.complex(0)
        else:
            zero = 0
        if n % 2 == 0:
            part1 = fft_data[0:int(n / 2)]
            part2 = fft_data[int(n / 2):]
        elif n % 2 == 1:
            part1 = fft_data[0:int((n + 1) / 2)]
            part2 = fft_data[int((n + 1) / 2):]
        else:
            raise RuntimeError("n % 2 must 1 or 0, but n is {} and type(n)={}".format(n, type(n)))

        part1 = np.roll(part1, shift_num)
        part1[:shift_num] = zero
        part2 = np.roll(part2, -shift_num)
        part2[-shift_num:] = zero
        return np.concatenate((part1, part2))

    def mono_frq_shift(self, data: list, fs: int, shift_frq: int):
        """
        单声道移频
        :param data:
        :param fs:
        :param shift_frq:
        :return:
        """
        if shift_frq != 0:
            fft_data = fft(data)
            shifted_fft_data = self.fft_data_shift(fs, fft_data, shift_frq)
            shifted_data = ifft(shifted_fft_data)
            return [i.real for i in shifted_data]
        else:
            return data

    def frq_shift(self, data, fs):
        """
        输入音频信号，返回移频后的音频信号
        :param data:
        :param fs:
        :return:
        """
        left_channel = self.mono_frq_shift(data[:, 0], fs, shift_frq=self.sfl)
        right_channel = self.mono_frq_shift(data[:, 1], fs, shift_frq=self.sfr)
        return np.array([[i[0], i[1]] for i in zip(left_channel, right_channel)])

    @staticmethod
    def check_audio_obj(audio_obj):
        if not hasattr(audio_obj, "data") and hasattr(audio_obj, "fs"):
            raise TypeError("音频对象audio_obj不符合规范，至少需要包含data属性及fs属性")
        if not isinstance(audio_obj.data, np.ndarray):
            raise TypeError("音频对象audio_obj不符合规范，data属性必须为numpy.ndarray类型")

    def process(self, audio_obj):
        """
        入口方法，对音频对象进行加工
        :param audio_obj:
        :return:
        """
        self.check_audio_obj(audio_obj)
        audio_obj.data = self.frq_shift(audio_obj.data, audio_obj.fs)
        return audio_obj


