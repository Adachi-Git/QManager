# QManager 项目

## 简介

QManager 是一个用于管理 qBittorrent 客户端的工具。它提供了一组脚本，用于执行以下操作：

- 获取指定状态的种子信息并打印出来。
- 设置 qBittorrent 客户端中指定状态的种子的上传和下载速率限制。

## 功能

### get_hash.py

该脚本用于获取指定状态的种子的信息并打印出来。它与 qBittorrent 客户端进行通信，获取指定状态的种子的哈希值、状态等信息。

### qbittorrent_manager.py

该脚本用于设置 qBittorrent 客户端中指定状态的种子的上传和下载速率限制。它与 qBittorrent 客户端进行通信，通过 API 设置上传和下载速率限制。

### main.py

主脚本，用于调用上述两个脚本，并传递必要的参数。

## 使用方法

1. 首先，确保已安装 Python 3 和 qBittorrent 客户端。
2. 配置 `config.json` 文件，填写 qBittorrent 客户端的用户名、密码和 URL，以及其他相关配置。
3. 运行 `main.py` 脚本以执行所需的操作。

## 配置说明

- `qbittorrent_username`: qBittorrent 客户端的用户名。
- `qbittorrent_password`: qBittorrent 客户端的密码。
- `qb_url`: qBittorrent 客户端的 URL 地址。
- `state`: 指定状态的种子，例如 "downloading" 表示正在下载的种子。
- `tag`: 种子的标签，可选参数。
- `sort`: 排序方式，可选参数。
- `reverse`: 是否倒序排列，可选参数。
- `limit`: 返回结果的数量限制，可选参数。
- `offset`: 返回结果的偏移量，可选参数。
- `upload_limit`: 上传速率限制，默认为 10000000，单位为字节。
- `download_limit`: 下载速率限制，默认为 10000000，单位为字节。

## 注意事项

- 在使用之前，请确保已正确配置 `config.json` 文件。
- 请注意设置上传和下载速率限制时的参数值，以避免影响网络性能。

