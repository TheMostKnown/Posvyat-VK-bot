import vk_api
from sqlalchemy.orm import Session
from vk_api.longpoll import VkLongPoll, VkEventType

from app.vk_tools.keyboards import user_keyboard
from vk_events import send_message
from app.config import settings
from create_db import engine, Info
from app.vk_tools.utils import admin_commands

session = Session(bind=engine)

vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
vk = vk_session.get_api()


def is_admin(id_p, event_p):

    group_id = vk_session.method("groups.getById", {"peer_id": event_p.peer_id})
    group_inf = vk_session.method("groups.getMembers", {"group_id": group_id[0]["id"], "filter": "managers"})

    for member in group_inf["items"]:

        if member["id"] == id_p:

            if member["role"] == "administrator" or "creator":
                return True
            else:
                return False


def start():

    for event in VkLongPoll(vk_session).listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            text = event.text.lower()

            is_commands(user_id, event, text, vk_session, is_admin)
