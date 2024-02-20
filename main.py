import json
import subprocess
import sys
import os

def main():
    # 获取当前脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建 get_hash.py 和 qbittorrent_manager.py 的绝对路径
    get_hash_path = os.path.join(script_dir, "get_hash.py")
    qbittorrent_manager_path = os.path.join(script_dir, "qbittorrent_manager.py")

    process1 = subprocess.Popen([sys.executable, get_hash_path], stdout=subprocess.PIPE)
    output1, _ = process1.communicate()

    # 解析输出
    try:
        torrent_info_list = json.loads(output1)
        print("Torrent info list from get_hash:", torrent_info_list)  # 调试语句
    except ValueError as e:
        print("Error: {}".format(e))  # 使用.format()方法进行变量插值
        print("Failed to parse output from get_hash.")
        torrent_info_list = []

    # 检查哈希列表的类型
    hash_list = [torrent_info.get('hash') for torrent_info in torrent_info_list if isinstance(torrent_info.get('hash'), str)]

    if not hash_list:
        print("Error: No valid hashes obtained from get_hash.")
        hash_list = []

    # 将哈希列表转换为字符串形式
    hash_list_str = "|".join(hash_list)

    # 调用并传递哈希列表作为参数给 qbittorrent_manager.py 脚本
    subprocess.Popen([sys.executable, qbittorrent_manager_path, hash_list_str]).wait()

if __name__ == "__main__":
    main()
