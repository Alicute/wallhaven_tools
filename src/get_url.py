import os
"""
获取收集、下载、喜欢的文件夹下面的txt文件路径，方便调试

"""

def get_dir_path():
    dir_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录的绝对路径
    parent_dir_path = os.path.join(dir_path, "..")  # 获取当前文件所在目录的上级目录的绝对路径
    favorites_dir_path = os.path.join(parent_dir_path, "Favorites")  # 获取Favorites目录的绝对路径
    condition_dir_path = os.path.join(parent_dir_path, "Condition_Result")  # 获取Favorites目录的绝对路径
    txt_list = []
    for dir_path in [favorites_dir_path,condition_dir_path]:
        for root, dirs, files in os.walk((dir_path)):
            for file in files:
                if file.endswith(".txt"):
                    txt_path = os.path.join(root, file)
                    # print(txt_path)
                    txt_list.append(txt_path)
    return txt_list


if __name__ == '__main__':

    arr = get_dir_path()
    print('\n'.join(arr))
