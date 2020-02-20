import unittest
from math import pi, sin
from scipy.fftpack import fft
import numpy as np

from audio_mixer.effects.shift_frequency.shift_frq import ShiftFrqTool


class TestShiftFrequency(unittest.TestCase):

    def test_frq_shift(self):
        Fs = 44100
        left_frq_shift = 5
        right_frq_shift = 4
        t = [(i + 1) / Fs for i in range(Fs)]
        sin_y1 = [sin(2 * pi * 5 * i) for i in t]
        sin_y2 = [sin(2 * pi * 6 * i) for i in t]
        test_data = np.array([[i[0], i[1]] for i in zip(sin_y1, sin_y2)])
        frqshift_5_6 = ShiftFrqTool(left_frq_shift, right_frq_shift)
        rtn_data = frqshift_5_6.frq_shift(test_data, Fs)
        left_data = [i[0] for i in rtn_data]
        right_data = [i[1] for i in rtn_data]
        self.assertEqual(int(fft(right_data)[10].real), 18)
        self.assertEqual(int(fft(left_data)[10].real), 15)

    def test_get_frq_shift_nums(self):
        n = 44100 * 2
        fs = 44100
        shift_frq = 10
        self.assertEqual(ShiftFrqTool.get_frq_shift_nums(n, fs, shift_frq), 20)

    def test_fft_data_shift(self):
        array1 = np.array([1, 2, 3, 4, 5, 6])
        array2 = np.array([1, 2, 3, 4, 5, 6, 7])
        array1 = ShiftFrqTool(2, 2).fft_data_shift(6, array1, 2)
        array2 = ShiftFrqTool(2, 2).fft_data_shift(7, array2, 2)
        self.assertEqual(list(array1), [0, 0, 1, 6, 0, 0])
        self.assertEqual(list(array2), [0, 0, 1, 2, 7, 0, 0])


if __name__ == "__main__":
    unittest.main()
