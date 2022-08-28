import json
import logging
import re
import time

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from app.config import settings
from app.create_db import get_session, engine, Guests, Sendings
from app.vk_tools.utils import dispatcher
from app.vk_tools.filters.admin import is_admin
from app.vk_tools.google.spreadsheet_parser.commands.export_to_db import get_init_data
from app.vk_events.send_message import send_message

# connecting to db
session = get_session(engine)

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()


def start():

    # Подключение логов
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # filling database with actual entries
    get_init_data(
        session,
        settings.GOOGLE_TABLE_ID,
        settings.DIR_NAME + settings.GOOGLE_CREDS_PATH,
        settings.DIR_NAME + settings.GOOGLE_TOKEN_PATH
    )

    logger.info('Parsing successful')

    while True:

        try:
            logger.info('Bot has launched')

            for event in VkBotLongPoll(vk=vk_session, group_id=settings.VK_GROUP_ID, wait=25).listen():

                # if vk group received new message
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                    logger.info(f'Received message from chat_id={event.message["from_id"]}: "{event.message["text"]}"')

                    chat_id = int(event.message['from_id'])

                    # if user is new -> add him to db and send welcome message
                    if chat_id not in {i[0] for i in session.query(Guests.chat_id).all()}:

                        # getting info about user
                        user_info = vk.users.get(user_id=chat_id, fields='domain')[0]
                        user_groups = json.dumps([1, 2]) \
                            if vk.groups.isMember(group_id=settings.VK_GROUP_ID, user_id=chat_id) == 1 \
                            else json.dumps([1])

                        session.add(
                            Guests(
                                chat_id=chat_id,
                                surname=user_info['last_name'],
                                name=user_info['first_name'],
                                patronymic='',
                                phone_number='',
                                tag='',
                                vk_link=user_info['domain'],
                                groups=user_groups,
                                texts=json.dumps([])
                            )
                        )
                        logger.info(
                            f'Added new user: '
                            f'chat_id="{chat_id}", '
                            f'link=vk.com/{user_info["domain"]}'
                        )

                        welcome_text = session.query(Sendings).filter_by(mail_name='welcome').first()

                        if welcome_text:
                            send_message(
                                vk=vk,
                                chat_id=chat_id,
                                text=welcome_text.text
                            )

                        send_message(
                            vk=vk,
                            chat_id=settings.TECH_SUPPORT_VK_ID,
                            text=f'Пользователь vk.com/{user_info["domain"]} ({chat_id}) написал боту'
                        )

                    session.commit()

                    if not event.message['text'] or event.message['text'][0] != '/':

                        # finishing work with db
                        session.commit()
                        session.close()

                        time.sleep(settings.DELAY)

                    else:
                        logger.info(f'user_id="{chat_id}" has just invoked command {event.message["text"]}')

                        if is_admin(session=session, chat_id=chat_id):
                            dispatcher.call_admin_command(
                                vk=vk,
                                session=session,
                                chat_id=chat_id,
                                event=event,
                                text=event.message['text']
                            )

                        else:
                            dispatcher.call_guest_command(
                                vk=vk,
                                vk_session=vk_session,
                                session=session,
                                chat_id=chat_id,
                                event=event,
                                text=event.message['text']
                            )

        except Exception as e:
            logger.error(e)
