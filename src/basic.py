import os
import shutil
import sqlite3

# 文件夹路径和文本文件路径
from src.common import get_dir_path, return_all_url


class CompareImageUrl:
    folder_path = r'../Download_img/1_All_Pictures'
    txt_path = r'../merged.txt'
    db_path = '../database.db'

    @staticmethod
    def move_pic_to_all_pictures():
        dir_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件所在目录的绝对路径
        parent_dir_path = os.path.join(dir_path, "..")  # 获取当前文件所在目录的上级目录的绝对路径
        download_dir_path = os.path.join(parent_dir_path, "Download_img")  # 获取Favorites目录的绝对路径
        down_dirs = [os.path.join(download_dir_path, f) for f in os.listdir(download_dir_path) if
                     os.path.isdir(os.path.join(download_dir_path, f))]
        print('\n'.join(down_dirs))
        my_pic = os.path.join(download_dir_path, "1_All_Pictures")
        os.makedirs(os.path.join(my_pic), exist_ok=True)
        for source_dir in down_dirs:
            # 获取源文件夹中所有jpg文件的路径列表
            file_list = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(('.jpg', '.png'))]
            for file_path in file_list:
                try:
                    shutil.move(file_path, my_pic)
                    print(file_path,my_pic)
                except Exception as e:
                    pass
                    # # 如果目标文件夹中已存在同名文件，则覆盖之
                    # if os.path.exists(my_pic):
                    #     os.replace(file_path, my_pic)
        for i in range(1, len(down_dirs)):
            if '1_All_Pictures' not in down_dirs[i]:
                os.rmdir(down_dirs[i])

    # 从总的图片文件夹中获取所有的图片的名称并放入一个列表，然后返回这个列表
    def extract_file_names(self):
        file_names = []
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                name = os.path.splitext(file_name)[0]
                file_names.append(name)
        return file_names

    def save_file_names_to_database(self, file_names):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # 检查表是否已经存在
            cursor.execute("PRAGMA table_info(images)")
            table_info = cursor.fetchall()
            if len(table_info) == 0:
                # 表不存在，创建表
                cursor.execute("CREATE TABLE images ( name TEXT UNIQUE)")
            # 检查存在的数据
            existing_names = set(cursor.execute("SELECT name FROM images").fetchall())
            filtered_file_names = [name for name in file_names if name not in str(existing_names)]
            # 插入数据
            cursor.executemany("INSERT INTO images VALUES (?)", [(name,) for name in filtered_file_names])
        except Exception as e:
            print(f'{e}')
        conn.commit()
        conn.close()

    def compare_urls_with_file_names(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM images")
        saved_file_names = [row[0] for row in cursor.fetchall()]
        conn.close()
        arr = get_dir_path()
        all_urls = return_all_url(arr)
        filtered_urls = []
        for url in all_urls:
            url = url.strip()
            url_name = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
            # print(url_name)
            if url_name not in saved_file_names:
                filtered_urls.append(url)
        print(f'搜集到的url数量为：{len(all_urls)}')
        # print(all_urls)
        print(f'过滤后的url数量为：{len(filtered_urls)}')
        target_file = '../merged.txt'
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(filtered_urls))
        print("↓↓↓↓↓↓↓↓↓---过滤后的全部图片URL的文件路径---↓↓↓↓↓↓↓↓↓\n{}".format(
            os.path.abspath(target_file)))

    def before_download_checkurl(self):
        fn = self.extract_file_names()
        self.save_file_names_to_database(fn)
        self.compare_urls_with_file_names()


if __name__ == '__main__':
    # 将子文件夹中的图片移动到总文件夹中去同时删除空文件夹
    CompareImageUrl.move_pic_to_all_pictures()
    cin = CompareImageUrl()
    cin.before_download_checkurl()