# -*- coding: utf-8 -*-
import math
import os.path
import random
import re
import time

import requests
import json
from src import myconfig

all_image_paths = []  # 创建空列表存储所有图片路径
# 构造请求 URL
init_path = []
# 获取api_key
api_key = myconfig.ConfigSingleton().api_key()
proxies = myconfig.con_str_to_dict(myconfig.ConfigSingleton().get_proxy())
level = myconfig.ConfigSingleton().set_level()
print(level)


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
    with open(cond_file_path, 'a+') as f:
        pass
    return cond_file_path


def send_req(stars=100):  # 三个1分别代表了SFW、Sketchy、NSFW，如001将会查找不宜展示的图片
    for num in range(20):
        # time.sleep(3)
        resolutions = [
            "640x480", "800x600", "1024x768", "1152x864", "1280x720", "1280x768",
            "1280x800", "1280x960", "1280x1024", "1360x768", "1366x768", "1400x1050",
            "1440x900", "1600x900", "1600x1200", "1680x1050", "1920x1080", "1920x1200",
            "2048x1152", "2560x1080", "2560x1440", "3440x1440", "3840x2160"
        ]
        only_good_resolutions = [
            "2048x1152", "2560x1080", "2560x1440", "3440x1440", "3840x2160"
        ]
        ratios = [
            "1x1", "4x3", "5x4", "16x9", "16x10", "21x9", "32x9", "32x10", "48x9", "48x10"
        ]
        only_use_ratios = [
             "16x9", "16x10", "21x9",  "9x16","9x18", "10x16"
        ]
        """
        默认请求链接是100收藏数以上、等级自己设定，分辨率和屏幕比例是随机的
        """
        url = f"https://wallhaven.cc/api/v1/search?favorites={stars}&purity={level}&atleast={random.choice(only_good_resolutions)}&ratios={random.choice(only_use_ratios)}&page={num + 1}&apikey={api_key} "
        # "https://wallhaven.cc/search?categories=111&purity=100&ratios=9x16&sorting=favorites&order=desc&page=2"
        # 其他参数：&topRange=1y&sorting=toplist&order=desc&ai_art_filter=1
        pattern = r"search\?(.*)\&page"
        # 匹配搜索条件并以此作为创建文本文件的名字
        match = re.search(pattern, url)
        file_path = cond_file_dir(match.group(1))
        print(url)
        try:
            response = requests.request(method="GET", url=url, proxies=proxies )
            data = json.loads(response.content)
            print(f"{(num + 1)}/{math.ceil(data['meta']['total'] / 24) + 1}")
            if not data['data']:
                print(f"第 {num + 1} 页没有数据，程序已停止。")
                continue
            # 提取 data[path] 字段
            image_paths = [item['path'] for item in data['data']]
            # 写入大列表
            all_image_paths.extend(image_paths)
            with open(file_path, 'a+') as f:
                for path in image_paths:
                    f.write(path + '\n')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    mkdir_init()
    send_req()