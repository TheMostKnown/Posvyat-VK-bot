import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_tools import Keyboard
from vk_events import send_message
from vk_config import token_vk


session = vk_api.VkApi(token=vk_token)


 def is_admin(id_p, event_p):

     flag = 0
     Group_id = session.method("groups.getById", {"peer_id": event_p.peer_id})
     GroupInf = session.method("groups.getMembers", {"group_id": Group_id[0]["id"], "filter": "managers"})

     for Member in GroupInf["items"]:
         if Member["id"] == id_p and (Member["role"] == "administrator" or "creator"):
             flag = 1

     return flag


 def start():
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
             text = event.text.lower()

             if text == "start":
                 if is_admin(user_id, event) == 1:
                     send_message(session, user_id, "Hi, admin!")
                 else:
                     send_message(session, user_id, "Hi, user!")

 start()