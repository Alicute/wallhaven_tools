# -*- coding: utf-8 -*-
import os
import time
from get_url import get_dir_path
import requests
import config

"""
此文件是作为将收集到的url添加到自己的收藏中去,这里有点问题，发送的POST状态成功了，但是操作没成功，此处需要重新编写逻辑
"""

# coll和token需要手动去创建一个collection，然后随意添加一个图片到该collection，查看post请求的参数
coll = 1664329
token = config.ConfigSingleton().get_token()

proxies = {
    "http": "127.0.0.1:7890",
    "https": "127.0.0.1:7890",
}

"""
获取喜欢的文件夹内的txt文件内存储的url
"""
def fav_add_url():
    file_arr = get_dir_path()
    fav_paths = [file_path for file_path in file_arr if "Favorites" in file_path]
    preadd_url = []
    for fav_path in fav_paths:
        with open(fav_path, "r") as f:
            lines = f.readlines()
            preadd_url = preadd_url + lines
    return preadd_url

"""
将url通过post请求添加到like中去，需要指定collection的id和token
"""
def add_pic_to_like():
    num = len(fav_add_url())
    for i, line in enumerate(fav_add_url()):
        url = line.strip()
        id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
        add_url = f"https://wallhaven.cc/favorites/add?wallHashid={id}&collectionId={coll}&_token={token}"
        try:
            res = requests.request(method="POST", url=add_url, proxies=proxies)
            print(res.text)
            print(f"已完成{i + 1}/{num}>>>>>>{add_url}>>>>>>{res.status_code}")
            time.sleep(2) #太快了会导致链接错误
        except Exception as e:
            print(e)


if __name__ == '__main__':
    add_pic_to_like()