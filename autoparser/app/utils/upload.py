import logging

import vk_api

from config import settings
from google.google_drive.google_drive_handler import download_picture, download_pdf_doc

# Подключение логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def upload_photo(
        vk: vk_api.upload.VkApiMethod,
        photo_id: str,
        image_file_path: str
) -> str:
    download_picture(
        file_id=photo_id,
        file_path=image_file_path,
        creds_file_name=settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH,
    )

    vk_upload = vk_api.VkUpload(vk)
    upload_response = vk_upload.photo_messages(
        photos=image_file_path,
        peer_id=settings.TECH_SUPPORT_VK_ID
    )[0]

    if 'owner_id' in upload_response.keys() and 'id' in upload_response.keys():
        owner_id = upload_response['owner_id']
        id = upload_response['id']

        return f'photo{owner_id}_{id}'

    return ''


def upload_pdf_doc(
        vk: vk_api.vk_api.VkApiMethod,
        doc_id: str,
        doc_file_path: str
) -> str:
    download_pdf_doc(
        file_id=doc_id,
        file_path=doc_file_path,
        creds_file_name=settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH,
    )

    vk_upload = vk_api.VkUpload(vk)

    upload_response = vk_upload.document_message(
        doc=doc_file_path,
        peer_id=settings.TECH_SUPPORT_VK_ID
    )

    if 'doc' in upload_response.keys():
        owner_id = upload_response['doc']['owner_id']
        id = upload_response['doc']['id']

        return f'doc{owner_id}_{id}'

    return ''
