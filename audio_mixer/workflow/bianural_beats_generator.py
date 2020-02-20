# -*- coding:utf-8 -*-

from audio_mixer.effects.effect_unit import EffectUnit
from audio_mixer.effects.shift_frequency.shift_frq import ShiftFrqTool
from audio_mixer.filter.frequency_filter import LowPassFrqFilter, HighPassFrqFilter
from audio_mixer.filter.filter_unit import FilterUnit
from audio_mixer.core.integrated_board import IntegratedBoardF2F, IntegratedBoardF2S, IntegratedBoardS2S, IntegratedBoardS2F
from audio_mixer.core.audio_handler import WavFile2Stream, Stream2WavFile
from audio_mixer.mixer.audio_mixer import AudioMixer


def generate_bianural_beats(input_file_path, output_file_path, left_frq, right_frq):
    """
    测试双耳节拍生成
    :param input_file_path:
    :param output_file_path:
    :param left_frq:
    :param right_frq:
    :return:
    """
    # 1. 配置效果单元（效果器集合，此处只使用了一个移频效果）
    shift_frq_tool = ShiftFrqTool(left_frq, right_frq)
    effect_unit = EffectUnit(shift_frq_tool)
    # 2. 配置源文件
    wav2stream = WavFile2Stream(input_file_path)
    # 3. 集成音频处理过程（此处只使用了效果单元）
    audio_obj_generator = IntegratedBoardS2S(effect_unit=effect_unit).run(wav2stream.audio_obj_generator)
    # 4. 迭代音频处理过程并保存至文件
    Stream2WavFile(output_file_path, audio_obj_generator, wav2stream.fs, wav2stream.channels).save()


def generate_lowfrq_bianural_beats(input_file_path, output_file_path, frq_threshold, left_frq, right_frq):
    """
    测试低频过滤+双耳节拍
    :param input_file_path:
    :param output_file_path:
    :param left_frq:
    :param right_frq:
    :return:
    """
    # 1. 配置移频效果器
    shift_frq_tool = ShiftFrqTool(left_frq, right_frq)
    effect_unit = EffectUnit(shift_frq_tool)

    # 2. 配置滤波器
    low_pass_filter = LowPassFrqFilter(frq_threshold, include_threshold=True)
    high_pass_filter = HighPassFrqFilter(frq_threshold, include_threshold=False)
    low_filter_unit = FilterUnit(low_pass_filter)
    high_filter_unit = FilterUnit(high_pass_filter)

    # 3. 从音频文件获取audio_obj_generator，此处注意不要从一个实例获取生成器
    audio_obj_generator1 = WavFile2Stream(input_file_path).audio_obj_generator
    audio_obj_generator2 = WavFile2Stream(input_file_path).audio_obj_generator

    # 4. 从音频文件获取采样率，channels
    tmp_file_obj = WavFile2Stream(input_file_path, init_load_file=False)
    fs = tmp_file_obj.fs
    channels = tmp_file_obj.channels

    # 低频部分移频
    audio_obj_generator1 = IntegratedBoardS2S(filter_unit=low_filter_unit, effect_unit=effect_unit).run(audio_obj_generator1)

    # 高频部分不变
    audio_obj_generator2 = IntegratedBoardS2S(filter_unit=high_filter_unit, effect_unit=None).run(audio_obj_generator2)

    # 混音
    mixer = AudioMixer((audio_obj_generator1, 1), (audio_obj_generator2, 1))
    mixed_audio_obj_generator = mixer.mix()

    # 保存至wav文件
    Stream2WavFile(output_file_path, mixed_audio_obj_generator, fs, channels).save()


