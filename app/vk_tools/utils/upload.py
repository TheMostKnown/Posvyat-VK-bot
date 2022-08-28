import json
import requests

import vk_api

from app.config import settings
from app.vk_tools.google.google_drive.google_drive_handler import download_data


def upload_photo(
        vk: vk_api.vk_api.VkApiMethod,
        photo_id: str
) -> str:
    photo = download_data(
        file_id=photo_id,
        creds_file_name=settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        token_file_name=settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
    )

    url_request = vk.photos.getMessagesUploadServer(
        access_token=settings.VK_TOKEN,
        peer_id=settings.TECH_SUPPORT_VK_ID
    )
    url_response = json.loads(url_request)

    if 'upload_url' in url_response.keys():
        upload_url = url_response['upload_url']

        upload = requests.post(
            url=upload_url,
            json=json.dumps({'photo': photo})
        )

        upload_response = json.loads(upload.json())

        if 'photo' in upload_response.keys():
            message_response = json.loads(
                vk.photos.saveMessagesPhoto(
                    photo=upload_response['photo'],
                    server=upload_response['server'],
                    hash=upload_response['hash']
                )
            )

            if 'id' in message_response.keys():
                return message_response['id']

    return ''
