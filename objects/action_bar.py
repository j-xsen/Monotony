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

    def set_actions(self, actions):
        # delete old ones
        for action in self.actions:
            action.destroy_button()

        self.actions = actions

        image_scale = (0.1, 0, 0.1)
        scale = 10
        pos = {
            1: [
                (0.4, 0, 0.55)
            ],
            2: [
                (0.1, 0, 0.55),
                (0.8, 0, 0.55)
            ]
        }

        number = 0
        for action in self.actions:
            # set location and scale
            action.create_button()
            action.button.setPos(pos[len(self.actions)][number])
            number += 1

    def reset_actions(self):
        self.actions = []

