import re

import vk_api
from sqlalchemy.orm import Session
from vk_api.bot_longpoll import VkBotEvent

from app.vk_tools.utils import admin_commands
from app.vk_events.send_message import send_message
from app.vk_events.mailing import messages as start_mailing, messages_by_domain as start_mailing_by_domain
from app.vk_events.issues import open_issues


def call_admin_command(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        event: VkBotEvent,
        text: str
) -> None:
    command_split = split_command_text(text)
    command = command_split['command']
    args = command_split['args'] if len(command_split['args']) > 0 else None

    if command == '/get_commands':
        admin_commands.get_commands(
            vk=vk,
            session=session,
            chat_id=chat_id,
            args=args
        )

    elif command == '/get_mailings':
        admin_commands.get_mailings(
            vk=vk,
            session=session,
            chat_id=chat_id,
            args=args
        )

    elif command == '/get_guests':
        admin_commands.get_guests(
            vk=vk,
            session=session,
            chat_id=chat_id,
            args=args
        )

    elif command == '/get_orgs':
        admin_commands.get_orgs(
            vk=vk,
            session=session,
            chat_id=chat_id,
            args=args
        )

    elif command == '/get_groups':
        admin_commands.get_groups(
            vk=vk,
            session=session,
            chat_id=chat_id,
            args=args
        )

    elif command == '/set_level':
        admin_commands.set_level(
            session=session,
            args=args
        )

    elif command == '/start_mailing':
        start_mailing(
            vk=vk,
            session=session,
            args=args
        )

    elif command == '/get_open_issues':
        open_issues(vk=vk, session=session)

    elif command == '/send_message':
        start_mailing_by_domain(
            vk=vk,
            session=session,
            args=args
        )

    else:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text='Не удалось выполнить. Возможно, такой команды не существует. См. /get_commands'
        )


def call_guest_command(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        event: VkBotEvent,
        text: str
) -> None:

    send_message(
        vk=vk,
        chat_id=chat_id,
        text='Не удалось выполнить. Возможно, такой команды не существует, или у Вас недостаточно прав'
    )


def split_command_text(text: str) -> dict:
    words = text.split(' ')
    command_name = words[0].lower()
    args = re.findall('<(.*?)>', text, re.DOTALL)

    return {'command': command_name, 'args': args}
