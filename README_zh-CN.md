# AI 生成视频创作工具

[English](README.md) | [简体中文](README_zh-CN.md)

这个项目是一个AI驱动的视频创作工具，结合图像生成、文本转语音和视频编辑技术，生成独特而引人入胜的视频。通过利用先进的AI技术，该工具允许用户创建具有自定义场景和相应背景解说的视频。

## 先决条件

在运行项目之前，请确保您具备以下条件：

- 连接到 Genmo 的 Discord 账号（在 `image_2_video_voice.py` 中配置）
- 用于文本转语音的 Azure API 密钥（在 `test_2_speech.py` 中配置）
- 用于图像生成的 OpenAI API 密钥（在 `test_2_image.py` 中配置）

## 使用方法

1. 在相应的文件中配置必要的 API 密钥和账号信息。
2. 在 `image_2_video_rpa.py` 中定义您自己的场景和背景解说。
3. 运行 `image_2_video_rpa.py` 以生成视频。

注意：如果您想创建新的视频，请确保在再次运行脚本之前清空 `audio_files` 和 `image_folder` 目录。

## 自定义

在 `image_2_video_rpa.py` 中，您可以通过修改 `my_scenes` 和 `my_texts` 列表来自定义场景和背景解说。每个场景应该有一个对应的背景解说，确保视觉和音频元素之间一一对应。

示例：
​```python
# 定义自己的场景
my_scenes = [
   "一个带有数学方程式的黑板，数字模糊且变化，描绘真理的不确定性。",
   "一个纠缠着线条的织布机，半成品挂毯悬挂着，象征着讲故事的复杂性和失误。",
   ...
]
# 生成图像
generate_images(my_scenes)

# 定义自己的文本
my_texts = [
   "在辨别的舞蹈中，二加二可能等于四，也可能等于二十二，",
   "故事的编织者们，用他们沉重的手，经常在他们的工艺中跌倒，",
   ...
]
​```

## 示例

查看使用该工具创建的示例视频：

[![示例 1](https://i.ytimg.com/vi/zwETWcPaTog/maxresdefault.jpg)](https://www.youtube.com/watch?v=zwETWcPaTog "示例 1")