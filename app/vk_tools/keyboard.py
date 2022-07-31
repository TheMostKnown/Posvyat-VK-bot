
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
    def __init__(self, button: list, one_time=False, inline=False):
        self.one_time = one_time
        self.inline = inline

        self.keyboard = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": button
        }

    

