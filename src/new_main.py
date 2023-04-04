import os
import requests
import time
import math
from config_demo import ConfigSingleton

"""
这个程序的主要功能为：获取用户的收藏夹，然后遍历该收藏夹所有的图片，并将图片的地址全部保存到本地
在此期间，会根据该用户有多少个收藏夹创建对应的文件夹，格式为：User-timestamp-collection-url.txt
当该用户的所有收藏夹的所有图片均被保存到本地后，会修改User-timestamp的时间戳文件夹，在后面加后缀——finished
表示拉取完成

"""

config = ConfigSingleton()
api_key = config.get_config("User","api_key")
init_path = []


def mkdir_init():
    """通过一个全局变量列表来装父路径，保证程序运行时只有一个时间戳路径，多次运行时存在多个时间戳路径"""
    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir_path = os.path.join(dir_path, "../Favorites")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    new_dir_path = os.path.join(parent_dir_path, user, time_str)
    init_path.append(new_dir_path)


def mkdir_fav(label):
    """创建收藏夹对应的目录"""
    label_dir_path = os.path.join(init_path[0], label)
    os.makedirs(label_dir_path, exist_ok=True)
    return label_dir_path


def get_collection(user, api_key):
    """获取用户的公开收藏夹"""
    url = f"https://wallhaven.cc/api/v1/collections/{user}?apikey={api_key}"
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}
    data = response.json().get('data', [])
    collection_info = {}
    for collection in data:
        label = collection.get('label', '')
        collection_id = collection.get('id', '')
        count = collection.get('count', 0)
        if label and collection_id:
            collection_info[label] = {collection_id: math.ceil(count / 24)}
    print(collection_info)
    return collection_info


def get_collection_id(collection_info):
    """根据收藏夹名字创建对应的文件夹，并在每个文件夹下创建url.txt记录该ID下的图片真实图片路径"""
    for label, inner_dict in collection_info.items():
        base_url_file_path = mkdir_fav(label)
        for collection_id, nums in inner_dict.items():
            for num in range(nums):
                print(f"{num + 1}/{nums}")
                url = f"https://wallhaven.cc/api/v1/collections/{user}/{collection_id}?purity=111&page={num + 1}&apikey={api_key}"
                time.sleep(3)
                print(url)
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
                    continue
                data = response.json().get('data', [])
                url_file = os.path.join(base_url_file_path, f"{collection_id}.txt")
                with open(url_file, "a", encoding="utf-8") as f:
                    for img in data:
                        url = img.get("path", "")
                        if url:
                            f.write(url + "\n")
                print(f"Saved {len(data)} image urls to {url_file}")


if __name__ == '__main__':
    """想要查询的用户的名字"""
    user = input("请输入你想要查询的用户： \n")
    """初始化父路径"""
    mkdir_init()
    """抓取收藏夹图片的路径"""
    collection_info = get_collection(user, api_key)
    get_collection_id(collection_info)
    """进行标志，修改已完成文件夹名字"""
    finish_flag = init_path[0]+"_finished"
    os.rename(init_path[0], finish_flag)
