import vk_api
from typing import List, Optional
import json
from sqlalchemy.orm import Session

from app.create_db import Sendings, Guests, Orgs, Groups
from send_message import send_message


# args = [Sendings.mail_name, None | Groups.group_num | Groups.group_info]
def messages(vk: vk_api.vk_api.VkApiMethod,
             session: Session,
             args: Optional[List[str]] = None) -> int:
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
    if not text.text and not text.media:
        return 10

    params = {}
    if len(args) > 1 and args[1].isdigit():
        params['group_number'] = int(args[1])
    elif len(args) > 1 and args[1]:
        group = session.query(Groups).filter_by(name=args[1]).first()
        if not group:
            return 4
        params['group_number'] = group.group_num
    elif str(text.group_num).isdigit():
        params['group_number'] = text.group_num

    for user in session.query(Guests).filter_by(**params):
        groups = json.loads(user.groups)

        if params['group_number'] in groups:
            send_message(
                vk=vk,
                chat_id=user.id,
                text=text.text,
                attachments=[] if not text.attachments else json.loads(text.attachments)
            )

    for org in session.query(Orgs).filter_by(**params):
        groups = json.loads(org.groups)

        if params['group_number'] in groups:
            send_message(
                vk=vk,
                chat_id=org.id,
                text=text.text,
                attachments=[] if not text.attachments else json.loads(text.attachments)
            )

    session.commit()
    return 0
