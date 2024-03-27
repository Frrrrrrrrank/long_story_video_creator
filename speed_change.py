import os
import subprocess
import ffmpeg


def adjust_video_speed(video_folder="video_folder", audio_folder="audio_files"):
    # 获取文件夹中所有视频和音频文件
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

    # 按文件名前缀配对视频和音频文件
    paired_files = []
    for video_file in video_files:
        prefix = os.path.splitext(video_file)[0]  # 获取不带扩展名的文件名
        audio_file = f"{prefix}.mp3"
        if audio_file in audio_files:
            paired_files.append((video_file, audio_file))

    # 计算文件的时长
    def get_duration(filename):
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)

    # 调整视频速度以匹配音频时长
    for video, audio in paired_files:
        video_path = os.path.join(video_folder, video)
        audio_path = os.path.join(audio_folder, audio)

        video_duration = get_duration(video_path)
        audio_duration = get_duration(audio_path)
        speed_factor = audio_duration / video_duration

        # 构建 FFmpeg 命令
        (
            ffmpeg
            .input(video_path)
            .filter_('setpts', '{}*PTS'.format(speed_factor))
            .output(os.path.join(video_folder, f"adjusted_{video}"))
            .run()
        )
