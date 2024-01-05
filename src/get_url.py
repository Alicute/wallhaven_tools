import os

"""
获取收集、下载、喜欢的文件夹下面的txt文件路径，方便查看，用于其他功能的使用

"""


def get_dir_path():
    dir_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录的绝对路径
    parent_dir_path = os.path.join(dir_path, "..")  # 获取当前文件所在目录的上级目录的绝对路径
    favorites_dir_path = os.path.join(parent_dir_path, "Favorites")  # 获取Favorites目录的绝对路径
    condition_dir_path = os.path.join(parent_dir_path, "Condition_Result")  # 获取Favorites目录的绝对路径
    txt_list = []
    for dir_path in [favorites_dir_path, condition_dir_path]:
        for root, dirs, files in os.walk((dir_path)):
            for file in files:
                if file.endswith(".txt"):
                    txt_path = os.path.join(root, file)
                    # print(txt_path)
                    txt_list.append(txt_path)
    return txt_list


def create_merge_txt(arr):
    target_file = '../merged.txt'
    with open(target_file, 'w', encoding='utf-8') as f:
        for file_path in arr:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                f.write(content)
            f.write('\n\n\n')
    print("↓↓↓↓↓↓↓↓↓---合并后的全部图片URL的文件路径,可能会很多很多，不建议在多次搜索和收藏后直接下载该文件---↓↓↓↓↓↓↓↓↓\n{}".format(os.path.abspath(target_file)))

if __name__ == '__main__':
    arr = get_dir_path()
    print('\n'.join(arr))
    create_merge_txt(arr)
