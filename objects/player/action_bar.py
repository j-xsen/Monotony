from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from objects.notifier import Notifier


class ActionBar(Notifier):
    def __init__(self):
        """
        Holds the box with the different actions available.
        """
        Notifier.__init__(self, 'actionbar')
        # Load activity textures
        self.drawn_square = loader.loadModel('art/activities/drawn_square.egg')

        # create image
        self.white_square = OnscreenImage(image='art/action_bar.png', scale=(0.87, 0.4, 0.4),
                                          pos=(0.425, 0, .55))
        self.white_square.setTransparency(TransparencyAttrib.MAlpha)

        self.actions = []
        self.temp = []

    def add_action(self, new_action):
        self.actions.append(new_action)

    def delete_actions(self, temp=False):
        for action in self.actions if not temp else self.temp:
            action.destroy_button()

    def set_actions(self, actions):
        self.delete_actions()

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
            action.set_pos(pos[len(self.actions)][number])
            number += 1

    def hide(self):
        self.notify.debug("[hide] Hiding actions...")
        self.temp = self.actions
        self.delete_actions()

    def show(self):
        self.notify.debug("[show] Showing actions...")
        self.set_actions(self.temp)
