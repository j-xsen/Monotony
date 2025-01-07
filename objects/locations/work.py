import random

from direct.gui.DirectGui import DGG
from direct.showbase.DirectObject import DirectObject

from objects.locations.location import Location
from objects.notifier import Notifier
from objects.ui.action import Action
from objects.ui.selfportrait import DRIVING, PERSON


class WorkAction(Action, DirectObject):
    def __init__(self, index):
        Action.__init__(self, str(index))
        self.number = 0
        self.text_scale = 0.08
        self.index = index

        self.accept("randomize", self.randomize)

    def randomize(self):
        self.number = random.randrange(10, 100)
        self.text_node.setText(str(self.number))

    def command(self):
        messenger.send("pressed_card", [self.index, self.number])


class Work(Location):
    def __init__(self, action_bar):
        Location.__init__(self, action_bar)
        self.notify.debug("[__init__] Creating Work location")
        messenger.send("update_state", [DRIVING])
        self.actions = [
            [

            ],
            [
                WorkAction(0),
                WorkAction(1),
                WorkAction(2),
                WorkAction(3),
                WorkAction(4),
            ]
        ]

        self.randomize_cards()

        self.click_order = []

        self.accept("pressed_card", self.pressed_card)

    def set_stage(self, stage):
        super().set_stage(stage)
        if stage == 0:
            taskMgr.doMethodLater(0.5, self.show_cards, "Driving")

    def pressed_card(self, index, number):
        self.actions[1][index].disable_button()
        self.click_order.append(number)

        if self.check_if_all_clicked():
            self.check_cards()

    def check_if_all_clicked(self):
        for action in self.actions[1]:
            if action.button['state'] == DGG.NORMAL:
                return False
        return True

    def check_cards(self):
        min = 0
        for number in self.click_order:
            if number < min:
                self.reset_cards()
                return False
            min = number
        messenger.send("profit")
        self.reset_cards()
        return True

    def reset_cards(self):
        self.delete_all_card_buttons()
        self.randomize_cards()
        self.enable_all_cards()

    def randomize_cards(self):
        self.click_order = []
        for i in range(0, 5):
            self.actions[1][i].randomize()

    def enable_all_cards(self):
        counter = 0
        for card in self.actions[1]:
            card.create_button()
            self.actions[1][counter].set_pos(self.action_bar.pos[5][counter])
            counter += 1

    def delete_all_card_buttons(self):
        for card in self.actions[1]:
            card.destroy_button()

    def show_cards(self, e):
        self.set_stage(1)
        messenger.send("update_state", [PERSON])
