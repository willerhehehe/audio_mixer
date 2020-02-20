import unittest
from math import pi, sin
import matplotlib.pyplot as plt
import numpy as np
from audio_mixer.filter.frequency_filter import LowPassFrqFilter, HighPassFrqFilter, BandPassFrqFilter


class TestShiftFrequency(unittest.TestCase):

    def test_lowpass_filter(self):
        Fs = 44100
        t = [(i + 1) / Fs for i in range(Fs)]
        sin_y1 = [sin(2 * pi * 10 * i) for i in t]
        sin_y2 = [sin(2 * pi * 100 * i) for i in t]
        sin_y3 = [sin(2 * pi * 500 * i) for i in t]
        sin_y4 = [sin(2 * pi * 2000 * i) for i in t]
        y_le100 = np.array(sin_y1) + np.array(sin_y2)
        y_lt100 = np.array(sin_y1)
        y_le500 = np.array(sin_y1) + np.array(sin_y2) + np.array(sin_y3)
        y = np.array(sin_y1) + np.array(sin_y2) + np.array(sin_y3) + np.array(sin_y4)
        lpff = LowPassFrqFilter(100, include_threshold=False)
        filter_y = lpff.frq_filter(y, Fs)
        sum = abs(filter_y-y_lt100).sum()
        self.assertAlmostEqual(sum, 0)
        lpff = LowPassFrqFilter(100, include_threshold=True)
        filter_y = lpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_le100).sum()
        self.assertAlmostEqual(sum, 0)
        lpff = LowPassFrqFilter(500, include_threshold=True)
        filter_y = lpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_le500).sum()
        self.assertAlmostEqual(sum, 0)

    def test_highpass_filter(self):
        Fs = 44100
        t = [(i + 1) / Fs for i in range(Fs)]
        sin_y1 = [sin(2 * pi * 10 * i) for i in t]
        sin_y2 = [sin(2 * pi * 100 * i) for i in t]
        sin_y3 = [sin(2 * pi * 500 * i) for i in t]
        sin_y4 = [sin(2 * pi * 2000 * i) for i in t]
        y = np.array(sin_y1) + np.array(sin_y2) + np.array(sin_y3) + np.array(sin_y4)
        y_ge100 = np.array(sin_y2) + np.array(sin_y3) + np.array(sin_y4)
        y_ge500 = np.array(sin_y3) + np.array(sin_y4)
        y_gt500 = np.array(sin_y4)
        hpff = HighPassFrqFilter(500, include_threshold=False)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_gt500).sum()
        self.assertAlmostEqual(sum, 0)
        hpff = HighPassFrqFilter(500, include_threshold=True)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_ge500).sum()
        self.assertAlmostEqual(sum, 0)
        hpff = HighPassFrqFilter(100, include_threshold=True)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_ge100).sum()
        self.assertAlmostEqual(sum, 0)

    def test_bandpass_filter(self):
        Fs = 44100
        t = [(i + 1) / Fs for i in range(Fs)]
        sin_y1 = [sin(2 * pi * 10 * i) for i in t]
        sin_y2 = [sin(2 * pi * 100 * i) for i in t]
        sin_y3 = [sin(2 * pi * 500 * i) for i in t]
        sin_y4 = [sin(2 * pi * 2000 * i) for i in t]
        y = np.array(sin_y1) + np.array(sin_y2) + np.array(sin_y3) + np.array(sin_y4)
        y_ge10le500 = np.array(sin_y1) + np.array(sin_y2) + np.array(sin_y3)
        y_ge10lt500 = np.array(sin_y1) + np.array(sin_y2)
        y_gt10le500 = np.array(sin_y2) + np.array(sin_y3)
        y_gt10lt500 = np.array(sin_y2)
        hpff = BandPassFrqFilter(10, 500, include_sfrq=True, include_efrq=True)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_ge10le500).sum()
        self.assertAlmostEqual(sum, 0)
        hpff = BandPassFrqFilter(10, 500, include_sfrq=True, include_efrq=False)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_ge10lt500).sum()
        self.assertAlmostEqual(sum, 0)
        hpff = BandPassFrqFilter(10, 500, include_sfrq=False, include_efrq=True)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_gt10le500).sum()
        self.assertAlmostEqual(sum, 0)
        hpff = BandPassFrqFilter(10, 500, include_sfrq=False, include_efrq=False)
        filter_y = hpff.frq_filter(y, Fs)
        sum = abs(filter_y - y_gt10lt500).sum()
        self.assertAlmostEqual(sum, 0)


if __name__ == "__main__":
    unittest.main()