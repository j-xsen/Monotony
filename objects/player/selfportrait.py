from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from objects.notifier import Notifier


PERSON = 0
EATING = 1
SLEEPING = 2
DRIVING = 3

self_portrait_dict = {
        PERSON: "art/portraits/person.png",
        EATING: "art/portraits/fork.png",
        SLEEPING: "art/portraits/bed.png",
        DRIVING: "art/portraits/car.png"
    }

class SelfPortrait(Notifier):

    def __init__(self):
        """
        Portrait on the left
        """
        Notifier.__init__(self, "selfportrait")
        self.state = PERSON
        self.image = OnscreenImage(image='art/portraits/person.png', scale=0.375, pos=(-.88, 0, .55))
        self.image.setTransparency(TransparencyAttrib.MAlpha)
        self.white_square = OnscreenImage(image='art/white_square.png', scale=0.4, pos=(-.88, 0, .55))
        self.white_square.setTransparency(TransparencyAttrib.MAlpha)
        self.update_state(SLEEPING)

    def update_state(self, new_state):
        """
        Updates self.state and changes image accordingly
        @param new_state: New portrait state
        """
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
