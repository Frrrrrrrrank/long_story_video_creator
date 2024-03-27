import os
import ffmpeg

def concatenate_videos(video_list, output_path):
    # Create a temporary text file for FFmpeg to read the list of videos
    with open('concat_list.txt', 'w') as f:
        for video in video_list:
            f.write(f"file '{video}'\n")

    # Concatenate videos using FFmpeg
    ffmpeg.input('concat_list.txt', format='concat', safe=0).output(output_path, c='copy').run()

    # Remove the temporary file
    os.remove('concat_list.txt')

def combine_videos_and_audios(video_name, video_folder="video_folder", audio_folder="audio_files", output_folder="finished_video"):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the subfolder for the completed video
    complete_video_folder = os.path.join(output_folder, "complete_video")
    if not os.path.exists(complete_video_folder):
        os.makedirs(complete_video_folder)

    # Get the adjusted video files
    adjusted_video_files = [f for f in os.listdir(video_folder) if f.startswith('adjusted_') and f.endswith('.mp4')]
    final_videos = []  # List to keep track of the final video files

    # For each adjusted video file, find the corresponding audio file and merge
    for video_file in adjusted_video_files:
        prefix = os.path.splitext(video_file)[0].replace('adjusted_', '')  # Get the original file name prefix
        audio_file = f"{prefix}.mp3"
        audio_path = os.path.join(audio_folder, audio_file)

        # If the corresponding audio file exists
        if os.path.isfile(audio_path):
            video_path = os.path.join(video_folder, video_file)
            output_path = os.path.join(output_folder, f"final_{prefix}.mp4")
            final_videos.append(output_path)  # Add the path to the list

            # Use FFmpeg to merge video and audio
            ffmpeg.input(video_path).output(
                ffmpeg.input(audio_path),
                output_path,
                vcodec='copy',  # Copy the video codec
                acodec='aac',  # Use AAC audio codec
                strict='experimental'  # Use experimental features if needed
            ).run()

    print("All videos and audios have been combined.")

    # Concatenate all final videos into one
    final_output_path = os.path.join(complete_video_folder, video_name)
    concatenate_videos(final_videos, final_output_path)

    print(f"All videos have been concatenated into {final_output_path}.")

# Example usage:
# combine_videos_and_audios()
