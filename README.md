# qbittorrent_management_script

This Python script is designed to perform various management tasks on qBittorrent using its Web API. It can log in, reannounce torrents, set upload and download limits, and log relevant information.

## Requirements

- Python 3.x
- Requests library (install using `pip install requests`)

## Configuration

1. Replace the placeholders in the script with your qBittorrent Web UI address, port, username, and password.
2. Ensure that Python is installed on your system.
3. Install the required `requests` library by running `pip install requests`.

## Usage

Run the script using the following command:

```bash
python qbittorrent_management_script.py
```


## Features

- **Login**: Logs in to the qBittorrent Web UI.
- **Reannounce Torrents**: Performs reannounce for all torrents.
- **Set Upload Limit**: Sets the upload limit for all torrents.
- **Set Download Limit**: Sets the download limit for all torrents.

## Logging

The script logs its activities to a file named `qbittorrent_management_log.txt`. The log file includes information about script start, login status, reannounce status, and limit-setting status.

## Troubleshooting

If there are issues, check the log file for detailed information about any errors or failures.

**Note:** Ensure that your qBittorrent Web UI is accessible, and the API endpoints match the configured values in the script.

Feel free to modify the script according to your specific requirements.
