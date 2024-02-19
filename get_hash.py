import json
import requests

def login_qbittorrent(qbittorrent_username, qbittorrent_password, qb_url):
    login_url = f"{qb_url}/api/v2/auth/login"
    login_data = {'username': qbittorrent_username, 'password': qbittorrent_password}
    headers = {'Referer': qb_url}
    
    try:
        response = requests.post(login_url, data=login_data, headers=headers)
        if response.status_code == 200:
            return response.cookies['SID']
        else:
            print("Failed to login. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None

def get_torrent_list(session_id, qb_url, config, hashes=None):
    torrent_list_url = f"{qb_url}/api/v2/torrents/info"
    params = {
        'filter': config.get('state'),
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
        response = requests.get(torrent_list_url, params=params, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get torrent list with state '{filter}'. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None

def fetch_and_print_downloading_torrents(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found.")
        return
    
    username = config.get('qbittorrent_username')
    password = config.get('qbittorrent_password')
    qb_url = config.get('qb_url')
    
    session_id = login_qbittorrent(username, password, qb_url)
    if not session_id:
        print("Login failed.")
        return
    
    downloading_torrent_list = get_torrent_list(session_id, qb_url, config=config)
    if downloading_torrent_list:
        print(json.dumps(downloading_torrent_list))  
    else:
        print("Failed to get downloading torrent list.")

# 调用函数并传入配置文件的路径
fetch_and_print_downloading_torrents("config.json")