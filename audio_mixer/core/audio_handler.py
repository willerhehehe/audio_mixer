# -*- coding:utf-8 -*-
from types import GeneratorType

import soundfile as sf
from audio_mixer.core.audio_object import AudioObject


class AudioFile(object):
    def __init__(self, input_file_dir):
        self.file_dir = input_file_dir
        self.samplerate = None
        self.subtype = None
        self.channels = None
        self.format = None
        self.get_file_info()

    def get_file_info(self):
        with sf.SoundFile(self.file_dir, 'r') as f:
            self.samplerate = f.samplerate
            self.subtype = f.subtype
            self.channels = f.channels
            self.format = f.format

    def read(self, blocksize: int = 1024, position: int = 0):
        with sf.SoundFile(self.file_dir, 'r') as f:
            file_size = len(f)
            if position > file_size:
                raise ValueError("TOO LARGE: start position is larger than file size")
            f.seek(position)
            while f.tell() < len(f):
                block_data = f.read(blocksize)
                yield block_data

    def read_as_audio_obj(self, blocksize: int = 1024, position: int = 0):
        for block_data in self.read(blocksize=blocksize, position=position):
            aud_obj = AudioObject(data=block_data, fs=self.samplerate)
            yield aud_obj

    def read_overlap(self, blocksize: int = 1024, overlap: int = 512):
        return (block for block in sf.blocks(self.file_dir, blocksize=blocksize, overlap=overlap))

    @staticmethod
    def write_iterator(input_data: iter, output_file: str, samplerate: int, channels: int):
        with sf.SoundFile(output_file, 'w', samplerate, channels) as f:
            for block_data in input_data:
                f.write(block_data)

    @staticmethod
    def write(block_data, f):
        f.write(block_data)


class WavFile2Stream(object):
    """
    接收一个wav文件路径
    通过访问实例的audio_obj_generator属性，获取一个该wav文件的audio_obj对象生成器
    param: init_load_file 默认为True, 代表在创建实例时自动读取文件创建生成器对象
    """

    def __init__(self, source_path, blocksize: int = 44100, position: int = 0, init_load_file=True):
        self.source_path = source_path
        self.blocksize = blocksize
        self.position = position
        self.audio_file = AudioFile(self.source_path)
        self.fs = self.audio_file.samplerate
        self.channels = self.audio_file.channels
        if init_load_file:
            self._audio_obj_generator = self.audio_file.read_as_audio_obj(self.blocksize, self.position)

    @property
    def audio_obj_generator(self):
        if not self._audio_obj_generator:
            self._audio_obj_generator = self.audio_file.read_as_audio_obj(self.blocksize, self.position)
        return self._audio_obj_generator

    @audio_obj_generator.setter
    def audio_obj_generator(self, audio_obj_generator):
        self._audio_obj_generator = audio_obj_generator

    @audio_obj_generator.deleter
    def audio_obj_generator(self):
        del self._audio_obj_generator


class Stream2WavFile(object):
    """
    接收一个audio_obj对象的生成器
    通过调用实例的save方法，将生成器内容保存在指定wav文件内
    """

    def __init__(self, file_save_path, audio_obj_generator, fs, channels):
        self._audio_obj_generator = None
        self.file_save_path = file_save_path
        self.audio_obj_generator = audio_obj_generator
        self.fs = fs
        self.channels = channels

    @property
    def audio_obj_generator(self):
        return self._audio_obj_generator

    @audio_obj_generator.setter
    def audio_obj_generator(self, audio_obj_generator):
        if not isinstance(audio_obj_generator, GeneratorType):
            raise TypeError("Audio_obj_generator must be a generator")
        self._audio_obj_generator = audio_obj_generator

    @audio_obj_generator.deleter
    def audio_obj_generator(self):
        del self._audio_obj_generator

    def save(self):
        with sf.SoundFile(self.file_save_path, 'w', self.fs, self.channels) as f:
            for audio_obj in self._audio_obj_generator:
                f.write(audio_obj.data)


if __name__ == "__main__":
    input_file_path = "/Users/willer/work/音频相关/不要说话.wav"
    wav2stream = WavFile2Stream(input_file_path)
    audio_obj_gen = wav2stream.audio_obj_generator
    Stream2WavFile("/Users/willer/work/音频相关/tmp_test_201912241430.wav", audio_obj_gen, wav2stream.fs, wav2stream.channels).save()


