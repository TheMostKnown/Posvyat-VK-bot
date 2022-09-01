import json
from typing import Optional, List
import logging

import vk_api
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.vk_events.send_message import send_message
from app.vk_tools.admin_handler import admin_add_info
from app.create_db import Guests, Orgs, Groups, Sendings, Command, UpdateTimer
from app.vk_tools.google.spreadsheet_parser.commands.export_to_db import get_init_data

# Подключение логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# args = [quantity]
def get_commands(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting commands from the Command table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param chat_id: user id for sending message
    :param args: arguments of the command entered

    :return: error number or 0
    """

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
        chat_id: int,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting texts from the Text table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param chat_id: user id for sending message
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
        texts = texts[:params['quantity']]

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

    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


# args = [{Groups.number}]
def update_timer(
        session: Session,
        args: Optional[List[str]] = None
) -> None:
    """ The function of updating of autoparser's timing.

        :param session: session to connect to the database
        :param args: arguments of the command entered

        :return: None
    """
    timer = session.query(UpdateTimer).first()

    if args and args[0].isnumeric():
        if timer:
            timer.update_timer = args[0]
        else:
            session.add(UpdateTimer(update_timer=int(args[0])))


# args = [quantity | Groups.group_num]
def get_guests(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting users from the Guests table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param chat_id: user id for sending message
    :param args: arguments of the command entered

    :return: error number or 0
    """

    params = {}
    if args:
        if args[0].isdigit():
            params['quantity'] = int(args[0])
        if len(args) == 2 and args[0].isdigit():
            params['group'] = int(args[1])

    users = session.query(Guests)
    if params and 'quantity' in params.keys() and params['quantity'] < users.count():
        users = users.order_by(asc(Guests.surname)).limit(params['quantity'])

    message_texts = []
    if not users.count():
        message_text = f'Пользователей в базе нет.'
    else:
        message_text = f'Сейчас есть информация об этих пользователях:\n\n'

        titles = {text.id: text.mail_name for text in session.query(Sendings)}

        for i, user in enumerate(users):

            if params and 'group' in params.keys() and params['group'] not in json.loads(user.groups):
                continue

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
        chat_id: int,
        args: Optional[List[str]] = None
) -> int:
    """ The function of getting users from the Orgs table in DB.

    :param vk: session for connecting to VK API
    :param session: session to connect to the database
    :param chat_id: user id for sending message
    :param args: arguments of the command entered

    :return: error number or 0
    """

    params = {}
    if args:
        if args[0].isdigit():
            params['quantity'] = int(args[0])
        if len(args) == 2 and args[1].isdigit():
            params['group'] = int(args[1])

    users = session.query(Orgs)
    if params and 'quantity' in params.keys() and params['quantity'] < users.count():
        users = users.order_by(asc(Orgs.surname)).limit(params['quantity'])

    message_texts = []
    if not users.count():
        message_text = f'Пользователей в базе нет.'
    else:
        message_text = f'Сейчас есть информация о пользователях:\n\n'

        for i, user in enumerate(users):

            if params and 'group' in params.keys() and params['group'] not in json.loads(user.groups):
                continue

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
        chat_id: int,
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
        groups = sorted(groups, key=lambda group: group['group_num'])[:params['quantity']]
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

    for message_text in message_texts:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text=message_text
        )

    session.commit()
    return 0


def restart_parser(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        spreadsheet_id: str,
        creds_file_name: str,
        token_file_name: str
) -> None:
    get_init_data(
        vk=vk,
        session=session,
        spreadsheet_id=spreadsheet_id,
        creds_file_name=creds_file_name,
        token_file_name=token_file_name
    )
    update_timer(session)
    logger.info('Parser has restarted')


def info(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        text: str
) -> None:

    if admin_add_info(session, text):
        send_message(vk, chat_id, "Вопрос добавлен")
    else:
        send_message(vk, chat_id, "Не удалось добавить вопрос")
        