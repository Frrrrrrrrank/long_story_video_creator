import requests
import os

# 在脚本中设置环境变量
os.environ['OPENAI_API_KEY'] = 'your openai key'
os.environ['OPENAI_BASE_URL'] = 'OPENAI_BASE_URL'
def download_image(url, folder_path, file_name):
    response = requests.get(url)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as file:
        file.write(response.content)
    return file_path

def generate_images(scenes):
    model_name = "dall-e-3"
    image_size = "1024x1024"

    # 程序所在文件夹的路径
    current_directory = os.getcwd()
    image_subfolder = os.path.join(current_directory, "image_folder")

    # 如果子文件夹不存在，则创建
    if not os.path.exists(image_subfolder):
        os.makedirs(image_subfolder)

    for i, prompt in enumerate(scenes):
        try:
            print(f"正在为 '{prompt}' 生成图片，请耐心等待……")
            response = requests.post(
                os.environ["OPENAI_BASE_URL"] + "/v1/images/generations",
                headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                json={"model": model_name, "size": image_size, "prompt": prompt, "n": 1},
            )
            response.raise_for_status()
            data = response.json()["data"]

            image_url = data[0]["url"]
            file_name = f"{i+1}.png"
            download_image(image_url, image_subfolder, file_name)
            print(f"图片 '{file_name}' 已下载至：", os.path.join(image_subfolder, file_name))

        except requests.exceptions.HTTPError as err:
            print("请求错误：", err.response.text)

        except Exception as e:
            print("发生错误：", str(e))

if __name__ == "__main__":
    model_name = "dall-e-3"
    image_size = "1024x1024"

    # 程序所在文件夹的路径
    current_directory = os.getcwd()
    image_subfolder = os.path.join(current_directory, "image_folder")

    # 如果子文件夹不存在，则创建
    if not os.path.exists(image_subfolder):
        os.makedirs(image_subfolder)

    # 你的场景描述
    scenes = [
        "图像显示一片古老的山林，薄雾缭绕，远处隐约可以看到狰的身影。",
        "镜头聚焦于狰的面容，展示其虎一般的面孔，尖锐的虎牙和发光的大眼睛。",
        "展示狰的全身，突出其庞大而强壮的体型和浓密的黑色毛发。",

        "画面展示狰在森林中迅速奔跑的情景，或在岩石上敏捷攀爬。",

        "聚焦于狰的尾巴，展示其粗壮和布满骨刺的特征。",

        "狰用尾巴猛烈地击打地面，引起震动和声响。",

        "镜头拉远，显示狰在山林中的守护姿态，彰显其威严与神秘。",

        "将狰置于古代传说的背景中，展示其在故事中的形象。",

        "图像展现古代人们围观狰，脸上流露出敬畏和好奇的神情。",

        "最后的画面是狰在月光下的身影，隐喻着它在中国神话中的永恒地位。"
    ]

    for i, prompt in enumerate(scenes):
        try:
            print(f"正在为 '{prompt}' 生成图片，请耐心等待……")
            response = requests.post(
                os.environ["OPENAI_BASE_URL"] + "/v1/images/generations",
                headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                json={"model": model_name, "size": image_size, "prompt": prompt, "n": 1},
            )
            response.raise_for_status()
            data = response.json()["data"]

            image_url = data[0]["url"]
            file_name = f"{i+1}.png"
            download_image(image_url, image_subfolder, file_name)
            print(f"图片 '{file_name}' 已下载至：", os.path.join(image_subfolder, file_name))

        except requests.exceptions.HTTPError as err:
            print("请求错误：", err.response.text)

        except Exception as e:
            print("发生错误：", str(e))
