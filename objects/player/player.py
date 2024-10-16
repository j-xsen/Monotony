from codes.locations import *
from objects.locations.home import Home
from objects.player.action_bar import ActionBar
from objects.notifier import Notifier
from objects.player.clock import Clock
from objects.player.selfportrait import SelfPortrait
from objects.player.statswidget import StatsWidget


class Stat:
    def __init__(self, value, max=100, min=0):
        """
        An integer with a minimum and maximum
        @param value: Value of the Stat
        @param max: Highest the Stat can go (default: 100)
        @param min: Lowest the Stat can go (default: 0)
        """
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
        """
        Adjust self.value within self.max and self.min
        @param adjust: Amount to add to self.value
        @return: Int new self.value
        """
        rtrn = int(self.value) + adjust
        if rtrn > self.max:
            return self.max
        elif rtrn < self.min:
            return self.min
        return rtrn


class Player(Notifier):
    def __init__(self):
        """
        Player object
        @param clock: Clock object
        """
        Notifier.__init__(self, "player")

        self.location_dict = {
            HOME: Home
        }

        self.self_portrait = SelfPortrait()
        self.action_bar = ActionBar()
        self.location = HOME
        self.location_object = None
        self.active = True  # this is if the player can take an action
        self.hygiene = Stat(20)
        self.hunger = Stat(20)
        self.in_bed = True  # checks if to add or remove from self.sleep
        self.sleep = Stat(100)
        self.money = 0
        self.head_to_location(HOME)

        self.clock = Clock(self)
        self.stats_widget = StatsWidget(self)

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
