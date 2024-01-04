import concurrent.futures

import os
import time

import requests
from tqdm import tqdm
from get_url import get_dir_path
init_path = []


def mkdir_init():
    """通过一个全局变量列表来装父路径，保证程序运行时只有一个时间戳路径，多次运行时存在多个时间戳路径，所以每次运行本文件均会创建一个文件夹"""
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    parent_dir_path = os.path.join(dir_path, "../Download_img")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    new_dir_path = os.path.join(parent_dir_path, time_str)
    os.makedirs(new_dir_path)
    init_path.append(new_dir_path)


# 图片的 URL
def get_url():
    # dir_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录的绝对路径
    # parent_dir_path = os.path.join(dir_path, "..")  # 获取当前文件所在目录的上级目录的绝对路径
    # favorites_dir_path = os.path.join(parent_dir_path, "Favorites")  # 获取Favorites目录的绝对路径
    # for root, dirs, files in os.walk(favorites_dir_path):
    #     for file in files:
    #         if file.endswith(".txt"):
    #             txt_path = os.path.join(root, file)
    #             print(txt_path)
    print("\n".join(get_dir_path()))
    urlpath = input("请复制上述你准备下载的地址然后粘贴到下面进行下载\n>>>>>【Favorites】OR【Condition】>>>>>>\n")
    with open(urlpath, "r") as f:
        lines = f.readlines()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in map(str.strip, lines):
            futures.append(executor.submit(download_img, url))
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")


def download_img(url):
    # 下载图片并保存到本地文件
    proxies = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890",
    }
    response = requests.request(method="GET", url=url,stream=True, proxies=proxies)
    response.raise_for_status()  # 检查请求是否成功
    id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
    type = url.split("/")[-1].split(".")[1]
    cond_file_path = os.path.join(init_path[0], f"{id}.{type}")
    with open(cond_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


if __name__ == '__main__':
    mkdir_init()
    get_url()