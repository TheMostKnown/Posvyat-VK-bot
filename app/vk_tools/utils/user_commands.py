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
from app.create_db import Info, Guests, TechSupport, Sendings

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

    available_info = dict() 
    for i in session.query(Info).all():
        available_info[i.question] = i.answer

    questions = list(available_info.keys())

    logger.info(f'Inside Info, availiable info: {available_info}')
    
    send_message(
            vk=vk,
            chat_id=chat_id,
            text='Доступная информация:',
            keyboard=user_keyboard.info_keyboard(questions)

        )

    for info_event in VkBotLongPoll(vk=vk_session, group_id=settings.VK_GROUP_ID, wait=25).listen():
        logger.info("inside Info listen")
        logger.info(f"Inside Info listen question: {info_event.message['text']}")
        if info_event.type == VkBotEventType.MESSAGE_NEW and info_event.from_user:

            info_text = info_event.message['text']
            info_chat_id = int(info_event.message['from_id'])
    

            if info_text in questions:
                respond = available_info[info_text]
                send_message(
                    vk=vk,
                    chat_id=info_chat_id,
                    text=respond,
                    keyboard=user_keyboard.info_keyboard(questions)
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
    user = session.query(Guests).get(chat_id)

    user_groups = json.loads(user.groups)
    user_texts = json.loads(user.texts)

    missing = []

    for elem in session.query(Sendings):
        sending_groups = json.loads(elem.groups)
        #проверка входят ли уровни рассылки в уровни пользователя
        if set(sending_groups).issubset(user_groups):
            if not elem.id in user_texts:
                missing.append(elem.id)
    if len(missing) == 0:
        send_message(vk, chat_id, "У вас нет пропущенных рассылок.")
        return 0

    send_message(vk, chat_id, "Пропущенные рассылки: ")
    for item in missing:
        sending = session.query(Sendings.text).filter(Sendings.id==item).first()[0]
        send_message(vk, chat_id, sending)
        
        user_texts.append(item)
    user.texts = json.dumps(user_texts)
    session.commit()
        
    return 0

def tech_support(
        vk: vk_api.vk_api.VkApiMethod,
        vk_session: vk_api.vk_api.VkApi,
        chat_id: int,
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for tech support button

    :param vk: session for connecting to VK API
    :param vk_session: VK session
    :param chat_id: user id for sending message
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 
    main_message = 'Вы можете направить обращение в техническую поддержку.\n'
    main_message += 'Пожалуйста, изложите свою проблему в одном сообщении.\n'
    main_message += 'Если вы передумали связываться с техподдержкой, отправьте "отмена"'
    send_message(vk, chat_id, main_message)

    for tech_event in VkBotLongPoll(vk=vk_session, group_id=settings.VK_GROUP_ID, wait=25).listen():

        logger.info('Inside Tech Support listen for message')

        if tech_event.type == VkBotEventType.MESSAGE_NEW and tech_event.from_user:
            
            tech_text = tech_event.message["text"]
            logger.info(f'Tech support got message {tech_text}')
            tech_chat_id = int(tech_event.message['from_id'])

            if tech_text.lower() == 'отмена':
                return 0

            respond_text = f'В техподдержку будет отправлено следующее сообщение: "{tech_text}".\n'
            respond_text += 'Для подтверждения данного действия отправьте "да"\n'
            respond_text += 'Для отмены данного действия отправьте "отмена"'
            send_message(vk, tech_chat_id, respond_text)


            for confirm_event in VkBotLongPoll(vk=vk_session, group_id=settings.VK_GROUP_ID, wait=25).listen():
                if confirm_event.type == VkBotEventType.MESSAGE_NEW and tech_event.from_user:
                    logger.info('Inside Tech Support listen for "yes" or "cansel"')

                    confirm_text = confirm_event.message["text"].lower()
                    confirm_chat_id = int(confirm_event.message['from_id'])

                    if confirm_text == 'да':
                        user_info = vk.users.get(user_id=confirm_chat_id, fields='domain')[0]
                        session.add(
                            TechSupport(
                               vk_link=user_info['domain'],
                               per_question=tech_text,
                               status='open'
                            )
                        )
                        session.commit()
                        #сообщение пользователю
                        send_message(vk, confirm_chat_id, "Сообщение успешно отправлено в техподдержку.")
                        #сообщение техподдержке
                        send_message(
                            vk=vk,
                            chat_id=settings.TECH_SUPPORT_VK_ID,
                            text=f'Пользователь vk.com/{user_info["domain"]} ({confirm_chat_id}) написал в техподдержку'
                        )
                        return 0

                    elif confirm_text == 'отмена':
                        return 0

                    else:
                        send_message(vk, confirm_chat_id, f"Команда не распознана!\n{respond_text}")