if __name__ == "__main__":
    from datetime import datetime
    import sys
    # 1. 选择功能
    print("双耳节拍生成器")
    print("输入数字选择功能：1. 将制定音乐转为双耳节拍音乐 2. 将制定音乐的某一频段内音乐转为双耳节拍")
    for line in sys.stdin:
        choice = line.rstrip()
        if choice == "1":
            print("当前的选择是：1. 将制定音乐转为双耳节拍音乐")
            break
        elif choice == "2":
            print("当前的选择是：2. 将制定音乐的某一频段内音乐转为双耳节拍")
            break
        else:
            print("错误：只能输入1或2，请重新选择")
            print("输入数字选择功能：1. 将制定音乐转为双耳节拍音乐 2. 将制定音乐的某一频段内音乐转为双耳节拍")
    choice_num = int(choice)
    # 2. 选择输入文件
    from os import path
    print("请输入音频源文件完整路径:")
    for line in sys.stdin:
        input_file_path = line.rstrip()
        if not path.exists(input_file_path):
            print("当前文件路径无效，请输入有效文件路径")
        else:
            break
    # 3. 根据功能选择参数
    if choice_num == 1:
        print("请输入音频文件保存路径：（如果输入路径为空，则以日期名为格式保存在音频源文件所在目录）：")
        for line in sys.stdin:
            output_file_path = line.rstrip()
            if output_file_path == "":
                input_file_dir = path.dirname(input_file_path)
                output_file_path = path.join(input_file_dir, "{}.wav".format(datetime.now().strftime("%Y%M%d_%H%M%S")))
            output_file_dir = path.dirname(output_file_path)
            if not path.exists(output_file_dir):
                print("目标文件所属目录不存在，请输入有效的保存路径：")
            else:
                break
        print("请输入左声道移频数：")
        for line in sys.stdin:
            try:
                left_frq = int(line.rstrip())
                if isinstance(left_frq, int):
                    break
            except ValueError:
                print("请输入正确的移频数字")
                continue
        print("请输入右声道移频数：")
        for line in sys.stdin:
            try:
                right_frq = int(line.rstrip())
                if isinstance(right_frq, int):
                    break
            except ValueError:
                print("请输入正确的移频数字")
                continue
        # 4. 执行任务
        print(input_file_path, output_file_path)
        print("processing...")
        generate_bianural_beats(input_file_path, output_file_path, left_frq=left_frq, right_frq=right_frq)
        print("执行完成，文件路径为：{}".format(output_file_path))
    elif choice_num == 2:
        print("请输入音频文件保存路径（如果输入路径为空，则以日期名为格式保存在音频源文件所在目录）：")
        for line in sys.stdin:
            output_file_path = line.rstrip()
            if output_file_path == "":
                input_file_dir = path.dirname(input_file_path)
                output_file_path = path.join(input_file_dir, "{}.wav".format(datetime.now().strftime("%Y%M%d_%H%M%S")))
            output_file_dir = path.dirname(output_file_path)
            if not path.exists(output_file_dir):
                print("目标文件所属目录不存在，请输入有效的保存路径：")
            else:
                break
        print("您打算将多少赫兹以内的音频频率进行移频")
        for line in sys.stdin:
            try:
                frq_threshold = int(line.rstrip())
                if isinstance(frq_threshold, int):
                    break
            except ValueError:
                print("请输入正确的频率数字")
                continue
        print("请输入左声道移频数：")
        for line in sys.stdin:
            try:
                left_frq = int(line.rstrip())
                if isinstance(left_frq, int):
                    break
            except ValueError:
                print("请输入正确的移频数字")
                continue
        print("请输入右声道移频数：")
        for line in sys.stdin:
            try:
                right_frq = int(line.rstrip())
                if isinstance(right_frq, int):
                    break
            except ValueError:
                print("请输入正确的移频数字")
                continue
        # 4. 执行任务
        print("processing...")
        generate_lowfrq_bianural_beats(input_file_path, output_file_path, frq_threshold=frq_threshold, left_frq=left_frq,
                                       right_frq=right_frq)
        print("执行完成，文件路径为：{}".format(output_file_path))
    else:
        print("无效的任务类型")
