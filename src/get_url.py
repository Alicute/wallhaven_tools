import os

dir_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录的绝对路径
parent_dir_path = os.path.join(dir_path, "..")  # 获取当前文件所在目录的上级目录的绝对路径
favorites_dir_path = os.path.join(parent_dir_path, "Favorites")  # 获取Favorites目录的绝对路径
txt_list = []
for root, dirs, files in os.walk(favorites_dir_path):
    for file in files:
        if file.endswith(".txt"):
            txt_path = os.path.join(root, file)
            print(txt_path)
            txt_list.append(txt_path)

print(txt_list)