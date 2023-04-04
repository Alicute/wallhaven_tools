# -*- coding: utf-8 -*-
import math
import os.path
import re
import time

import requests
import json

api_key = "mprbYShCTmcuUxIpUV2hpDhU3PvCbYiC"
all_image_paths = []  # 创建空列表存储所有图片路径
# 构造请求 URL
init_path = []


def mkdir_init():
    """通过一个全局变量列表来装父路径，保证程序运行时只有一个时间戳路径，多次运行时存在多个时间戳路径"""
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    print(dir_path)
    parent_dir_path = os.path.join(dir_path, "../Condition_Result")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    new_dir_path = os.path.join(parent_dir_path, time_str)
    os.makedirs(new_dir_path)
    init_path.append(new_dir_path)


def cond_file_dir(cond_name):
    cond_file_path = os.path.join(init_path[0], f"{cond_name}_url.txt")
    with open(cond_file_path,'a+') as f:
        pass
    return cond_file_path


def send_req():
    for num in range(100):
        time.sleep(3)
        url = f"https://wallhaven.cc/api/v1/search?favorites=100&purity=001&atleast=3840x2160&ratios=9x16&page={num + 1}&apikey={api_key}"
        # "https://wallhaven.cc/search?categories=111&purity=100&ratios=9x16&sorting=favorites&order=desc&page=2"
        pattern = r"search\?(.*)\&page"
        match = re.search(pattern, url)
        file_path = cond_file_dir(match.group(1))
        print(url)
        # 发送 HTTP 请求并获取响应
        response = requests.get(url)
        # 将响应内容解析为 JSON 格式
        data = json.loads(response.content)
        print(f"{(num +1)}/{math.ceil(data['meta']['total']/ 24)+1}")
        if not data['data']:
            print(f"第 {num + 1} 页没有数据，程序已停止。")
            break
        # 提取 data[path] 字段
        image_paths = [item['path'] for item in data['data']]
        # 写入大列表
        all_image_paths.extend(image_paths)
        with open(file_path, 'a+') as f:
            for path in image_paths:
                f.write(path + '\n')

if __name__ == '__main__':
    mkdir_init()
    send_req()
