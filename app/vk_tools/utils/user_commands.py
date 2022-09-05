import re
import json
from typing import Optional, List
import logging

import vk_api
from sqlalchemy import desc
from sqlalchemy.orm import Session
from vk_api.bot_longpoll import VkBotEvent
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from app.config import settings
from app.vk_events.send_message import send_message
from app.vk_tools.keyboards import user_keyboard
from app.create_db import Info, Guests, TechSupport, Sendings, Missing

logger = logging.getLogger(__name__)

def main_menu(
        vk: vk_api.vk_api.VkApiMethod,
        chat_id: int,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function of main menu keyboard

    :param vk: session for connecting to VK API
    :param chat_id: user id for sending message
    :param event: event object in VK
    :return: error number or 0
    """ 
    send_message(
            vk=vk,
            chat_id=chat_id,
            text='Меню:',
            keyboard=user_keyboard.main_keyboard
            )
    return 0

def get_information(
        vk: vk_api.vk_api.VkApiMethod,
        vk_session: vk_api.vk_api.VkApi,
        chat_id: int,
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for sending answers to info buttons

    :param vk: session for connecting to VK API
    :param vk_session: VK session
    :param chat_id: user id for sending message
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 

    # available_info = dict() 
    # for i in session.query(Info).all():
    #     available_info[i.question] = i.answer

    # questions = list(available_info.keys())
    questions = [information.question for information in session.query(Info).all()]
    
    send_message(
            vk=vk,
            chat_id=chat_id,
            text='Доступная информация:',
            keyboard=user_keyboard.info_keyboard(questions)

        )
    return 0


def send_answer(
        vk: vk_api.vk_api.VkApiMethod,
        chat_id: int,
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for sending answer to buttons

    :param vk: session for connecting to VK API
    :param chat_id: user id for sending message
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 
    reply = session.query(Info.answer).filter(Info.question==event.message['text']).first()[0]
    send_message(
            vk=vk,
            chat_id=chat_id,
            text=reply
        )
    return 0

    

def what_missed(
        vk: vk_api.vk_api.VkApiMethod,
        chat_id: int,
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for giving information about what
    user has missed

    :param vk: session for connecting to VK API
    :param chat_id: user id for sending message
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 

    missed = [missed.button for missed in session.query(Missing).all()]
    
    send_message(
            vk=vk,
            chat_id=chat_id,
            text='Доступная информация:',
            keyboard=user_keyboard.info_keyboard(missed)

        )
    return 0
    # user = session.query(Guests).get(chat_id)

    # user_groups = json.loads(user.groups)
    # user_texts = json.loads(user.texts)

    # missing = []

    # for elem in session.query(Sendings):

    #     if elem.groups[0] != '!':
    #         sending_groups = json.loads(f'[{elem.groups}]')
    #         #проверка входят ли уровни рассылки в уровни пользователя
    #         if set(sending_groups).issubset(user_groups):
    #             if not elem.id in user_texts:
    #                 missing.append(elem.id)
    #     else:
    #         not_sending_groups = json.loads(f'[{elem.groups[1:]}]')
    #         #проверка чтобы не входило в уровни пользователя
    #         intersection = []
    #         for group in user_groups:
    #             if group in not_sending_groups:
    #                 intersection.append(group)
    #         if len(intersection) == 0 and not elem.id in user_texts:
    #             missing.append(elem.id)


    # if len(missing) == 0:
    #     send_message(vk, chat_id, "У вас нет пропущенных рассылок.")
    #     return 0

    # send_message(vk, chat_id, "Пропущенные рассылки: ")
    # for item in missing:
    #     sending = session.query(Sendings).filter(Sendings.id==item).first()

    #     sending_text = sending.text
    #     sending_pics = json.loads(sending.pics)
    #     sending_video = json.loads(sending.video)
    #     sending_reposts = json.loads(sending.reposts)
    #     sending_docs = json.loads(sending.docs)

    #     send_message(
    #             vk=vk,
    #             chat_id=chat_id,
    #             text=sending_text,
    #             attachments=[
    #                 *sending_pics,
    #                 *sending_video,
    #                 *sending_reposts,
    #                 *sending_docs
    #             ]
    #         )
        
    #     user_texts.append(item)
    # user.texts = json.dumps(user_texts)
    # session.commit()
        
    # return 0

def send_answer_missed(
        vk: vk_api.vk_api.VkApiMethod,
        chat_id: int,
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for sending answer to missed buttons

    :param vk: session for connecting to VK API
    :param chat_id: user id for sending message
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 
    reply = session.query(Missing.answer).filter(Missing.button==event.message['text']).first()[0]
    send_message(
            vk=vk,
            chat_id=chat_id,
            text=reply
        )
    return 0

def tech_support(
        vk: vk_api.vk_api.VkApiMethod,
        chat_id: int,
) -> int:
    """ The function for tech support button

    :param vk: session for connecting to VK API
    :param chat_id: user id for sending message

    :return: error number or 0
    """ 
    main_message = 'Вы можете направить обращение в техническую поддержку.\n'
    main_message += 'Для этого изложите свою проблему в одном сообщении в следующем текстовом формате:\n'
    main_message += 'TECH_SUPPORT: текст вашего обращения'
    send_message(vk, chat_id, main_message)
    return 0

def send_tech_support(
    vk: vk_api.vk_api.VkApiMethod,
    chat_id: int,
    session: Session,
    event: Optional[VkBotEvent] = None,
) -> int:

    tech_text = event.message['text'].lower()

    correct = re.search(r"tech_support\s*\:\s*(.{1,200})\s*", tech_text)
    if not correct:
        send_message(vk, chat_id, "Не удалось отправить сообщение в техническую поддержку.")
        return 0
    message = correct[1]
    logger.info(f'Tech support message: {message}')
    user_info = vk.users.get(user_id=chat_id, fields='domain')[0]

    session.add(
        TechSupport(
            vk_link=user_info['domain'],
            per_question=message,
            status='open'
        )
    )
    #сообщение пользователю
    send_message(vk, chat_id, "Сообщение успешно отправлено в техподдержку. В ближайшее время Вам помогут!")
    #сообщение техподдержке
    send_message(
        vk=vk,
        chat_id=settings.TECH_SUPPORT_VK_ID,
        text=f'Пользователь vk.com/{user_info["domain"]} ({chat_id}) написал в техподдержку'
    )
    session.commit()
    return 0


