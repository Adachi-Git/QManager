import os
import shutil

directory_path = 'F:\Downlord'

# 确保目录存在
if os.path.exists(directory_path):
    # 删除目录下后缀为 .torrent 的所有文件
    for filename in os.listdir(directory_path):
        if filename.endswith(".torrent"):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass
else:
    print(f"目录 '{directory_path}' 不存在")
