import vk_api
from sqlalchemy.orm import Session
from vk_api.longpoll import VkLongPoll, VkEventType

from config import settings
from create_db import engine
from vk_tools.utils import dispatcher
from vk_tools.filters.admin import is_admin

session = Session(bind=engine)

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()


def start():

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
                        session=session,
                        chat_id=chat_id,
                        event=event,
                        text=text
                    )

