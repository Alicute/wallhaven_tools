import concurrent.futures

import os
import time

import requests
from tqdm import tqdm

init_path = []

def mkdir_init():
    """通过一个全局变量列表来装父路径，保证程序运行时只有一个时间戳路径，多次运行时存在多个时间戳路径"""
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    parent_dir_path = os.path.join(dir_path, "../Download_img")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    new_dir_path = os.path.join(parent_dir_path, time_str)
    print(new_dir_path)
    os.makedirs(new_dir_path)
    init_path.append(new_dir_path)
# 图片的 URL
def get_url():
    urlpath = input("请输入想要下载的url文本地址：")
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
    response = requests.get(url, stream=True)
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
