from objects.player.locations.home import Home
from objects.player.action_bar import ActionBar
from objects.notifier import Notifier
from objects.player.clock import Clock
from objects.player.selfportrait import SelfPortrait, EATING, PERSON
from objects.player.stats.statswidget import StatsWidget
from objects.player.stats.stat import Stat
from objects.player.locations.location import HOME
from direct.task import Task


class Player(Notifier):
    def __init__(self):
        """
        Player object
        @param clock: Clock object
        """
        Notifier.__init__(self, "player")

        # Location
        self.location_dict = {
            HOME: Home
        }
        self.location = None

        self.self_portrait = SelfPortrait()
        self.action_bar = ActionBar()
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
            self.location = self.location_dict[destination](self)
        else:
            return False

        self.location.set_stage(stage)

        return True

    def deteriorate(self):
        self.starve()
        self.stink()
        if self.in_bed:
            self.rest()
        else:
            self.tire()

    def stink(self):
        """
        Pee-ew!
        """
        self.hygiene -= 5

    def starve(self):
        """
        No cheezburger
        """
        self.hunger -= 10

    def feed(self, calories=10):
        """
        Cheezburger
        @param calories: Amount of hunger to restore
        """
        daze_time = 1
        self.self_portrait.update_state(EATING)
        self.hunger += calories
        taskMgr.doMethodLater(daze_time, self.finish_eating, "Eating")
        self.daze(daze_time)

    def finish_eating(self, task):
        self.self_portrait.update_state(PERSON)

    def tire(self):
        """
        Another hour awake
        """
        self.sleep -= 5

    def rest(self, power_boost=10):
        """
        Zzz...
        @param power_boost: Amount of sleep to restore
        """
        self.sleep += power_boost

    def daze(self, duration=5):
        self.action_bar.hide()
        taskMgr.doMethodLater(duration, self.undaze, 'DazePlayer')

    def undaze(self, task):
        self.action_bar.show()
