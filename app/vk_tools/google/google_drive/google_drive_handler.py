import io
import logging
from PIL import Image

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from app.vk_tools.google.get_creds import get_creds

# Подключение логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def download_raw_data(
        file_id: str,
        creds_file_name: str,
        token_file_name: str,
) -> bytes:

    creds = get_creds(creds_file_name, token_file_name)
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)

    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    is_done = False

    while not is_done:
        status, is_done = downloader.next_chunk()

    return file.getvalue()


def download_picture(
        file_id: str,
        file_path: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:

    image_bytes = download_raw_data(
        file_id,
        creds_file_name,
        token_file_name
    )

    image = Image.open(io.BytesIO(image_bytes))
    image.save(file_path)


def download_pdf_doc(
        file_id: str,
        file_path: str,
        creds_file_name: str,
        token_file_name: str,
) -> None:

    file_bytes = download_raw_data(
        file_id,
        creds_file_name,
        token_file_name
    )

    with open(file_path, 'wb') as doc:
        doc.write(file_bytes)
    doc.close()

