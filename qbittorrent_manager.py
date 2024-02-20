# -*- coding: utf-8 -*-
import sys
import json
import requests
import logging
from datetime import datetime
import os

# Constants
ENDPOINTS = {
    'LOGIN': '/api/v2/auth/login',
    'REANNOUNCE': '/api/v2/torrents/reannounce',
    'SET_UPLOAD_LIMIT': '/api/v2/torrents/setUploadLimit',
    'SET_DOWNLOAD_LIMIT': '/api/v2/torrents/setDownloadLimit',
}

LOG_FILE_PATH = 'qbittorrent_management_log.txt'

def setup_logger():
    """设置日志记录器"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

def api_request(session, endpoint, data=None, cookies=None, qb_url=None):
    """发送API请求"""
    url = qb_url + ENDPOINTS[endpoint]
    if endpoint == 'LOGIN':
        headers = {'Referer': qb_url}
    else:
        headers = {'Cookie': 'SID=' + cookies}
    response = session.post(url, data=data, headers=headers)
    return response

def login(session, qbittorrent_username, qbittorrent_password, qb_url):
    """登录到qBittorrent客户端"""
    login_url = qb_url + "/api/v2/auth/login"
    login_data = {'username': qbittorrent_username, 'password': qbittorrent_password}
    headers = {'Referer': qb_url}
    
    try:
        response = requests.post(login_url, data=login_data, headers=headers)
        if response.status_code == 200:
            sid_cookie = response.cookies.get('SID')
            return sid_cookie
        else:
            logging.error("Failed to login. Status code: %s", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred during login: %s", e)
        return None

def reannounce_torrents(session, sid_cookie, qb_url):
    """重新汇报种子"""
    reannounce_url = qb_url + "/api/v2/torrents/reannounce"
    headers = {'Referer': qb_url, 'Cookie': 'SID=' + sid_cookie}
    data = {'hashes': 'all'}

    response = api_request(session, 'REANNOUNCE', data=data, cookies=sid_cookie, qb_url=qb_url)
    if response.status_code == 200:
        logging.info("Reannounce successful.")
        return True
    else:
        logging.error("Reannounce failed. Status code: %s, %s", response.status_code, response.text)
        return False

def set_upload_limit(session, sid_cookie, qb_url, upload_limit):
    """设置上传限速"""
    upload_limit_url = qb_url + "/api/v2/torrents/setUploadLimit"
    headers = {'Referer': qb_url, 'Cookie': 'SID=' + sid_cookie}
    data = {'hashes': '|'.join(sys.argv[1:]), 'limit': upload_limit}

    response = api_request(session, 'SET_UPLOAD_LIMIT', data=data, cookies=sid_cookie, qb_url=qb_url)
    if response.status_code == 200:
        logging.info("Set upload limit successful.")
        return True
    else:
        logging.error("Set upload limit failed. Status code: %s, %s", response.status_code, response.text)
        return False

def set_download_limit(session, sid_cookie, qb_url, download_limit):
    """设置下载限速"""
    download_limit_url = qb_url + "/api/v2/torrents/setDownloadLimit"
    headers = {'Referer': qb_url, 'Cookie': 'SID=' + sid_cookie}
    data = {'hashes': '|'.join(sys.argv[1:]), 'limit': download_limit}

    response = api_request(session, 'SET_DOWNLOAD_LIMIT', data=data, cookies=sid_cookie, qb_url=qb_url)
    if response.status_code == 200:
        logging.info("Set download limit successful.")
        return True
    else:
        logging.error("Set download limit failed. Status code: %s, %s", response.status_code, response.text)
        return False

def main():
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建配置文件的绝对路径
    config_file = os.path.join(script_dir, "config.json")

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found.")
        return
    
    qbittorrent_username = config.get('qbittorrent_username')
    qbittorrent_password = config.get('qbittorrent_password')
    qb_url = config.get('qb_url')
    upload_limit = config.get('upload_limit', 30000000)
    download_limit = config.get('download_limit', 10000000)

    session = requests.Session()
    logger = setup_logger()

    logger.info('Script started at %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Script has started.")

    # 登录到qBittorrent
    sid_cookie = login(session, qbittorrent_username, qbittorrent_password, qb_url)
    if not sid_cookie:
        print("Login failed.")
        return

    # 重新汇报种子
    if not reannounce_torrents(session, sid_cookie, qb_url):
        print("Reannounce failed.")
        return

    # 设置上传限速
    if not set_upload_limit(session, sid_cookie, qb_url, upload_limit):
        print("Set upload limit failed.")
        return

    # 设置下载限速
    if not set_download_limit(session, sid_cookie, qb_url, download_limit):
        print("Set download limit failed.")
        return

    logger.info('Script ended at %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Script has completed.")

if __name__ == "__main__":
    main()
