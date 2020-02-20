# -*- coding:utf-8 -*-
from audio_mixer.core.audio_object import AudioObject


class AudioMixer(object):
    def __init__(self, *audio_rate_tuple):
        """
        :param audio_rate_tuple: (audio_obj_generator, rate)
        """
        self.audio_rate_tuple = audio_rate_tuple

    def mix(self):
        while True:
            try:
                first_audio_obj_generator, rate1 = self.audio_rate_tuple[0][0], self.audio_rate_tuple[0][1]
                first_audio_obj = next(first_audio_obj_generator)
                fs = first_audio_obj.fs
                sum_audio_data = first_audio_obj.data * rate1
                for i in range(1, len(self.audio_rate_tuple)):
                    audio_obj_generator, rate = self.audio_rate_tuple[i][0], self.audio_rate_tuple[i][1]
                    sum_audio_data += next(audio_obj_generator).data * rate
                rtn_audio_obj = AudioObject(sum_audio_data, fs)
                yield rtn_audio_obj
            except StopIteration:
                break
