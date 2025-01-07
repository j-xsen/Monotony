from direct.showbase.DirectObject import DirectObject
from panda3d.core import ConfigVariableString

from objects.notifier import Notifier
from objects.player.stat import Stat
from objects.ui.selfportrait import EATING, PERSON, BATHING
from objects.ui.statswidget import StatsWidget


class Player(Notifier, DirectObject):
    def __init__(self, clock):
        """
        Player object
        @param clock: Clock object
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
        self.money = 0

        # Decay/Boost variables
        self.hunger_decay = int(ConfigVariableString('hunger-decay', '10').getValue())
        self.sleep_decay = int(ConfigVariableString('sleep-decay', '10').getValue())
        self.sleep_boost = int(ConfigVariableString('sleep-boost', '10').getValue())
        self.hygiene_decay = int(ConfigVariableString('hygiene-decay', '10').getValue())

        self.stats_widget = StatsWidget(self, clock)

        self.accept("add_note", self.add_note)
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
        self.hunger -= self.hunger_decay
        self.hygiene -= self.hygiene_decay
        if self.in_bed:
            self.sleep += self.sleep_boost
        else:
            self.sleep -= self.sleep_decay
        self.stats_widget.update_stats()

    def bathe(self, duration=2, effect=80, after=None):
        """
        The player takes a bath
        @param duration: How long it takes to wash
        @param effect: How much hygiene restored
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

    def feed(self, calories=20, daze_time=2, after=None):
        """
        Cheezburger
        @param calories: Amount of hunger to restore
        @param daze_time: How long to eat
        @param after: function to run after done eating
        """
        self.notify.debug(f"[feed] Start feeding: {daze_time}s for +{calories}.")
        messenger.send("update_state", [EATING])
        self.consuming_calories += calories
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
        messenger.send("ab_hide")
        messenger.send("clock_disable_pausing")
        messenger.send("inv_disable")
        taskMgr.doMethodLater(duration, self.undaze, 'DazePlayer')

    def undaze(self, task):
        messenger.send("clock_enable_pausing")
        messenger.send("inv_enable")
        messenger.send("ab_show")

    def add_note(self, note):
        self.notify.debug(f"[add_note_] Received note: {note.title}: {note.message[:10]}")
        note.display()

    def enable_actions(self):
        self.able = True

    def disable_actions(self):
        self.able = False

    def profit(self, amount=100):
        self.money += amount
        messenger.send("update_stats")

    def destroy(self):
        self.ignore_all()
