from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    """"
    class for generating and getting keyboards from list of buttons

    :param button: buttons for current keyboard
    :type button: list
    :param one_time: if the keyboard is need to be used once or not
    :type one_time: bool
    :param inline: shows keyboard inside the message if true
    :type inline: bool
    """
    def __init__(self, buttons: list, one_time=False, inline=False):
        self.one_time = one_time
        self.inline = inline
        self.buttons = buttons
        self.keyboard = VkKeyboard(self.one_time, self.inline)
    
    def get(self):
        for count, button in enumerate(self.buttons):
            self.keyboard.add_button(button)
            if count != (len(self.buttons)-1):
                self.keyboard.add_line()

        return self.keyboard
    

