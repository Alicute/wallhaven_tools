import os
import shutil


def get_download_path():
    dir_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录的绝对路径
    parent_dir_path = os.path.join(dir_path, "..")  # 获取当前文件所在目录的上级目录的绝对路径
    download_dir_path = os.path.join(parent_dir_path, "Download_img")  # 获取Favorites目录的绝对路径
    down_dirs = [os.path.join(download_dir_path, f) for f in os.listdir(download_dir_path) if
                 os.path.isdir(os.path.join(download_dir_path, f))]
    print(down_dirs)
    my_pic = os.path.join(download_dir_path, "1_All_Pictures")
    os.makedirs(os.path.join(my_pic), exist_ok=True)
    for source_dir in down_dirs:
        # 获取源文件夹中所有jpg文件的路径列表
        file_list = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(('.jpg', '.png'))]
        for file_path in file_list:
            try:
                shutil.move(file_path, my_pic)
            except:
                pass
    for i in range(1, len(down_dirs)):
        os.rmdir(down_dirs[i])


if __name__ == '__main__':
    get_download_path()
