# AI-Generated Video Creator

[English](README.md) | [简体中文](README_zh-CN.md)

This project is an AI-powered video creation tool that combines image generation, text-to-speech, and video editing to produce unique and engaging videos. By leveraging advanced AI technologies, this tool allows users to create videos with custom scenes and corresponding background commentary.

## Prerequisites

Before running the project, make sure you have the following:

- Discord account connected to Genmo (configure in `image_2_video_voice.py`)
- Azure API key for text-to-speech (configure in `test_2_speech.py`)
- OpenAI API key for image generation (configure in `test_2_image.py`)

## Usage

1. Configure the necessary API keys and account information in the corresponding files.
2. Define your custom scenes and background commentary in `image_2_video_rpa.py`.
3. Run `image_2_video_rpa.py` to generate the video.

Note: If you want to create a new video, make sure to clear the `audio_files` and `image_folder` directories before running the script again.

## Customization

In `image_2_video_rpa.py`, you can customize the scenes and background commentary by modifying the `my_scenes` and `my_texts` lists. Each scene should have a corresponding background commentary, ensuring a one-to-one correspondence between the visual and audio elements.

Example:
```python

# Define your own scenes

my_scenes = [
   "A chalkboard with mathematical equations, where the numbers blur and shift, illustrating the fluid nature of truth.",
   "A loom tangled with threads, half-finished tapestries hanging, symbolizing the complexity and mishaps in storytelling.",
   ...
]

# Generate images

generate_images(my_scenes)

# Define your own text

my_texts = [
   "In the dance of discernment, where two plus two may equal four or perhaps twenty-two,",
   "The weavers of tales, with their heavy hands, often stumble in their craft,",
   ...
]
```

## Example

Check out an example video created using this tool:

[![Example 1](https://i.ytimg.com/vi/zwETWcPaTog/maxresdefault.jpg)](https://www.youtube.com/watch?v=zwETWcPaTog "Example 1")
