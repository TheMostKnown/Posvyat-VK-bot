from .keyboard import Keyboard

def user_info_keyboard(user_query):
    info_buttons = []
    for i in user_query:
        info_buttons.append(i.question)
    return Keyboard(buttons = info_buttons)