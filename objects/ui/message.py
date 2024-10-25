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
        self.player.enable_actions()
        self.container.destroy()

    def create_button(self):
        Action.create_button(self)
        self.set_pos((0, 0, -.2))


class Message(Panel):
    def __init__(self, player, title, message):
        Panel.__init__(self,"Message", frame_size=(size, -size, size, -size))
        player.disable_actions()
        self.title = title
        self.message = message
        self.close_button = CloseAction(player, self)
        self.close_button.button.reparentTo(self.background)
