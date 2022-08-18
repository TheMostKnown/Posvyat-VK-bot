import vk_api
import psycopg2
from sqlalchemy.testing import db
from sqlalchemy.orm import Session, sessionmaker
from vk_api.longpoll import VkLongPoll, VkEventType

from vk_tools import user_keyboard
from vk_events import send_message
from vk_config import token_vk
from create_db import engine, get_session, guests, orgs, groups, info, tech_support, sendings
import admin_commands

session = Session(bind=engine)

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

            admin_commands.is_get_unread(user_id, event, text, vk_session, is_admin)

            admin_commands.is_get_orgs(user_id, event, text, vk_session, is_admin)

            admin_commands.is_get_members(user_id, event, text, vk_session, is_admin)

            admin_commands.is_get_members_all(user_id, event, text, vk_session, is_admin)

            admin_commands.is_give_level(user_id, event, text, vk_session, is_admin)

            admin_commands.is_start_mailing(user_id, event, text, vk_session, is_admin)

            admin_commands.is_start_mailing_all(user_id, event, text, vk_session, is_admin)

            admin_commands.is_get_mailings(user_id, event, text, vk_session, is_admin)

            admin_commands.is_commands(user_id, event, text, vk_session, is_admin)

            admin_commands.is_info(user_id, event, text, vk_session, session, is_admin)

            
            if text == "информация":
                send_message(vk_session, user_id, "Доступная информация:", keyboard = user_keyboard.info_keyboard(session.query(info)))
            else:
                send_message(vk_session, user_id, "Hi, user!", keyboard = user_keyboard.main_keyboard)
                
