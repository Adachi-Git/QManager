import sys
import json
import requests
import logging
from datetime import datetime

# Constants
ENDPOINTS = {
    'LOGIN': '/api/v2/auth/login',
    'REANNOUNCE': '/api/v2/torrents/reannounce',
    'SET_UPLOAD_LIMIT': '/api/v2/torrents/setUploadLimit',
    'SET_DOWNLOAD_LIMIT': '/api/v2/torrents/setDownloadLimit',
}

LOG_FILE_PATH = 'qbittorrent_management_log.txt'

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

def api_request(session, endpoint, data=None, cookies=None, qb_url=None):
    url = qb_url + ENDPOINTS[endpoint]
    headers = {'Referer': qb_url} if endpoint == 'LOGIN' else {'Cookie': f'SID={cookies}'}
    response = session.post(url, data=data, headers=headers)
    return response

def main(config_file):
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

    try:
        # 登录
        login_response = api_request(session, 'LOGIN', {'username': qbittorrent_username, 'password': qbittorrent_password}, qb_url=qb_url)
        if login_response.status_code == 200:
            sid_cookie = login_response.cookies.get('SID')
            logger.info("Login successful. SID cookie: %s", sid_cookie)
            print("Login successful.")

            # 执行 reannounce
            reannounce_response = api_request(session, 'REANNOUNCE', {'hashes': 'all'}, sid_cookie, qb_url=qb_url)
            if reannounce_response.status_code == 200:
                logger.info("Reannounce successful.")
                print("Reannounce successful.")
            else:
                logger.error("Reannounce failed. Status code: %s, %s", reannounce_response.status_code, reannounce_response.text)
                print(f"Reannounce failed. Status code: {reannounce_response.status_code}, {reannounce_response.text}")

            # 设置上传限制
            upload_limit_response = api_request(session, 'SET_UPLOAD_LIMIT', {'hashes': '|'.join(sys.argv[1:]), 'limit': upload_limit}, sid_cookie, qb_url=qb_url)
            if upload_limit_response.status_code == 200:
                logger.info("Set upload limit successful.")
                print("Set upload limit successful.")
            else:
                logger.error("Set upload limit failed. Status code: %s, %s", upload_limit_response.status_code, upload_limit_response.text)
                print(f"Set upload limit failed. Status code: {upload_limit_response.status_code}, {upload_limit_response.text}")

            # 设置下载限制
            download_limit_response = api_request(session, 'SET_DOWNLOAD_LIMIT', {'hashes': '|'.join(sys.argv[1:]), 'limit': download_limit}, sid_cookie, qb_url=qb_url)
            if download_limit_response.status_code == 200:
                logger.info("Set download limit successful.")
                print("Set download limit successful.")
            else:
                logger.error("Set download limit failed. Status code: %s, %s", download_limit_response.status_code, download_limit_response.text)
                print(f"Set download limit failed. Status code: {download_limit_response.status_code}, {download_limit_response.text}")

        else:
            logger.error("Login failed. Status code: %s, %s", login_response.status_code, login_response.text)
            print(f"Login failed. Status code: {login_response.status_code}, {login_response.text}")

    except Exception as e:
        logger.exception("An error occurred: %s", str(e))
        print(f"An error occurred: {str(e)}")

    finally:
        logger.info('Script ended at %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("Script has completed.")

if __name__ == "__main__":
    main("config.json")
