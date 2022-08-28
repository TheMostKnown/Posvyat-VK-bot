import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from app.vk_tools.google.get_creds import get_creds


def download_data(
        file_id: str,
        creds_file_name: str,
        token_file_name: str
) -> bytes:

    creds = get_creds(creds_file_name, token_file_name)
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)

    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    is_done = False

    while not is_done:
        status, done = downloader.next_chunk()

    return file.getvalue()
