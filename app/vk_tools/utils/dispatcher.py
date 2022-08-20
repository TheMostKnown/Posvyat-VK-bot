import vk_api
from vk_api.bot_longpoll import VkBotEvent

from app.vk_tools.utils import admin_commands
from app.vk_events import send_message


def call_admin_command(
        chat_id: int,
        event: VkBotEvent,
        text: str,
        vk: vk_api.vk_api.VkApiMethod,
        is_admin: bool
) -> None:

    if text == '/commands':
        admin_commands.get_commands()

    else:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text='Такой команды не существует'
        )


def call_guest_command(
        chat_id: int,
        event: VkBotEvent,
        text: str,
        vk: vk_api.vk_api.VkApiMethod,
) -> None:

    if text == '/commands':
        admin_commands.get_commands()

    else:
        send_message(
            vk=vk,
            chat_id=chat_id,
            text='Не удалось выполнить. Возможно, такой команды не существует, или у Вас недостаточно прав'
        )
