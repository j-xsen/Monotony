from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableString

from objects.notifier import Notifier
from objects.player.stat import Stat
from objects.ui.selfportrait import EATING, PERSON, BATHING
from objects.ui.statswidget import StatsWidget


class Player(Notifier, DirectObject):
    def __init__(self, clock):
        """
        Holds all the player information
        :param clock: The clock object
        :type clock: Clock
        """
        Notifier.__init__(self, "player")

        # Ability to act
        self.able = True

        # Stats
        self.hygiene = Stat(20)
        self.cleaning_amount = 0  # adds hygiene after bathing
        self.hunger = Stat(20)
        self.consuming_calories = 0  # adds calories when done eating
        self.sleep = Stat(100)
        self.in_bed = True  # Used for decay or boost checking
        self.money = Stat(0, 99999, -99999)

        # Decay/Boost variables
        self.hunger_decay = int(ConfigVariableString('hunger-decay', '10').getValue())
        self.sleep_decay = int(ConfigVariableString('sleep-decay', '10').getValue())
        self.sleep_boost = int(ConfigVariableString('sleep-boost', '10').getValue())
        self.hygiene_decay = int(ConfigVariableString('hygiene-decay', '10').getValue())

        self.stats_widget = StatsWidget(self, clock)

        self.accept("deteriorate", self.deteriorate)
        self.accept("disable_actions", self.disable_actions)
        self.accept("enable_actions", self.enable_actions)
        self.accept("wake_up", self.wake_up)
        self.accept("feed", self.feed)
        self.accept("bathe", self.bathe)
        self.accept("profit", self.profit)

    def wake_up(self):
        self.in_bed = False

    def deteriorate(self):
        """
        Hourly deductions in stats.
        """
        self.hunger -= self.hunger_decay
        self.hygiene -= self.hygiene_decay
        if self.in_bed:
            self.sleep += self.sleep_boost
        else:
            self.sleep -= self.sleep_decay
        self.stats_widget.update_stats()

    def bathe(self, duration=2, effect=80, after=None):
        """
        :param duration: Length of shower in seconds.
        :type duration: int
        :param effect: Effect on the player's hygiene stat.
        :type effect: int
        :param after: Function to run once the shower is complete.
        :type after: function
        """
        self.notify.debug(f"[bathe] Start bathing for {duration} seconds for {effect} hygiene.")
        messenger.send("update_state", [BATHING])
        self.cleaning_amount = effect
        taskMgr.doMethodLater(duration, self.finish_bathing, "Bathing")
        if after:
            taskMgr.doMethodLater(duration, after, "AfterBathing")
        self.daze(duration)

    def finish_bathing(self, task):
        self.notify.debug(f"[finish_bathing] Finished bathing; restoring {self.cleaning_amount} to {self.hygiene}.")
        messenger.send("update_state", [PERSON])
        self.hygiene += self.cleaning_amount
        self.cleaning_amount = 0
        self.stats_widget.update_stats()

    def feed(self, daze_time=2, effect=20, after=None):
        """
        :param daze_time: Number of seconds to halt player activity.
        :type daze_time: int
        :param effect: Effect on the player's hunger stat.
        :type effect: int
        :param after: Function to run once the player is done eating.
        :type after: function
        """
        self.notify.debug(f"[feed] Start feeding: {daze_time}s for +{effect}.")
        messenger.send("update_state", [EATING])
        self.consuming_calories += effect
        taskMgr.doMethodLater(daze_time, self.finish_eating, "Eating")
        if after:
            taskMgr.doMethodLater(daze_time, after, "PostEating")
        self.daze(daze_time)

    def finish_eating(self, task):
        self.notify.debug(f"[finish_eating] Finished eating; restoring {self.consuming_calories} to {self.hunger}.")
        self.hunger += self.consuming_calories
        self.consuming_calories = 0
        messenger.send("update_state", [PERSON])

        self.stats_widget.update_stats()

    def daze(self, duration=5):
        """
        :param duration: Length of time to block all player movement.
        :type duration: int
        """
        messenger.send("ab_hide")
        messenger.send("clock_disable_pausing")
        messenger.send("inv_disable")
        taskMgr.doMethodLater(duration, self.undaze, 'DazePlayer')

    def undaze(self, task):
        messenger.send("clock_enable_pausing")
        messenger.send("inv_enable")
        messenger.send("ab_show")

    def enable_actions(self):
        self.able = True

    def disable_actions(self):
        self.able = False

    def profit(self, amount=100):
        """
        :param amount: Money to give/subtract from player.
        :type amount: int
        """
        self.money += amount
        messenger.send("update_stats")

    def destroy(self):
        self.ignore_all()
