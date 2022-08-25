import json
from typing import Optional, List

import vk_api
from sqlalchemy import desc
from sqlalchemy.orm import Session
from vk_api.bot_longpoll import VkBotEvent

from app.vk_events.send_message import send_message
from app.vk_tools.admin_handler import admin_add_info
from app.create_db import Guests, Orgs, Groups, Sendings, Command
from app.vk_tools.utils.make_domain import make_domain


# args = [quantity]
def get_commands(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting commands from the Command table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    chat_id = event.raw[3]

    params = dict()

    commands = [{
        'name': command.name,
        'arguments': command.arguments,
        'info': command.desc
    } for command in session.query(Command)]

    if args:
        if not args[0].isdigit():
            return 9
        params['quantity'] = int(args[0])

    if params and 'quantity' in params.keys() and params['quantity'] < len(commands):
        # commands = sorted(commands, key=lambda i: i['date'], reverse=True)[:params['quantity']]
        commands = commands[:params['quantity']]
    commands = sorted(commands, key=lambda command: command['name'])

    message_texts = []
    if not commands:
        message_text = 'У вас нет доступных команд.'
    else:
        message_text = ''
        for i, command in enumerate(commands):

            if i and i % 50 == 0:
                message_texts.append(message_text)
                message_text = ''

            message_text += f'\n{i + 1}) {command["name"]} {command["arguments"]}  ({command["info"]}'

    message_texts.append(message_text)

    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


# args = [quantity]
def get_mailings(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting texts from the Text table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if args[0].isdigit():
            params['quantity'] = int(args[0])
        else:
            return 9

    texts = [{
        'mail_name': text.mail_name,
        'text': text.text,
        'groups': text.groups
    } for text in session.query(Sendings).all()]

    if params and 'quantity' in params.keys() and params['quantity'] < len(texts):
        texts = sorted(texts, key=lambda text: text['send_time'], reverse=True)[:params['quantity']]
    texts = sorted(texts, key=lambda text: text['mail_name'])

    message_texts = []
    if not texts:
        message_text = 'Список текстов пуст.'
    else:
        message_text = ''

        for i, text in enumerate(texts):

            if i and i % 50 == 0:
                message_texts.append[message_text]
                message_text = ''

            message_text += f'{i + 1}) "{text["mail_name"]}" уровни: {text["groups"]}\n'

    message_texts.append(message_text)

    chat_id = event.raw[3]

    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


# args = [{Guests.vk_link}, {Groups.number}]
def give_level(
        session: Session,
        args: Optional[List[str]] = None
) -> int:
    """ The function of updating a group from the Guest table in DB.

        :param vk: session for connecting to VK API
        :param session: session to connect to the database
        :param event: event object in VK
        :param args: arguments of the command entered

        :return: error number or 0
        """
    if len(args) < 2 or not args[0] or not args[1]:
        return 1

    user = session.query(Guests).filter_by(vk_link=args[0]).first()
    if not user:
        return 5

    if args[1].isdigit():
        if int(args[1]) not in {group.group_num for group in session.query(Groups)}:
            return 4

        user_groups = json.loads(user.groups)
        user_groups.append(int(args[1]))

        user.groups = json.dumps(user_groups)

    session.commit()
    return 0


# args = [quantity | Groups.group_num]
def get_guests(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting users from the Guests table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """

    params = {}
    if args:
        if not args[0].isdigit():
            return 9
        params['quantity'] = int(args[0])

    chat_id = event.raw[3]

    users = session.query(Guests).filter(Guests.chat_id != chat_id)
    if params and 'quantity' in params.keys() and params['quantity'] < users.count():
        users = users.order_by(desc(Guests.surname)).limit(params['quantity'])

    message_texts = []
    if not users.count():
        message_text = f'Пользователей в базе нет.'
    else:
        message_text = f'Сейчас есть информация о {users.count()} пользователях:\n\n'

        titles = {text.id: text.mail_name for text in session.query(Sendings)}

        for i, user in enumerate(users):
            if i and i % 5 == 0:
                message_texts.append(message_text)
                message_text = ''

            user_groups = user.groups if len(user.groups) != 0 else 'Без уровней'

            message_text += f'{i + 1}) {user.name} {user.surname} - vk.com/{user.vk_link}\n- Уровни: {user_groups}\n'

            if not user.texts or user.texts == '[None]':
                message_text += '- Нет полученных рассылок.\n\n'
            else:
                texts = json.loads(user.texts)
                message_text += '- Полученные рассылки - '
                for j, text in enumerate(texts):
                    if text in titles.keys():
                        message_text += '; '.join(sorted({f'"{titles[text]}"' for text in texts})) + '\n\n'

    message_texts.append(message_text)
    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


# args = [quantity | Groups.group_num]
def get_orgs(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting users from the Orgs table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """

    params = {}
    if args:
        if not args[0].isdigit():
            return 9
        params['quantity'] = int(args[0])

    chat_id = event.raw[3]

    users = session.query(Orgs)
    if params and 'quantity' in params.keys() and params['quantity'] < users.count():
        users = users.order_by(desc(Orgs.surname)).limit(params['quantity'])

    message_texts = []
    if not users.count():
        message_text = f'Пользователей в базе нет.'
    else:
        message_text = f'Сейчас есть информация о {users.count()} пользователях:\n\n'

        groups = {group.group_num: group.group_info for group in session.query(Groups)}

        for i, user in enumerate(users):
            if i and i % 5 == 0:
                message_texts.append(message_text)
                message_text = ''

            user_groups = user.groups if len(user.groups) != 0 else 'Без уровней'

            message_text += f'{i + 1}) {user.name} {user.surname} - vk.com/{user.vk_link}\n- Уровни - {user_groups}\n'

    message_texts.append(message_text)
    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


# args = [quantity]
def get_groups(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        event: Optional[VkBotEvent] = None,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting steps from the Groups table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param event: event object in VK
    :param args: arguments of the command entered

    :return: error number or 0
    """
    params = {}
    if args:
        if not args[0].isdigit():
            return 9
        params['quantity'] = int(args[0])

    groups = [{
        'group_num': group.group_num,
        'group_info': group.group_info,
    } for group in session.query(Groups).all()]

    if params and 'quantity' in params.keys() and params['quantity'] < len(groups):
        groups = sorted(groups, key=lambda group: group['group_num'], reverse=True)[:params['quantity']]
    groups = sorted(groups, key=lambda group: group['group_num'])

    message_texts = []
    if not groups:
        message_text = 'Список шагов пуст.'
    else:
        message_text = ''
        for i, group in enumerate(groups):
            if i and i % 50 == 0:
                message_texts.append(message_text)
                message_text = ''
            message_text += f'{group["group_num"]}) {group["group_info"]}\n'

    message_texts.append(message_text)

    chat_id = event.raw[3]

    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


def info(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        event: VkBotEvent,
        text: str
) -> None:

    if admin_add_info(session, text):
        send_message(vk, chat_id, "Вопрос добавлен")
    else:
        send_message(vk, chat_id, "Не удалось добавить вопрос")