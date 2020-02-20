# -*- coding:utf-8 -*-
"""
选择输入设备，处理单元（效果器单元），输出设备
"""
import soundfile as sf

from audio_mixer.core.audio_handler import AudioFile


class IntegratedBoard(object):

    def __init__(self):
        pass


class IntegratedBoardF2F(IntegratedBoard):
    """
    from file to file
    """
    def __init__(self, source_file_path, target_file_path, filter_unit=None, effect_unit=None):
        self.sfp = source_file_path
        self.tfp = target_file_path
        self.effect_unit = effect_unit
        self.filter_unit = filter_unit

    def integrated_process(self, audio_obj):
        # 滤波器处理
        if self.filter_unit:
            audio_obj = self.filter_unit.process(audio_obj)
        # 效果器处理
        if self.effect_unit:
            audio_obj = self.effect_unit.process(audio_obj)
        return audio_obj

    def run(self, blocksize=44100):
        audio_file_obj = AudioFile(self.sfp)
        with sf.SoundFile(self.tfp, 'w', audio_file_obj.samplerate, audio_file_obj.channels) as f:
            for audio_obj in audio_file_obj.read_as_audio_obj(blocksize=blocksize):
                audio_obj = self.integrated_process(audio_obj)
                f.write(audio_obj.data)


class IntegratedBoardF2S(IntegratedBoard):
    """
    from file to stream audio_obj generator
    """
    def __init__(self, source_file_path, filter_unit=None, effect_unit=None):
        self.sfp = source_file_path
        self.effect_unit = effect_unit
        self.filter_unit = filter_unit

    def integrated_process(self, audio_obj):
        # 滤波器处理
        if self.filter_unit:
            audio_obj = self.filter_unit.process(audio_obj)
        # 效果器处理
        if self.effect_unit:
            audio_obj = self.effect_unit.process(audio_obj)
        return audio_obj

    def run(self, blocksize=44100):
        audio_file_obj = AudioFile(self.sfp)
        for audio_obj in audio_file_obj.read_as_audio_obj(blocksize=blocksize):
            audio_obj = self.integrated_process(audio_obj)
            yield audio_obj


class IntegratedBoardS2F(IntegratedBoard):
    """
    from stream to file audio_obj generator
    """
    def __init__(self, target_file_path, filter_unit=None, effect_unit=None):
        self.tfp = target_file_path
        self.effect_unit = effect_unit
        self.filter_unit = filter_unit

    def integrated_process(self, audio_obj_generator):
        for audio_obj in audio_obj_generator:
            # 滤波器处理
            if self.filter_unit:
                audio_obj = self.filter_unit.process(audio_obj)
            # 效果器处理
            if self.effect_unit:
                audio_obj = self.effect_unit.process(audio_obj)
            yield audio_obj

    def run(self, audio_obj_generator, fs, channels):
        with sf.SoundFile(self.tfp, 'w', fs, channels) as f:
            for audio_obj in self.integrated_process(audio_obj_generator):
                f.write(audio_obj.data)


class IntegratedBoardS2S(IntegratedBoard):
    """
    from stream audio_object generator to stream audio_object generator
    """
    def __init__(self, filter_unit=None, effect_unit=None):
        self.effect_unit = effect_unit
        self.filter_unit = filter_unit

    def integrated_process(self, audio_obj_generator):
        for audio_obj in audio_obj_generator:
            # 滤波器处理
            if self.filter_unit:
                audio_obj = self.filter_unit.process(audio_obj)
            # 效果器处理
            if self.effect_unit:
                audio_obj = self.effect_unit.process(audio_obj)
            yield audio_obj

    def run(self, audio_obj_generator):
        for audio_obj in self.integrated_process(audio_obj_generator):
            yield audio_obj
