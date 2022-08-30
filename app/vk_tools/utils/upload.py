import json
import requests
import logging

import vk_api

from app.config import settings
from app.vk_tools.google.google_drive.google_drive_handler import download_data

# Подключение логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def upload_photo(
        vk: vk_api.vk_api.VkApiMethod,
        photo_id: str,
        image_file_name: str
) -> str:
    download_data(
        file_id=photo_id,
        creds_file_name=settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH,
        image_file_name=image_file_name
    )

    url_response = vk.photos.getMessagesUploadServer(
        access_token=settings.VK_TOKEN,
        peer_id=settings.TECH_SUPPORT_VK_ID
    )

    if isinstance(url_response, dict) and 'upload_url' in url_response.keys():
        upload_url = url_response['upload_url']

        with open(image_file_name, 'rb') as file:

            upload = requests.post(
                url=upload_url,
                files={'photo': file}
            )

        upload_response = upload.json()

        logger.info(upload_response)

        if isinstance(upload_response, dict) and 'photo' in upload_response.keys():
            save_response = vk.photos.saveMessagesPhoto(
                photo=upload_response['photo'],
                server=upload_response['server'],
                hash=upload_response['hash']
            )[0]

            logger.info(save_response)

            if isinstance(save_response, dict) and \
                    'id' in save_response.keys() and \
                    'owner_id' in save_response.keys():
                return f'photo{save_response["owner_id"]}_{save_response["id"]}'

    return ''
