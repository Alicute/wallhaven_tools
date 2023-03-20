# -*- coding: utf-8 -*-
import math
import os
import time

import requests

# 基础信息
api_key = "mprbYShCTmcuUxIpUV2hpDhU3PvCbYiC"
user = "11tangsong"




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
    collection_info = get_collection("11tangsong", api_key)
    get_collection_id(collection_info)
