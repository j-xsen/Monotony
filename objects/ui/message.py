from direct.gui.DirectButton import DirectButton

from objects.locations.action import Action
from objects.ui.panel import Panel

size = .45

class CloseAction(Action):
    def __init__(self, player, container):
        Action.__init__(self, "Close", player)
        self.create_button()
        self.container = container

    def command(self):
        self.container.message_destroy()


class Message(Panel):
    def __init__(self, player, title, message):
        Panel.__init__(self,"Message", frame_size=(size, -size, size, -size))
        self.title = title
        self.message = message
        self.close = CloseAction(player, self)

    def message_destroy(self):
        self.close.destroy_button()
        self.destroy()
