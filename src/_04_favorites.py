# -*- coding: utf-8 -*-
import os
import time
from common import get_dir_path
import requests
import myconfig

"""
此文件是作为将收集到的url添加到自己的收藏中去

"""

coll = myconfig.ConfigSingleton().get_coll()
token, mysession = myconfig.ConfigSingleton().get_mysession()
proxies = myconfig.con_str_to_dict(myconfig.ConfigSingleton().get_proxy())
"""
获取喜欢的文件夹内的txt文件内存储的url
"""


def fav_add_url():
    print("\n".join(get_dir_path()))
    print("收藏前请确认好自己的收藏夹id、cookie、token是否填写正确")
    urlpath = input("请复制上述地址然后粘贴到下面进行收藏:\n")
    with open(urlpath, "r") as f:
        lines = f.readlines()
    return lines


"""
将url通过post请求添加到like中去，需要指定collection的id和token
"""


def other_to_like():
    con = myconfig.ConfigSingleton()
    arr = fav_add_url()
    num = len(arr)
    for i, line in enumerate(arr):
        url = line.strip()
        id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
        add_url = f"https://wallhaven.cc/favorites/add?wallHashid={id}&collectionId={coll}&_token={token}"
        try:
            res = mysession.post(url=add_url, proxies=myconfig.con_str_to_dict(con.config.get("User", "proxy")))
            print(f"已完成{i + 1}/{num}>>>>>>{add_url}>>>>>>{res.status_code}")
            time.sleep(2)
        except Exception as e:
            print(e)


def add_pic_to_like():
    arr = fav_add_url()
    num = len(arr)
    for i, line in enumerate(arr):
        url = line.strip()
        id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
        add_url = f"https://wallhaven.cc/favorites/add?wallHashid={id}&collectionId={coll}&_token={token}"
        headers = {
            "content-type": "application/json"
        }
        try:
            res = requests.request(method="POST", url=add_url, headers=headers, proxies=proxies,
                                   cookies=mysession.cookies)
            print(f"已完成{i + 1}/{num}>>>>>>{add_url}>>>>>>{res.status_code}")
            time.sleep(2)  # 太快了会导致链接错误
        except Exception as e:
            print(e)


def just_copy_then_gogogogogogo():
    copy_token = myconfig.ConfigSingleton().get_copy_token()  # 随便收藏一张图片，F12把请求后面的token复制过来
    copy_cookies = myconfig.con_str_to_dict(myconfig.ConfigSingleton().get_copy_cookies())  # 你的cookie，从浏览器直接复制的
    arr = fav_add_url()
    num = len(arr)
    for i, line in enumerate(arr):
        url = line.strip()
        wallHashid = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
        add_url = f"https://wallhaven.cc/favorites/add?wallHashid={wallHashid}&collectionId={coll}&_token={copy_token}"
        try:
            res = requests.request(method="POST", url=add_url, proxies=proxies, cookies=copy_cookies)
            print(f"已完成{i + 1}/{num}>>>>>>{add_url}>>>>>>{res.status_code}")
            time.sleep(2)  # 太快了会导致链接错误
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # other_to_like()  # session传递有点问题，看着能用，其实一点用都没用

    just_copy_then_gogogogogogo()  # 纯享手动版，lets go!
