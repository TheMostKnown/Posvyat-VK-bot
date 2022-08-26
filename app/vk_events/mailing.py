import json

import vk_api
from typing import List, Optional
from sqlalchemy.orm import Session

from app.create_db import Sendings, Guests, Groups
from app.vk_events.send_message import send_message


# args = [Sendings.mail_name]
def messages(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        args: str = None
) -> int:
    """ The function of launching mailing in VK.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param args: arguments of the command entered

    :return: error number or 0
    """

    if not args:
        return 1

    text = session.query(Sendings).filter_by(mail_name=args).first()
    if not text:
        return 2
    if not text.text:
        return 10

    text_groups = json.loads(text.groups)
    for user in session.query(Guests).all():
        user_groups = json.loads(user.groups)
        intersection = []

        for elem in user_groups:
            if elem in text_groups:
                intersection.append(elem)

        print(f"{intersection}")

        if intersection == text_groups:
            send_message(
                vk=vk,
                chat_id=user.chat_id,
                text=text.text,
                attachments=[]
            )

    session.commit()
    return 0
