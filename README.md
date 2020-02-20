# 项目作用
为wav格式音频增加binaural beats双耳节拍效果

# 使用说明
## 快速制作双耳节拍音乐

### 1. 安装audio_mixer包
执行`pip install audio_mixer`

### 2. 执行`bianural_beats_generator`模块
执行`python -m audio_mixer.workflow.bianural_beats_generator`

### 3. 按照命令行提示符输入指定参数

*PS:若在未安装audio_mixer包的情况下使用：*

*需要先切换至audio_mixer包所在的父目录下，并执行以下命令：*

*`python -m audio_mixer.workflow.bianural_beats_generator`*

*（注：当前仅支持wav格式文件，请进行格式转换后再使用)*


# 开发使用的python版本
python --version: Python 3.6.6

# pip requirement 依赖包
依赖包文件：
`audio_mixer/config/requirement.txt`

## 项目代码拓扑
![代码拓扑](https://github.com/willerhehehe/audio_mixer/blob/master/img/audio_mixer.svg)
## 工作流
![工作流](https://github.com/willerhehehe/audio_mixer/blob/master/img/workflow.svg)
