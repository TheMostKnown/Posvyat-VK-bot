import vk_api
from sqlalchemy.orm import Session
from vk_api.bot_longpoll import VkBotEvent

from app.vk_tools.utils import admin_commands, user_commands
from app.vk_events.send_message import send_message
from app.vk_events.mailing import messages as start_mailing
from app.vk_events.issues import open_issues

def call_admin_command(
        vk: vk_api.vk_api.VkApiMethod,
        session: Session,
        chat_id: int,
        event: VkBotEvent,
        text: str
) -> None:
    text_split = text.split(sep=" ")
    command = text_split[0]

    if command == '/get_commands':
        admin_commands.get_commands(
            vk=vk,
            session=session,
            event=event,
            args=text_split[1] if len(text_split) > 1 else None
        )

    elif command == '/get_mailing':
        admin_commands.get_mailings(
            vk=vk,
            session=session,
            event=event,
            args=text_split[1] if len(text_split) > 1 else None
        )

    elif command == '/get_guests':
        admin_commands.get_guests(
            vk=vk,
            session=session,
            event=event,
            args=text_split[1] if len(text_split) > 1 else None
        )

    elif command == '/get_orgs':
        admin_commands.get_orgs(
            vk=vk,
            session=session,
            event=event,
            args=text_split[1] if len(text_split) > 1 else None
        )

    elif command == '/get_groups':
        admin_commands.get_groups(
            vk=vk,
            session=session,
            event=event,
            args=text_split[1] if len(text_split) > 1 else None
        )

    elif command == '/give_level':
        admin_commands.give_level(
            session=session,
            args=text_split[1:3] if len(text_split) > 2 else None
        )

    elif command == '/start_mailing':
        start_mailing(
            vk=vk,
            session=session,
            args=text_split[1] if len(text_split) > 1 else None
        )

    elif command == '/get_open_issues':
        open_issues(vk=vk, session=session)

    else:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text='Такой команды не существует'
        )


def call_guest_command(
        vk: vk_api.vk_api.VkApiMethod,
        vk_session: vk_api.vk_api.VkApi,
        session: Session,
        chat_id: int,
        event: VkBotEvent,
        text: str
) -> None:

    if text == 'информация':
        user_commands.get_information(
            vk=vk,
            vk_session=vk_session,
            session=session,
            event=event
        )
            
    elif text == 'что пропустил?':
        user_commands.what_missed(
            vk=vk,
            session=session,
            event=event
        )
        
    elif text == 'техподдержка':
        user_commands.tech_support(
            vk=vk,
            vk_session=vk_session,
            session=session,
            event=event
        )

    else:
        user_commands.main_menu(
            vk=vk,
            event=event
            )