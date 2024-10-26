from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode

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
        self.title = DirectLabel(text=title, scale=0.1,
                                 text_font=player.font,
                                 pos=(0,0,.2), text_bg=(0, 0, 0, 1),
                                 text_fg=(1, 1, 1, 1),
                                 relief=None,parent=self.background)
        self.message = DirectLabel(text=message, scale=0.1,
                                   text_font=player.font,
                                   pos=(0,0,0), text_bg=(0, 0, 0, 1),
                                   text_fg=(1, 1, 1, 1),
                                   relief=None,parent=self.background)
        self.close_button = CloseAction(player, self)
        self.close_button.button.reparentTo(self.background)
        print(self.title.getBounds())

    def destroy(self):
        self.title.destroy()
        self.message.destroy()
        self.background.destroy()
        self.close_button.destroy_button()
