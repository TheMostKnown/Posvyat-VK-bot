import json
from typing import Optional, List

import vk_api
from sqlalchemy.orm import Session

from app.config import settings
from app.create_db import Sendings, Guests, Groups
from app.vk_events.send_message import send_message
from app.vk_tools.utils.upload import upload_photo


# args = [Sendings.mail_name]
def messages(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        args: Optional[List[str]] = None
) -> int:
    """ The function of launching mailing in VK.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param args: arguments of the command entered

    :return: error number or 0
    """

    if not args:
        return 1

    text = session.query(Sendings).filter_by(mail_name='paying').first()
    if not text:
        return 2
    if not text.text:
        return 10

    text_groups = json.loads(text.groups)
    text_pics = json.loads(text.pics)
    text_video = json.loads(text.video)
    text_reposts = json.loads(text.reposts)
    # text_docs = json.loads(text.docs)

    for user in session.query(Guests).all():
        user_groups = json.loads(user.groups)
        user_texts = json.loads(user.texts)
        intersection = []

        for elem in user_groups:
            if elem in text_groups:
                intersection.append(elem)

        if intersection == text_groups and text.id not in user_texts:
            send_message(
                vk=vk,
                chat_id=user.chat_id,
                text=text.text,
                attachments=[
                    *text_pics,
                    *text_video,
                    *text_reposts
                ]
            )
            user_texts.append(text.id)
            user.texts = json.dumps(user_texts)

    session.commit()
    return 0


# args = [Guests.vk_link], text
def messages_by_domain(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        args: str = None
) -> int:
    """ The function of launching mailing in VK by user domains.

        :param vk: session for connecting to VK API
        :param session: session to connect to the database
        :param args: arguments of the command entered

        :return: error number or 0
    """

    if not args:
        return 1

    domains = json.dumps(f'[{args[0]}]')
    text = args[1]

    for domain in domains:
        for user in session.query(Guests).all():

            if str(domain) == user.vk_link:
                send_message(
                    vk=vk,
                    chat_id=user.chat_id,
                    text=text,
                    attachments=[]
                )
                break

    session.commit()
    return 0
