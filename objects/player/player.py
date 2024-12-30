from panda3d.core import ConfigVariableString
from objects.locations.home import Home
from objects.locations.work import Work
from objects.ui.action_bar import ActionBar
from objects.notifier import Notifier
from objects.clock import Clock
from objects.ui.detailrectangle import DetailRectangle
from objects.ui.message import Message
from objects.ui.selfportrait import SelfPortrait, EATING, PERSON, BATHING
from objects.ui.statswidget import StatsWidget
from objects.player.stat import Stat
from objects.locations.location import HOME, WORK


class Player(Notifier):
    def __init__(self):
        """
        Player object
        @param clock: Clock object
        """
        Notifier.__init__(self, "player")

        # load font
        self.font = loader.loadFont("Monotony-Regular.ttf")
        self.font.setPixelsPerUnit(120)

        # load image for buttons
        self.drawn_square = loader.loadModel('art/drawn_square.egg').find("**/drawn_square")

        # Collection of notes
        self.notes = []

        # Ability to act
        self.able = True

        # Widgets
        self.self_portrait = SelfPortrait()
        self.action_bar = ActionBar()
        self.clock = Clock(self)
        self.detail_rectangle = DetailRectangle(self)

        # Location
        self.location_dict = {
            HOME: Home,
            WORK: Work
        }
        self.location = None
        self.head_to_location(HOME)

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

        self.stats_widget = StatsWidget(self)

    def head_to_location(self, destination, stage=0):
        if destination in self.location_dict:
            self.location = self.location_dict[destination](self)
        else:
            return False

        self.location.set_stage(stage)

        return True

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
        self.self_portrait.update_state(BATHING)
        self.cleaning_amount = effect
        taskMgr.doMethodLater(duration, self.finish_bathing, "Bathing")
        if after:
            taskMgr.doMethodLater(duration, after, "AfterBathing")
        self.daze(duration)

    def finish_bathing(self, task):
        self.notify.debug(f"[finish_bathing] Finished bathing; restoring {self.cleaning_amount} to {self.hygiene}.")
        self.self_portrait.update_state(PERSON)
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
        self.self_portrait.update_state(EATING)
        self.consuming_calories += calories
        taskMgr.doMethodLater(daze_time, self.finish_eating, "Eating")
        if after:
            taskMgr.doMethodLater(daze_time, after, "PostEating")
        self.daze(daze_time)

    def finish_eating(self, task):
        self.notify.debug(f"[finish_eating] Finished eating; restoring {self.consuming_calories} to {self.hunger}.")
        self.hunger += self.consuming_calories
        self.consuming_calories = 0
        self.self_portrait.update_state(PERSON)

        self.stats_widget.update_stats()

    def daze(self, duration=5):
        self.action_bar.hide()
        taskMgr.doMethodLater(duration, self.undaze, 'DazePlayer')

    def undaze(self, task):
        self.action_bar.show()

    def add_note_(self, title, text):
        new_note = Message(title, text, self)
        self.notify.debug(f"[add_note_] Received note: {title}: {text[:10]}")
        self.notes.append(new_note)
        self.detail_rectangle.inventory.add(new_note)

    def enable_actions(self):
        self.able = True
        self.clock.start_clock()
        self.action_bar.enable_actions()

    def disable_actions(self):
        self.able = False
        self.clock.stop_clock()
        self.action_bar.disable_actions()
