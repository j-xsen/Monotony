from objects.ui.action import Action
from objects.ui.panel import Panel


class ActionBar(Panel):
    def __init__(self):
        """
        Holds the box with the different actions available.
        """
        Panel.__init__(self, "actionbar",
                       frame_size=(1.7, 0, .8, 0),
                       pos=(-.4, 0, .18))

        self.actions = []
        self.temp = []

        self.pos = {
            0: [],
            1: [
                (0.45, 0, 0.575)
            ],
            2: [
                (0.1, 0, 0.575),
                (0.8, 0, 0.575)
            ],
            3: [
                (0.1, 0, 0.75),
                (0.8, 0, 0.75),
                (0.45, 0, 0.4)
            ],
            5: [
                (-.15, 0, 0.6),
                (.15, 0, 0.6),
                (0.45, 0, 0.6),
                (0.75, 0, 0.6),
                (1.05, 0, 0.6)
            ],
        }

        self.accept("set_actions", self.set_actions)
        self.accept("disable_actions", self.disable_actions)
        self.accept("enable_actions", self.enable_actions)
        self.accept("ab_hide", self.hide)
        self.accept("ab_show", self.show)

    def add_action(self, new_action: Action):
        self.actions.append(new_action)

    def delete_actions(self):
        for action in self.actions:
            action.destroy_button()

    def set_actions(self, actions: list[Action]):
        self.delete_actions()

        self.actions = actions

        number = 0
        for action in self.actions:
            # set location and scale
            action.create_button()
            action.set_pos(self.pos[len(self.actions)][number])
            number += 1

    def hide(self):
        self.notify.debug("[hide] Hiding actions...")
        self.temp = self.actions
        self.delete_actions()

    def show(self):
        self.notify.debug("[show] Showing actions...")
        self.set_actions(self.temp)
        self.temp = []

    def disable_actions(self):
        for action in self.actions:
            action.disable_button()

    def enable_actions(self):
        for action in self.actions:
            action.enable_button()

    def destroy(self):
        self.ignore_all()
