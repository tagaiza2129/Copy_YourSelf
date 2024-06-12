from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.http import io, MediaIoBaseDownload
import os
import json
from logging import getLogger, config
from tqdm import tqdm
with open('設定ファイル/log_config.json', 'r') as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)
def Drive_Download(path,output):
    os.chdir(os.path.dirname(__file__))
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '設定ファイル/copy-yourself-a3cc232df672.json', SCOPES
    )
    http_auth = credentials.authorize(Http())
    drive_service = build('drive', 'v3', http=http_auth)
    condition_list = [
    f"('{'1YfnxfJeDiGHYv8YZUw_-bJ-zWFusqyla'}' in parents)"
    ]
    conditions = " and ".join(condition_list)

    results = drive_service.files().list(
        q = conditions,
        fields = "nextPageToken, files(id, name)",
        pageSize = 100, 
    ).execute()
    files = results.get('files', [])
    if files:
        os.chdir(os.path.join(os.path.dirname(__file__),output))
        file_names = [file['name'] for file in files]
        if path not in file_names:
            logger.info("対象のファイルが見つかりませんでした")
            exit()
        else:
            logger.info("ファイルIDを取得しています...")
            for file in files:
                if file['name'] == path:
                    file_id=file['id']
                    condition_list = [f"('{file_id}' in parents)"]
                    conditions = " and ".join(condition_list)
                    results = drive_service.files().list(
                    q = conditions,
                    fields = "nextPageToken, files(id, name,size)",
                    pageSize = 100, 
                    ).execute()
                    files_goal = results.get('files', [])
                    if files_goal:
                        for goal_file in files_goal:
                            file_size = int(goal_file['size'])
                            request = drive_service.files().get_media(fileId=goal_file['id'])
                            fh = io.FileIO(goal_file['name'], 'wb')
                            downloader = MediaIoBaseDownload(fh, request)
                            pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc=goal_file['name'])
                            done = False
                            while done is False:
                                status, done = downloader.next_chunk()
                                pbar.update(status.resumable_progress - pbar.n)
                            pbar.close()
                    else:
                        logger.info("ファイルが見つかりませんでした")
                        exit()
    else:
        logger.info("ファイルが見つかりませんでした")
        exit()