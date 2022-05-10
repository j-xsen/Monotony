"""
This class is the portrait on the top-left
"""
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from codes.selfportraitstates import *
from objects.notifier import Notifier


class SelfPortrait(Notifier):

    def __init__(self):
        Notifier.__init__(self, "selfportrait")
        self.state = PERSON
        self.image = OnscreenImage(image='art/portraits/person.png', scale=0.4, pos=(-.88, 0, .55))
        self.image.setTransparency(TransparencyAttrib.MAlpha)
        self.white_square = OnscreenImage(image='art/white_square.png', scale=0.4, pos=(-.88, 0, .55))
        self.white_square.setTransparency(TransparencyAttrib.MAlpha)
        self.update_state(SLEEPING)

    def update_state(self, new_state):
        if self.state != new_state:
            if new_state in self_portrait_dict:
                self.state = new_state
                self.image.setImage(self_portrait_dict[self.state])
                self.image.setTransparency(TransparencyAttrib.MAlpha)
                return True
            else:
                self.notify.warning(f"Invalid new_state {new_state}!")
        return False

    def destroy(self):
        self.image.destroy()
