import vk_api
from typing import List, Optional
import json
from sqlalchemy.orm import Session

from app.create_db import Sendings, Guests, Groups
from app.vk_events.send_message import send_message


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
    if not args or not args[0]:
        return 1

    params = {'mail_name': args[0]}

    text = session.query(Sendings).filter_by(**params).first()
    if not text:
        return 2
    if not text.text:
        return 10

    for user in session.query(Guests).filter_by(**params):
        groups = json.loads(user.groups)

        if list(set(text.groups) & set(groups)) == text.groups:
            send_message(
                vk=vk,
                chat_id=user.id,
                text=text.text,
                attachments=[] if not text.attachments else json.loads(text.attachments)
            )

    session.commit()
    return 0
