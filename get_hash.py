# -*- coding: utf-8 -*-
import json
import requests
import os

def login_qbittorrent(qbittorrent_username, qbittorrent_password, qb_url):
    # 构建登录请求的URL和数据
    login_url = qb_url + "/api/v2/auth/login"
    login_data = {'username': qbittorrent_username, 'password': qbittorrent_password}
    headers = {'Referer': qb_url}
    
    try:
        # 发送登录请求并获取响应
        response = requests.post(login_url, data=login_data, headers=headers)
        if response.status_code == 200:
            # 如果登录成功，返回会话ID
            return response.cookies['SID']
        else:
            # 如果登录失败，打印错误信息并返回None
            print("Failed to login. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # 发生请求异常时打印错误信息并返回None
        print("An error occurred:", e)
        return None

def get_torrent_list(session_id, qb_url, config, hashes=None):
    # 构建获取种子列表请求的URL和参数
    torrent_list_url = qb_url + "/api/v2/torrents/info"
    state_filter_var = config.get('state')  # 重命名为state_filter_var以避免与内置函数filter重名
    params = {
        'filter': state_filter_var,
        'category': config.get('category'),
        'tag': config.get('tag'),
        'sort': config.get('sort'),
        'reverse': config.get('reverse', False),
        'limit': config.get('limit'),
        'offset': config.get('offset'),
        'hashes': hashes
    }
    headers = {'Referer': qb_url}
    cookies = {'SID': session_id}

    try:
        # 发送获取种子列表的请求并获取响应
        response = requests.get(torrent_list_url, params=params, headers=headers, cookies=cookies)
        if response.status_code == 200:
            # 如果请求成功，返回JSON格式的种子列表信息
            return response.json()
        else:
            # 如果请求失败，打印错误信息并返回None
            print("Failed to get torrent list with state '{}'. Status code: {}".format(state_filter_var, response.status_code))
            return None
    except requests.exceptions.RequestException as e:
        # 发生请求异常时打印错误信息并返回None
        print("An error occurred:", e)
        print("Response content:", response.content)
        return None
    
def fetch_and_print_downloading_torrents():
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建配置文件的绝对路径
    config_file = os.path.join(script_dir, "config.json")

    try:
        # 读取配置文件
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        # 如果配置文件不存在，打印错误信息并返回
        print("Config file not found:", config_file)
        return
    
    # 从配置中获取qbittorrent用户名、密码和URL
    username = config.get('qbittorrent_username')
    password = config.get('qbittorrent_password')
    qb_url = config.get('qb_url')
    
    # 登录qbittorrent并获取会话ID
    session_id = login_qbittorrent(username, password, qb_url)
    if not session_id:
        # 如果登录失败，打印错误信息并返回
        print("Login failed.")
        return
    
    # 获取正在下载的种子列表
    downloading_torrent_list = get_torrent_list(session_id, qb_url, config=config)
    
    # 检查是否成功获取了种子列表
    if downloading_torrent_list is None:
        print("Failed to get downloading torrent list.")
        return
    
    # 检查是否有正在下载的种子
    if not downloading_torrent_list:
        print("No downloading torrents found.")
        return
    
    # 打印正在下载的种子信息
    print(json.dumps(downloading_torrent_list))

# 调用函数并传入配置文件的路径
fetch_and_print_downloading_torrents()
