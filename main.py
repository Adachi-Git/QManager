import json
import subprocess

def main():
    process1 = subprocess.Popen(["python", "get_hash.py"], stdout=subprocess.PIPE)
    output1, _ = process1.communicate()

    # 解析输出
    try:
        torrent_info_list = json.loads(output1)
        print("Torrent info list from get_hash:", torrent_info_list)  # 调试语句
        if not torrent_info_list:
            raise ValueError("No torrent info obtained from get_hash.")
    except ValueError as e:
        print(f"Error: {e}")
        print("Failed to parse output from get_hash.")
        return

    # 检查哈希列表的类型
    hash_list = [torrent_info.get('hash') for torrent_info in torrent_info_list if isinstance(torrent_info.get('hash'), str)]
    if not hash_list:
        print("Error: No valid hashes obtained from get_hash.")
        return

    # 将哈希列表转换为字符串形式
    hash_list_str = "|".join(hash_list)

    # 调用第二个脚本并传递哈希列表作为参数
    subprocess.run(["python", "qbittorrent_management_script.py", hash_list_str])

if __name__ == "__main__":
    main()
