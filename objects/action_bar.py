from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib


class ActionBar:
    def __init__(self):
        # create image
        self.white_square = OnscreenImage(image='art/action_bar.png', scale=(0.87, 0.4, 0.4),
                                          pos=(0.425, 0, .55))
        self.white_square.setTransparency(TransparencyAttrib.MAlpha)

        self.actions = []

    def add_action(self, new_action):
        self.actions.append(new_action)

    def reset_actions(self):
        self.actions = []

