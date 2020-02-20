# -*- coding:utf-8 -*-


def num2frq(num, fs, data_length):
    """
    点数转换为频率
    :param num: 点数
    :param fs: 采样率
    :param data_length: 数据长度
    :return:
    """
    return round(num*fs/data_length)


def frq2num(frq, data_length, fs):
    """
    频率转换为点数
    :param frq: 频率
    :param data_length: 数据长度
    :param fs: 采样率
    :return: 点数
    """
    k = round(frq*(data_length/fs))
    return k