# -*- coding:utf-8 -*-


def fft_data_divide(fft_data):
    n = len(fft_data)
    if n % 2 == 0:
        part1 = fft_data[0:int(n / 2)]
        part2 = fft_data[int(n / 2):]
    elif n % 2 == 1:
        part1 = fft_data[0:int((n + 1) / 2)]
        part2 = fft_data[int((n + 1) / 2):]
    else:
        raise RuntimeError("n % 2 must 1 or 0, but n is {} and type(n)={}".format(n, type(n)))
    return part1, part2