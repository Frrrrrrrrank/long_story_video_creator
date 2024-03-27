import os
import azure.cognitiveservices.speech as speechsdk

def init_azure_speech_synthesizer(subscription_key, region):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = 'zh-CN-XiaoxiaoNeural'
    return speech_config

def generate_audio(speech_config, text, filename):
    # 确保文件夹存在
    audio_folder = 'audio_files'
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    # 设置音频输出为文件
    audio_config = speechsdk.audio.AudioConfig(filename=os.path.join(audio_folder, filename))

    # 设置语音配置为中文语音
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

    # 设置语音配置为英文语音
    # speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"


    # 设置语音配置为德语语音
    # speech_config.speech_synthesis_voice_name = "de-DE-ChristophNeural"

    # 设置语音配置为日语语音
    # speech_config.speech_synthesis_voice_name = "ja-JP-MayuNeural"
    # 创建 SSML 文本中文
    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="zh-CN">
        <voice name="{speech_config.speech_synthesis_voice_name}">
            <mstts:express-as style="lyrical">
                {text}
            </mstts:express-as>
        </voice>
    </speak>
    """

    # 创建 SSML 文本英文低语
    # ssml_text = f"""
    # <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
    #     <voice name="{speech_config.speech_synthesis_voice_name}">
    #         <mstts:express-as style="whispering">
    #             {text}
    #         </mstts:express-as>
    #     </voice>
    # </speak>
    # """

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_ssml_async(ssml_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text [{text}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        print(f"Speech synthesis canceled: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"Error detail: {cancellation.error_details}")

def generate_speech_from_texts(texts, speech_config):
    # 循环文本列表，并生成对应的音频文件
    for i, text in enumerate(texts):
        filename = f"{i+1}.mp3"  # 文件命名为 1.mp3, 2.mp3, ...
        generate_audio(speech_config, text, filename)

if __name__ == "__main__":
    # 订阅密钥和区域
    subscription_key = "Your Azure tts Key"
    subscription_region = "eastus"

    # 初始化 Azure TTS 配置
    speech_config = init_azure_speech_synthesizer(subscription_key, subscription_region)

    # 待转换的文本列表
    texts = [
        "探索Claude 3系列AI模型的智能与成本关系图。这张图表利用对数尺度清晰展示了三款模型—Haiku, Sonnet和Opus—之间的成本效益比。随着成本的提高，每个模型的智能水平也相应提升，其中Haiku性价比最高，Sonnet居中，而Opus则在智能和价格上均处于顶端",

        "深入比较Claude 3系列模型，涵盖Haiku、Sonnet和Opus，以及其他同类AI模型。这些模型在多个领域中展示出卓越性能，包括内容创作、多语言对话、以及对复杂数据的处理。特别强调了Opus模型在处理超过一百万token的输入上具有行业领先的表现，同时所有模型都具备了更快的响应能力和更高的准确性，显著提升了用户体验",

        "虽然缺少直接的性能对比数据，但Claude 3家族在增强智能、速度、成本效益和视觉处理能力方面树立了新的标准。这些模型设计用于在一系列认知任务中取得优异成绩，展示了其领先的技术优势。",

        "相较于早期版本，Claude 3系列在理解上下文和减少不必要的拒绝方面取得了显著进步，表现出更加细腻的请求理解能力和对边缘内容的合理处理。",

        "Claude 3 Opus在提高准确性和处理复杂查询方面相较于先前模型取得了显著进步，同时所有模型都在用户交互、数据提取和视觉格式处理等方面展现出强大能力。",

        "Claude 3 Opus在处理长达200K token的长文本信息中展现出接近完美的信息回忆能力，成功应对了“大海捞针”这一挑战，准确率超过99%。。",

        "Claude 3系列模型提供了多种智能、速度和成本的平衡选择，强调了在提供高性能的同时降低成本和增强用户体验的重要性，包括对视觉信息的处理能力和对偏见的减少。",

        "“Context window”的介绍强调了Claude 3家族模型在处理大量信息方面的能力，初始提供200K token的处理窗口，未来还将扩展至超过一百万token，满足特定客户的需求。",

        "Claude 3模型在成本结构和潜在应用领域，特别是在客户互动、内容审核和多步骤指令执行方面具有很好的应用潜力，强调了其在提供快速准确支持和自然语言处理方面的优势。",

    ]

    # 循环文本列表，并生成对应的音频文件
    for i, text in enumerate(texts):
        filename = f"{i+1}.mp3"  # 文件命名为 1.mp3, 2.mp3, ...
        generate_audio(speech_config, text, filename)