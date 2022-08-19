from app.vk_tools.keyboards.keyboard import Keyboard

main_keyboard = Keyboard(buttons=['Информация']).get()


def info_keyboard(user_query):
    info_buttons = []
    for i in user_query:
        info_buttons.append(i.question)
    return Keyboard(buttons = info_buttons).get()