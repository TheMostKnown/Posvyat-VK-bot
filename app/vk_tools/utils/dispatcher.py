import re
import logging

import vk_api
from sqlalchemy.orm import Session
from vk_api.bot_longpoll import VkBotEvent

from app.vk_tools.utils import admin_commands, user_commands
from app.vk_events.send_message import send_message
from app.vk_events.mailing import messages as start_mailing, messages_by_domain as start_mailing_by_domain
from app.vk_events.issues import open_issues
from app.vk_tools.utils.admin_commands import restart_parser
from app.config import settings
from app.create_db import Info

logger = logging.getLogger(__name__)


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

    elif command == '/update_timer':
        admin_commands.update_timer(session=session, args=args)

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

    elif command == '/restart_parser':
        restart_parser(
            vk=vk,
            session=session,
            spreadsheet_id=settings.GOOGLE_TABLE_ID,
            creds_file_name=settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
            token_file_name=settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
        )

    elif command == '/close_tech':
        admin_commands.close_tech(
            vk=vk,
            session=session,
            chat_id=chat_id,
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
        vk_session: vk_api.vk_api.VkApi,
        session: Session,
        chat_id: int,
        event: VkBotEvent,
        text: str
) -> None:
    logger.info(f'Inside call_guest, received message "{text}"')

    if text.lower() == 'информация':
        user_commands.get_information(
            vk=vk,
            vk_session=vk_session,
            chat_id=chat_id,
            session=session,
            event=event
        )

    elif text.lower() == 'что пропустил?':
        user_commands.what_missed(
            vk=vk,
            chat_id=chat_id,
            session=session,
            event=event
        )

    elif text.lower() == 'техподдержка':
        user_commands.tech_support(
            vk=vk,
            chat_id=chat_id,
        )

    elif text in [information.question for information in session.query(Info).all()]:
        user_commands.send_answer(
            vk=vk,
            chat_id=chat_id,
            session=session,
            event=event
        )
    elif text.lower().startswith('tech_support'):
        user_commands.send_tech_support(
            vk=vk,
            chat_id=chat_id,
            session=session,
            event=event
        )

    else:
        user_commands.main_menu(
            vk=vk,
            chat_id=chat_id,
            event=event
        )


def split_command_text(text: str) -> dict:
    words = text.split(' ')
    command_name = words[0].lower()
    args = re.findall('<(.*?)>', text, re.DOTALL)

    return {'command': command_name, 'args': args}
