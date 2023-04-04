# -*- coding: utf-8 -*-
import math
import os
import time
import requests
# 基础信息
from config_demo import ConfigSingleton

config = ConfigSingleton()
api_key = config.get_config("User","api_key")

"""
这个程序的主要功能为：获取用户的收藏夹，然后遍历该收藏夹所有的图片，并将图片的地址全部保存到本地
在此期间，会根据该用户有多少个收藏夹创建对应的文件夹，格式为：User-timestamp-collection-url.txt
当该用户的所有收藏夹的所有图片均被保存到本地后，会修改User-timestamp的时间戳文件夹，在后面加后缀——finished
表示拉取完成

"""


# 获取用户的公开收藏夹，存储收藏夹的名字、id、id下图片分页数量
def get_collection(user, api_key):
    url = f"https://wallhaven.cc/api/v1/collections/{user}?apikey={api_key}"
    print(url)
    response = requests.get(url)
    data = response.json()['data']
    collection_info = {}
    for collection in data:
        label = collection['label']
        collection_info[label] = {}
        collection_id = collection['id']
        collection_info[label][collection_id] = math.ceil(collection['count'] / 24)
    print(collection_info)
    return collection_info

# 根据收藏夹名字创建对应的文件夹，并在每个文件夹下创建url.txt记录该ID下的图片真实图片路径
def get_collection_id(collection_info):
    pic_info = collection_info
    for label, inner_dict in pic_info.items():
        print(label)
        print(inner_dict)
        # 创建文件夹
        if not os.path.exists(label):
            os.makedirs(label)
        if not os.path.exists(os.path.join(label, "url.txt")):
            open(os.path.join(label, "url.txt"), "w").close()


        # 获取收藏id下面的图片链接并保存到创建的文件中
        for collection_id, nums in inner_dict.items():
            for num in range(nums):
                print(num+1)
                url = f"https://wallhaven.cc/api/v1/collections/{user}/{collection_id}?purity=111&page={num+1}&apikey={api_key}"
                time.sleep(3)
                print(url)
                response = requests.get(url)
                data = response.json()['data']
                for i, img in enumerate(data):
                    url = img["path"]
                    print(url)
                    url_file = os.path.join(label, "url.txt")
                    if os.path.exists(url_file):
                        with open(url_file, "a") as f:
                            f.write(url + "\n")
                    else:
                        with open(url_file, "w") as f:
                            f.write(url + "\n")



if __name__ == '__main__':
    user = input("请输入你想要查询的用户： \n")
    collection_info = get_collection(user, api_key)
    get_collection_id(collection_info)
