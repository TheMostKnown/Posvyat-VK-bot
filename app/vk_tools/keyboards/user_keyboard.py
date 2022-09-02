from app.vk_tools.keyboards.keyboard import Keyboard

main_keyboard = Keyboard(buttons=['Информация', 'Что пропустил?', 'Техподдержка']).get()


def info_keyboard(availiable_info):
    info_buttons = availiable_info.copy()
    info_buttons.append('назад')
    return Keyboard(buttons=info_buttons).get()
