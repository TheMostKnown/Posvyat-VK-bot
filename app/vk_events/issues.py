from sqlalchemy.orm import Session
import vk_api

from app.create_db import TechSupport
from app.vk_events.send_message import send_message
from app.config import settings


def open_issues(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int
) -> int:
    """ The function of sending open issues in VK.

        :param vk: session for connecting to VK API
        :param session: session to connect to the database

        :return: error number or 0
        """

    issues = session.query(TechSupport).filter_by(status='open').all()

    text = ''
    if issues:
        for issue in issues:
            text += f'У пользователя vk.com/{issue.vk_link} произошла проблема:\n' \
                   f'{issue.per_question}\n'
    else:
        text = 'Сейчас нет открытых баг-репортов. Можешь почиллить!'
    #сообщение техподдержке
    send_message(
        vk=vk,
        chat_id=settings.TECH_SUPPORT_VK_ID,
        text=text
    )
    #сообщение админу, который вызвал
    send_message(
        vk=vk,
        chat_id=chat_id,
        text=text
    )

    return 0
