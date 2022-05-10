from codes.locations import *
from locations.bed import Bed
from objects.notifier import Notifier


class Player(Notifier):

    location_dict = {
        BED: Bed,
        HOME: "art/portraits/eating.png",
    }

    def __init__(self, level_holder):
        Notifier.__init__(self, "player")

        self.level_holder = level_holder

        self.location = BED
        self.location_object = None
        self.active = True  # this is if the player can take an action
        self.hygiene = 100
        self.hunger = 100
        self.sleep = 100
        self.money = 100
        self.head_to_location(BED)

    def head_to_location(self, destination):
        if destination in self.location_dict:
            self.location_object = self.location_dict[destination](self.level_holder.action_bar)
        else:
            return False

        self.location_object.head_to()

        return True
