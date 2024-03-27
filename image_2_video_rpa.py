# -*- coding: utf-8 -*-
import os
import time
from text_2_image import generate_images
from text_2_speech import generate_speech_from_texts
from video_creator.speed_change import adjust_video_speed
from video_creator.combine_video_voice import combine_videos_and_audios
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import re

# 全局 WebDriver 实例
from video_creator.text_2_speech import init_azure_speech_synthesizer

driver = None


def get_driver():
    global driver
    return driver


def open_browser_with_options(url, browser):
    global driver
    options = Options()

    # 防止自动化检测
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    # 创建WebDriver实例
    if browser == "chrome":
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
    else:
        raise ValueError("Browser type not supported")

    # 访问指定的URL
    driver.get(url)
    time.sleep(2)

def login_account():
    global driver
    # login in
    # 等待直到页面包含特定的class属性的元素
    class_name = "rounded-md"
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )

    # 定位login按钮
    login_buttons = driver.find_elements(By.CLASS_NAME, class_name)

    # 在找到的按钮中寻找包含“Login”文本的按钮
    for button in login_buttons:
        if "Login" in button.text:
            login_button = button
            break

    # 点击login按钮
    login_button.click()

    # 等待并点击 "Continue with Discord" 按钮
    class_name_for_discord = "items-center"  # 一个特征class名，用于定位"Continue with Discord"按钮
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name_for_discord))
    )

    discord_buttons = driver.find_elements(By.CLASS_NAME, class_name_for_discord)

    # 从找到的元素中寻找包含 "Continue with Discord" 文本的按钮
    for button in discord_buttons:
        if "Continue with Discord" in button.text:
            discord_button = button
            break

    # 点击 "Continue with Discord" 按钮
    discord_button.click()

    # 等待账号输入框出现
    email_input_xpath = "//input[@name='email']"
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, email_input_xpath))
    )

    # 定位账号输入框并输入账号
    email_input = driver.find_element(By.XPATH, email_input_xpath)
    email_input.send_keys("your dicord account that connect the genmo")  # 替换为你的账号

    # 定位密码输入框并输入密码
    password_input_xpath = "//input[@name='password']"
    password_input = driver.find_element(By.XPATH, password_input_xpath)
    password_input.send_keys("your password")  # 替换为你的密码

    # 定位登录按钮并点击
    login_button_xpath = "//button[.//div[text()='登录']]"
    login_button = driver.find_element(By.XPATH, login_button_xpath)
    login_button.click()

    # 等待用户确认并登陆成功
    logo_xpath = "/html/body/div[2]/div/div[4]/div[1]/h1/button/a/span"
    print("Success")
    WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.XPATH, logo_xpath))
    )


def numerical_sort(file_name):
    # Extract numbers from filename
    numbers = re.findall(r'\d+', file_name)
    return int(numbers[0]) if numbers else 0


def upload_image(file_path):
        global driver

        try:
            # Check for the presence of the Remove button
            time.sleep(10)
            remove_button = driver.find_element(By.XPATH, "//button[contains(., 'Remove')]")
            remove_button.click()
            print("Remove button clicked.")
        except NoSuchElementException:
            # If the Remove button is not found, do nothing
            print("Remove button not found, proceeding with upload.")
        # 找到文件上传的input元素
        file_input = driver.find_element(By.ID, "upload-image")
        file_input.send_keys(file_path)
        time.sleep(10)
        submit_button_xpath = "//button[.//span[text()='Submit']]"
        submit_button = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, submit_button_xpath))
        )
        submit_button.click()


def download_video(video_index,image_path):
    global driver

    # 获取初始状态下的所有视频URLs
    existing_video_urls = set()
    WebDriverWait(driver, 1000).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "source"))
    )

    existing_videos = driver.find_elements(By.TAG_NAME, "source")
    for video in existing_videos:
        src = video.get_attribute('src')
        if src:
            existing_video_urls.add(src)
            print(f"Existing video URL: {src}")

    # 图片上传逻辑...
    upload_image(image_path)

    # 定义一个新的等待条件，等待新的视频URL出现
    def video_url_has_changed(driver):
        video_elements = driver.find_elements(By.TAG_NAME, "source")
        for video in video_elements:
            src = video.get_attribute('src')
            # print(f"Checking video URL: {src}")
            if src and src not in existing_video_urls and "text_to_video_v3" in src:
                print(f"New video URL found: {src}")
                return src
        return False

    # 等待新的视频URL出现
    try:
        time.sleep(10)
        new_video_url = WebDriverWait(driver, 30000).until(video_url_has_changed)
    except TimeoutException:
        print("Timeout waiting for new video URL.")
        return
    # 如果视频URL找到了，就下载视频文件
    if new_video_url:
        print(f"Downloading video from {new_video_url}")

        # 发送HTTP GET请求下载视频
        response = requests.get(new_video_url)

        # 确保请求成功
        if response.status_code == 200:
            # 创建视频文件夹和构建视频文件的路径
            video_folder_path = os.path.join(os.getcwd(), "video_folder")
            if not os.path.exists(video_folder_path):
                os.makedirs(video_folder_path)

            # 设置视频文件的完整保存路径
            video_file_name = f"{video_index}.mp4"  # Name the file based on video_index
            video_file_path = os.path.join(video_folder_path, video_file_name)

            # 写入视频文件内容
            with open(video_file_path, 'wb') as file:
                file.write(response.content)
            print(f"Video successfully downloaded to {video_file_path}")
        else:
            print(f"Failed to download video, status code: {response.status_code}")
    else:
        print("Video URL not found")



