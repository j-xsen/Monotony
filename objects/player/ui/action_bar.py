from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from objects.notifier import Notifier
from objects.player.ui.panel import Panel


class ActionBar(Panel):
    def __init__(self):
        """
        Holds the box with the different actions available.
        """
        Panel.__init__(self, "actionbar")
        self.background.setScale((0.87, 0.4, 0.4))
        self.background.setPos((0.425, 0, .55))

        # drawn square texture for actions
        self.drawn_square = loader.loadModel('art/activities/drawn_square.egg')

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
        self.temp = []
