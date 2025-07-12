import random

from direct.gui.DirectGui import DGG
from direct.interval.IntervalManager import ivalMgr
from direct.interval.LerpInterval import LerpColorInterval
from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableString

from objects.locations.location import Location, HOME
from objects.ui.uiconstants import UIConstants
from objects.ui.action import Action
from objects.ui.actionbar import ActionBar
from objects.ui.selfportrait import DRIVING, PERSON


class GoHome(Action):
    def __init__(self):
        Action.__init__(self, "Go Home")

    def command(self):
        messenger.send("set_stage", [3])
        messenger.send("update_state", [DRIVING])

class WorkAction(Action, DirectObject):
    def __init__(self, index: int):
        """
        A special action for the Work scene's minigame.
        :param index: The index of the action (0-4)
        :type index: int
        """
        Action.__init__(self, str(index))
        self.number = 0
        self.text_scale = 0.08
        self.index = index
        self.pressed = False

        self.accept("randomize", self.randomize)

    def enable_button(self):
        if not self.pressed:
            Action.enable_button(self)

    def disable_button(self):
        flashing_interval = ivalMgr.getInterval(f"flashing_action_bar{self.index}")
        if flashing_interval:
            ivalMgr.removeInterval(flashing_interval)
        Action.disable_button(self)

    def randomize(self):
        self.pressed = False
        self.number = random.randrange(10, 100)
        self.text_node.setText(str(self.number))

    def command(self):
        self.pressed = True
        base.loader.loadSfx("art/sounds/work_card.ogg").play()
        messenger.send("pressed_card", [self.index, self.number])


class Work(Location):
    ENDTIME=int(ConfigVariableString('work-end', '1700').getValue())
    def __init__(self, action_bar: ActionBar):
        Location.__init__(self, action_bar, "Work")
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
            ],
            [
                GoHome(),
            ],
            []
        ]

        self.randomize_cards()

        self.click_order = []

        self.accept("pressed_card", self.pressed_card)
        self.accept(self.ENDTIME, self.works_done)

    def head_home_message(self, e):
        messenger.send("head_to_location", [HOME, 2])

    def set_stage(self, stage: int):
        super().set_stage(stage)
        if stage == 0:
            taskMgr.doMethodLater(0.5, self.show_cards, "DrivingWork")
        elif stage == 3:
            taskMgr.doMethodLater(0.5, self.head_home_message, "DrivingHome")

    def works_done(self):
        messenger.send("add_log", ["Time to clock out."])
        self.set_stage(2)
        self.notify.debug("[works_done] Work is finished (" + str(self.ENDTIME) + ")")

    def pressed_card(self, index: int, number: int):
        """
        Ran when a card is pressed. Disables card and adds to the click order.
        :param index: The index of the card.
        :type index: int
        :param number: Number of the card.
        :type number: int
        """
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
        success = True
        for number in self.click_order:
            if number < min:
                success = False
                break
            min = number

        # pay player if they won
        if success:
            messenger.send("profit")

        # sounds
        sounds = [
            ["art/sounds/fail_1.ogg",
             "art/sounds/fail_2.ogg",
             "art/sounds/fail_3.ogg",],
            ["art/sounds/success_1.ogg",
            "art/sounds/success_2.ogg",
            "art/sounds/success_3.ogg",]
        ]
        chosen_sound = base.loader.loadSfx(random.choice(sounds[success]))
        chosen_sound.setVolume(0.3)
        chosen_sound.play()

        self.reset_cards()
        self.flash_action_bar(not success)

        return success

    def flash_action_bar(self, is_red: bool):
        color = (1, 0, 0, 1) if is_red else (0, 1, 0, 1)
        lerpcolor = LerpColorInterval(self.action_bar.background, 1, UIConstants.COLOR_ENABLE, color)
        lerpcolor.start()
        for action in self.actions[self.stage]:
            new_color = LerpColorInterval(action.button, 1, UIConstants.COLOR_ENABLE, color,
                                          name=f"flashing_action_bar{action.index}")
            new_color.start()

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