def main():

    # 初始化 Azure TTS 配置
    subscription_key = "your Azure TTS key"
    subscription_region = "eastus"
    speech_config = init_azure_speech_synthesizer(subscription_key, subscription_region)

    # 定义自己的场景
    my_scenes = [
        "A chalkboard with mathematical equations, where the numbers blur and shift, illustrating the fluid nature of truth.",
        "A loom tangled with threads, half-finished tapestries hanging, symbolizing the complexity and mishaps in storytelling.",
        "A spider web glistening in the morning light, with the spider caught in its own creation, representing self-entrapment.",
        "An open book with pages that seem to reflect rather than absorb the light, suggesting the allure of fabricated stories.",
        "A masquerade ball where masks float without wearers, representing the deceptive facades people wear.",
        "A pathway made of broken mirrors, each reflecting a distorted fragment of the sky, symbolizing fragmented truths.",
        "A lantern glowing softly in a foggy twilight, guiding the way through obscured paths, embodying vigilance.",
        "A shattered stained glass window beside an intact one, showing the fragility and beauty of trust.",
        "An open book with illustrations of a child's life, representing the hero's backstory.",
        "A phoenix rising from ashes in a painting, symbolizing triumph over adversity.",
        "A dance floor where shadows and figures merge and part under a flickering light, illustrating the interplay of truth and deceit.",
        "A knife with a honey-coated blade, representing the dual nature of truth as both harmful and enticing.",
        "A desert with a single, flourishing mirage in the distance, symbolizing the pursuit of comforting illusions.",
        "A cradle in a moonlit room, gently rocking by an unseen force, conveying the peace brought by lies."
    ]
    # 生成图片
    generate_images(my_scenes)

    # 定义自己的文本
    my_texts = [
        "In the dance of discernment, where two plus two may equal four or perhaps twenty-two,",
        "The weavers of tales, with their heavy hands, often stumble in their craft,",
        "Yet, paradoxically, find themselves ensnared in webs of their own design,",
        "Believing with ease the very fictions they spin for others.",
        "Beware the half-truths and the silver-tongued, for deception wears many masks,",
        "Not all lies are spoken; the most cunning deceit is dressed in fragments of truth,",
        "A mosaic crafted with care, meant to mislead, to bewilder, to ensnare.",
        "Vigilance is the lantern in the dark, for even the closest of friends may harbor shadows,",
        "Trust, once shattered, transforms sanctuary into a field of glass,",
        "Where every step forward is a question, every word a potential double-edged sword.",
        "In the realm of human connection, truth and falsehood dance a delicate ballet,",
        "The truth, with its sharp edges, often cuts deeper than the lie's sweetest honey,",
        "Yet, we chase the illusion, a mirage of comfort in a desert of uncertainty,",
        "For sometimes, the lie is the lullaby that soothes our restless spirits."
    ]

    # 生成语音
    generate_speech_from_texts(my_texts, speech_config)

    # 然后上传图片并下载视频
    image_folder_path = os.path.join(os.getcwd(), "image_folder")  # Path to the folder containing images
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.png')]  # List all .png files
    image_files.sort(key=numerical_sort)
    video_counter = 1  # Initialize a counter for naming videos

    for image_file in image_files:
        image_path = os.path.join(image_folder_path, image_file)
        print(f"Uploading {image_file}...")
        download_video(video_counter,image_path)  # Download video with a specific name
        video_counter += 1  # Increment counter after each download

    # 下载视频文件后，调整视频速度
    adjust_video_speed()

    # 调整视频速度并下载视频文件后，组合视频和音频
    combine_videos_and_audios(video_name = "gushi_2.mp4")

if __name__ == "__main__":
    url = "https://www.genmo.ai/create/video"
    browser_type = "chrome"
    open_browser_with_options(url, browser_type)
    login_account()
    # main()
    # 然后上传图片并下载视频
    image_folder_path = os.path.join(os.getcwd(), "image_folder")  # Path to the folder containing images
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.png')]  # List all .png files
    image_files.sort(key=numerical_sort)
    video_counter = 1  # Initialize a counter for naming videos

    for image_file in image_files:
        image_path = os.path.join(image_folder_path, image_file)
        print(f"Uploading {image_file}...")
        download_video(video_counter,image_path)  # Download video with a specific name
        video_counter += 1  # Increment counter after each download

    # 下载视频文件后，调整视频速度
    adjust_video_speed()

    # 调整视频速度并下载视频文件后，组合视频和音频
    combine_videos_and_audios(video_name = "gushi_2.mp4")







