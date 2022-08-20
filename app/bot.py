import vk_api
from sqlalchemy.orm import Session
from vk_api.longpoll import VkLongPoll, VkEventType

from app.config import settings
from create_db import engine
from app.vk_tools.utils import dispatcher

session = Session(bind=engine)

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()


def start():

    for event in VkLongPoll(vk_session).listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            text = event.text.lower()

            dispatcher.call_command(
                chat_id=user_id,
                event=event,
                text=text,
                vk=vk
            )
