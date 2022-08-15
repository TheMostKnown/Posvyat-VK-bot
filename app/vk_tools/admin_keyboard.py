from .keyboard import Keyboard
from .admin_commands import *
"""
инициализация клавиатуры администратора
"""
admin_keyboard = Keyboard(buttons = [add_info]).get()
