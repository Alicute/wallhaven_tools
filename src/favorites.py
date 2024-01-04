# -*- coding: utf-8 -*-
import os
import time
from get_url import get_dir_path
import requests
import myconfig

"""
此文件是作为将收集到的url添加到自己的收藏中去,这里有点问题，发送的POST状态成功了，但是操作没成功，此处需要重新编写逻辑
"""

# coll和token需要手动去创建一个collection，然后随意添加一个图片到该collection，查看post请求的参数
coll = myconfig.ConfigSingleton().get_coll()
token = myconfig.ConfigSingleton().get_live_cookie()[1]
cookies = myconfig.ConfigSingleton().get_live_cookie()[0]
proxies = myconfig.con_str_to_dict(myconfig.ConfigSingleton().get_proxy())
"""
获取喜欢的文件夹内的txt文件内存储的url
"""
def fav_add_url():
    print("\n".join(get_dir_path()))
    urlpath = input("请复制上述地址然后粘贴到下面进行收藏:\n")
    with open(urlpath, "r") as f:
        lines = f.readlines()
    return lines

"""
将url通过post请求添加到like中去，需要指定collection的id和token
"""
def add_pic_to_like():
    arr = fav_add_url()
    num = len(arr)
    for i, line in enumerate(arr):
        url = line.strip()
        id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
        add_url = f"https://wallhaven.cc/favorites/add?wallHashid={id}&collectionId={coll}&_token={token}"
        try:
            res = requests.request(method="POST", url=add_url, proxies=proxies,cookies=cookies)
            print(f"已完成{i + 1}/{num}>>>>>>{add_url}>>>>>>{res.status_code}")
            time.sleep(2) #太快了会导致链接错误
        except Exception as e:
            print(e)


if __name__ == '__main__':
    add_pic_to_like()