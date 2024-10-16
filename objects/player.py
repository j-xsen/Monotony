from codes.locations import *
from locations.home import Home
from objects.notifier import Notifier


class Stat:
    def __init__(self, value, max=100, min=0):
        self.value = value
        self.max = max
        self.min = min

    def __add__(self, other):
        self.value = self.change_value(other)
        return self

    def __sub__(self, other):
        self.value = self.change_value(-other)
        return self

    def __str__(self):
        return f"{self.value}"

    def change_value(self, adjust):
        rtrn = int(self.value) + adjust
        if rtrn > self.max:
            return self.max
        elif rtrn < self.min:
            return self.min
        return rtrn


class Player(Notifier):

    def __init__(self, level_holder, clock):
        Notifier.__init__(self, "player")

        self.level_holder = level_holder
        self.clock = clock

        self.location_dict = {
            HOME: Home
        }

        self.location = HOME
        self.location_object = None
        self.active = True  # this is if the player can take an action
        self.hygiene = Stat(20)
        self.hunger = Stat(20)
        self.in_bed = True
        self.sleep = Stat(100)
        self.money = 0
        self.head_to_location(HOME)

    def head_to_location(self, destination, stage=0):
        if destination in self.location_dict:
            self.location_object = self.location_dict[destination](self)
        else:
            return False

        self.location_object.set_stage(stage)

        return True

    def deteriorate(self):
        self.hunger -= 10
        self.hygiene -= 10
        if self.in_bed:
            self.sleep += 10
        else:
            self.sleep -= 5
