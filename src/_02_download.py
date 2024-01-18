import concurrent.futures

import os
import time

import requests
from tqdm import tqdm
from common import get_dir_path
from src import myconfig
from src.basic import CompareImageUrl


"""
主要功能：下载_01_search.py获取到的图片，运行之前建议使用basic.py文件，会将所有的图片放到总图片文件夹中去
然后便利图片名字并存入sqlite中，再次与本地所有url进行对比，如果该url中包含任一sql结果，则剔除
将过滤后的url写入merged.txt文件中，并通过多线程的方式下载这些url
"""


init_path = []
_, cookies = myconfig.ConfigSingleton().get_mysession()
proxies = myconfig.con_str_to_dict(myconfig.ConfigSingleton().get_proxy())


def down_mkdir_init():
    """通过一个全局变量列表来装父路径，保证程序运行时只有一个时间戳路径，多次运行时存在多个时间戳路径，所以每次运行本文件均会创建一个文件夹"""
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    parent_dir_path = os.path.join(dir_path, "../Download_img")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    new_dir_path = os.path.join(parent_dir_path, time_str)
    os.makedirs(new_dir_path)
    init_path.append(new_dir_path)
    return parent_dir_path


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
    # 将每一次下载的图片放到总的文件夹内进行过滤，如果不希望移动，也可以注释掉
    # CompareImageUrl.move_pic_to_all_pictures()
    cin = CompareImageUrl()
    cin.before_download_checkurl()
    urlpath = input("请复制上述你准备下载的地址然后粘贴到下面进行下载:\n")
    with open(urlpath, "r") as f:
        lines = f.readlines()
    url_dict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in map(str.strip, lines):
            fut = executor.submit(download_img, url)
            futures.append(fut)
            url_dict[fut] = url
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")
                url = url_dict[future]
                retry_download(url)


def retry_download(url):
    # 重新提交下载任务的逻辑
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(download_img, url)
        try:
            future.result()
        except Exception as e:
            print(f"Error: {e}")


def download_img(url):
    # 下载图片并保存到本地文件
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,en;q=0.9,zh-CN;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }
    response = requests.request(method="GET", url=url, headers=headers,stream=True, proxies=proxies)
    response.raise_for_status()  # 检查请求是否成功
    id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
    type = url.split("/")[-1].split(".")[1]
    cond_file_path = os.path.join(init_path[0], f"{id}.{type}")
    with open(cond_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)


def dir_is_none_to_del():
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    parent_dir_path = os.path.join(dir_path, "../Download_img")
    return parent_dir_path


def is_folder_empty(folder_path):
    # 列出文件夹中的所有文件和子文件夹
    contents = os.listdir(folder_path)

    for item in contents:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # 如果是子文件夹，递归调用 is_folder_empty() 函数检查是否为空
            if not is_folder_empty(item_path):
                return False
        else:
            # 如果是文件，则说明文件夹不为空，返回 False
            return False

    # 文件夹为空
    return True


def delete_empty_folders(folder_path):
    # 列出文件夹中的所有文件和子文件夹
    contents = os.listdir(folder_path)

    for item in contents:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # 如果是子文件夹，递归调用 delete_empty_folders() 函数删除空文件夹
            delete_empty_folders(item_path)

    # 判断文件夹是否为空
    if is_folder_empty(folder_path):
        # 如果文件夹为空，删除该文件夹
        os.rmdir(folder_path)


# 删除空文件夹
def deldeldeldel_empty_dir():
    dir_path = dir_is_none_to_del()
    delete_empty_folders(dir_path)


if __name__ == '__main__':
    down_mkdir_init()
    get_url()
    # 需要删除空文件夹时，运行即可
    # deldeldeldel_empty_dir()
