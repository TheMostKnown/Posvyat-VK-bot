import requests
import logging

import vk_api

from app.config import settings
from app.vk_tools.google.google_drive.google_drive_handler import download_picture, download_pdf_doc

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

    url_response = vk.photos.getMessagesUploadServer(
        access_token=settings.VK_TOKEN,
        peer_id=settings.TECH_SUPPORT_VK_ID
    )

    if isinstance(url_response, dict) and 'upload_url' in url_response.keys():
        upload_url = url_response['upload_url']

        with open(image_file_path, 'rb') as file:

            upload = requests.post(
                url=upload_url,
                files={'photo': file}
            )

        upload_response = upload.json()

        # logger.info(upload_response)

        if isinstance(upload_response, dict) and 'photo' in upload_response.keys():
            save_response = vk.photos.saveMessagesPhoto(
                photo=upload_response['photo'],
                server=upload_response['server'],
                hash=upload_response['hash']
            )[0]

            # logger.info(save_response)

            if isinstance(save_response, dict) and \
                    'id' in save_response.keys() and \
                    'owner_id' in save_response.keys():
                return f'photo{save_response["owner_id"]}_{save_response["id"]}'

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