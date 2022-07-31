import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_tools import Keyboard
from vk_events import send_message
from vk_config import token_vk


session = vk_api.VkApi(token=token_vk)


def start():

    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            text = event.text.lower()

            if text == "start":
                send_message(session, user_id, "Hello!")
