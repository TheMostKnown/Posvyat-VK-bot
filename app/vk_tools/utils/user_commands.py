import json
from typing import Optional, List

import vk_api
from sqlalchemy import desc
from sqlalchemy.orm import Session
from vk_api.bot_longpoll import VkBotEvent
from vk_api.longpoll import VkLongPoll, VkEventType

from app.vk_events.send_message import send_message
from app.vk_tools.keyboards import user_keyboard
from app.create_db import Info, Guests, TechSupport


def main_menu(
        vk: vk_api.vk_api.VkApiMethod,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function of main menu keyboard

    :param vk: session for connecting to VK API
    :param event: event object in VK

    :return: error number or 0
    """ 
    chat_id = event.raw[3]
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
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for sending answers to info buttons

    :param vk: session for connecting to VK API
    :param vk_session: VK session
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 
    chat_id = event.raw[3]

    available_info = dict() 
    for i in session.query(Info):
        available_info[i.question] = i.answer

    questions = list(available_info.keys())
    
    send_message(
            vk=vk,
            chat_id=chat_id,
            text='Доступная информация:',
            keyboard=user_keyboard.info_keyboard(questions)

        )

    for info_event in VkLongPoll(vk_session).listen():
        if info_event.type == VkEventType.MESSAGE_NEW and info_event.to_me and info_event.user_id==chat_id:

            info_text = info_event.text
            info_chat_id = info_event.raw[3]
    

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
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for giving information about what
    user has missed

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 
    chat_id = event.raw[3]

    guest_groups = json.loads(session.query(Guests.groups).filter(Guests.id == chat_id).first()[0])
    
    return 0

def tech_support(
        vk: vk_api.vk_api.VkApiMethod,
        vk_session: vk_api.vk_api.VkApi,
        session: Session,
        event: Optional[VkBotEvent] = None,
) -> int:
    """ The function for tech support button

    :param vk: session for connecting to VK API
    :param vk_session: VK session
    :param session: session to connect to the database
    :param event: event object in VK

    :return: error number or 0
    """ 
    chat_id =  event.raw[3]
    main_message = 'Вы можете направить обращение в техническую поддержку.\n'
    main_message += 'Пожалуйста, изложите свою проблему в одном сообщении.\n'
    main_message += 'Если вы передумали связываться с техподдержкой, отправьте "отмена"'
    send_message(vk, chat_id, main_message)

    for tech_event in VkLongPoll(vk_session).listen():
        if tech_event.type == VkEventType.MESSAGE_NEW and tech_event.to_me and tech_event.user_id == chat_id:

            tech_text = tech_event.text
            tech_chat_id = tech_event.raw[3]

            if tech_text.lower() == 'отмена':
                return 0

            respond_text = f'В техподдержку будет отправлено следующее сообщение: "{tech_text}".\n'
            respond_text += 'Для подтверждения данного действия отправьте "да"\n'
            respond_text += 'Для отмены данного действия отправьте "отмена"'
            send_message(vk, tech_chat_id, respond_text)


            for confirm_event in VkLongPoll(vk_session).listen():
                if confirm_event.type == VkEventType.MESSAGE_NEW and confirm_event.to_me and confirm_event.user_id==tech_chat_id:

                    confirm_text = confirm_event.text.lower()
                    confirm_chat_id = confirm_event.raw[3]

                    if confirm_text == 'да':
                        session.add(
                            TechSupport(
                               vk_link=f'id{confirm_chat_id}',
                               per_question=tech_text,
                               status='open'
                            )
                        )
                        session.commit()
                        send_message(vk, confirm_chat_id, "Сообщение успешно отправлено в техподдержку.")
                        return 0

                    elif confirm_text == 'отмена':
                        return 0

                    else:
                        send_message(vk, confirm_chat_id, f"Команда не распознана!\n{respond_text}")
