import logging

import vk_api
from sqlalchemy.orm import Session
from vk_api.longpoll import VkLongPoll, VkEventType

from app.config import settings
from app.create_db import engine
from app.vk_tools.utils import dispatcher
from app.vk_tools.filters.admin import is_admin
from app.vk_tools.spreadsheet_parser.commands.export_to_db import get_init_data

session = Session(bind=engine)

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()


def start():

    # filling database
    get_init_data(
        session,
        settings.GOOGLE_TABLE_ID,
        settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
    )

    print('Parsing successful')

    while True:

        for event in VkLongPoll(vk_session).listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:

                chat_id = event.user_id
                text = event.text.lower()

                if is_admin(session=session, chat_id=chat_id):
                    dispatcher.call_admin_command(
                        vk=vk,
                        session=session,
                        chat_id=chat_id,
                        event=event,
                        text=text
                    )

                else:
                    dispatcher.call_guest_command(
                        vk=vk,
                        vk_session=vk_session,
                        session=session,
                        chat_id=chat_id,
                        event=event,
                        text=text
                    )

