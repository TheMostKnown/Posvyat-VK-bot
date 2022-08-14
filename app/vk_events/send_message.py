from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard
import vk_api
import time
from typing import Optional, List

from app.config import settings
from app.create_db import get_session, engine, Guests, Orgs


def send_message(
        vk: vk_api.vk_api.VkApiMethod,
        chat_id: int,
        text: str,
        keyboard: Optional[vk_api.keyboard.VkKeyboard] = None,
        attachments: Optional[List[str]] = None) -> int:
    """Function sends message to certain user.

    :param vk: started VK session with authorization in group
    :type vk: VkApiMethod

    :param chat_id: user id
    :type chat_id: int

    :param text: text for messaging
    :type text: str

    :param keyboard: unnecessary keyboard, that attaches to the message
    :type keyboard: VkKeyboard

    :param attachments: unnecessary attachments to the message
    :type attachments: List[str]

    :return: nothing
    :rtype: None
    """

    message_id = 0

    # Попытка отправить сообщение
    try:
        message_id = vk.messages.send(
            user_id=chat_id,
            message=text,
            attachment=attachments,
            random_id=get_random_id(),
            keyboard=None if not keyboard else keyboard.get_keyboard()
        )

        # Задержка от спама
        time.sleep(settings.DELAY)

    # Оповещение о недошедшем сообщении
    except Exception as e:

        session = get_session(engine)
        user = session.query(Guests).filter_by(id=chat_id).first()
        organizer = session.query(Orgs).filter_by(id=chat_id).first()

        if organizer:
            user = organizer

        if user:
            domain = session.query(Guests).filter_by(id=chat_id).first().domain

            error_text = f'Пользователю vk.com/{domain} ({chat_id})' \
                         f'не отправилось сообщение "{text}"\n' \
                         f'По причине: "{e}"'
            vk.messages.send(
                user_id=settings.TECH_SUPPORT_VK_ID,
                message=error_text,
                random_id=get_random_id()
            )

    return message_id
