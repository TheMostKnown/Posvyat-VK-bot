import logging
from app.vk_tools.keyboards.keyboard import Keyboard

logger = logging.getLogger(__name__)

main_keyboard = Keyboard(buttons=['Информация', 'Что пропустил?', 'Техподдержка']).get()


def info_keyboard(availiable_info):
    info_buttons = availiable_info.copy()
    info_buttons.append('назад')
    logger.info(f"Получены информационные кнопки {info_buttons}")
    return Keyboard(buttons=info_buttons).get()

def missed_keyboard(availiable_missing):
    missed_buttons = availiable_missing.copy()
    missed_buttons.append('назад')
    logger.info(f"Получены кнопки что пропустил {missed_buttons}")
    return Keyboard(buttons=missed_buttons).get()
