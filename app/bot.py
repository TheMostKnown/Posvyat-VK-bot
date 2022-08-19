import vk_api
import psycopg2

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


from vk_tools import Keyboard
from vk_events import send_message
from vk_config import token_vk
from create_db import engine, get_session, guests, orgs, groups, info, tech_support, sendings
from admin_commands import is_commands

vk_session = vk_api.VkApi(token=token_vk)


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
