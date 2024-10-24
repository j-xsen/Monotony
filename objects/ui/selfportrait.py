from direct.gui.DirectFrame import DirectFrame
from panda3d.core import TransparencyAttrib
from objects.ui.panel import Panel

PERSON = 0
EATING = 1
SLEEPING = 2
DRIVING = 3
BATHING = 4

self_portrait_dict = {
    PERSON: "art/portraits/person.png",
    EATING: "art/portraits/fork.png",
    SLEEPING: "art/portraits/bed.png",
    DRIVING: "art/portraits/car.png",
    BATHING: "art/portraits/bath.png"
}


class SelfPortrait(Panel):

    def __init__(self):
        """
        Portrait on the left
        """
        Panel.__init__(self, "selfportrait",
                       frame_size=(.8, 0, .8, 0),
                       pos=(-1.25, 0, .18))
        self.state = PERSON

        self.image = DirectFrame(image='art/portraits/person.png',
                                 image_scale=0.35,
                                 image_pos=(0.4, 0, 0.4),
                                 parent=self.background)

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
