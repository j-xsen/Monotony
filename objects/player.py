from codes.locations import *
from locations.home import Home
from objects.notifier import Notifier


class Player(Notifier):

    def __init__(self, level_holder):
        Notifier.__init__(self, "player")

        self.level_holder = level_holder

        self.location_dict = {
            HOME: Home
        }

        self.location = HOME
        self.location_object = None
        self.active = True  # this is if the player can take an action
        self.hygiene = 100
        self.hunger = 100
        self.sleep = 100
        self.money = 100
        self.head_to_location(HOME)

    def head_to_location(self, destination, stage=0):
        if destination in self.location_dict:
            self.location_object = self.location_dict[destination](self)
        else:
            return False

        self.location_object.set_stage(stage)

        return True
