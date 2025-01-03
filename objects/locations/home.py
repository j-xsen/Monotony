from objects.locations.location import Location, WORK
from objects.notifier import Notifier
from objects.ui.action import Action, DelayedAction
from objects.ui.selfportrait import PERSON


class WakeUp(Action):
    def __init__(self, player):
        Action.__init__(self, "Wake Up", player)

    def command(self):
        if Action.command(self):
            # change stage
            self.player.location.set_stage(1)
            # update portrait
            self.player.self_portrait.update_state(PERSON)
            # change player variable for deteriorate
            self.player.in_bed = False
            self.add_log("Good morning Me!")


class GoToWork(Action):
    def __init__(self, player):
        Action.__init__(self, "Go to Work", player)

    def command(self):
        if Action.command(self):
            self.player.head_to_location(WORK)


class Eat(DelayedAction):
    def __init__(self, player):
        Action.__init__(self, "Eat", player)

    def command(self):
        if Action.command(self):
            self.player.feed(calories=60, daze_time=1, after=self.post)

    def post(self, e):
        self.add_log("Delicious!")


class Bathe(DelayedAction):
    def __init__(self, player):
        Action.__init__(self, "Bathe", player)

    def command(self):
        if Action.command(self):
            self.player.bathe(duration=2, effect=80, after=self.post)

    def post(self, e):
        self.add_log("All clean.")


class Home(Location, Notifier):
    def __init__(self, player):
        """
        Home Location object
        @param player: Player object
        """
        Location.__init__(self, player)
        Notifier.__init__(self, "home")
        self.notify.debug("[__init__] Creating Home location")

        self.actions = [
            [
                WakeUp(player)
            ],
            [
                Eat(player),
                Bathe(player),
                GoToWork(player)
            ]
        ]

    def set_stage(self, stage):
        super().set_stage(stage)
        if stage == 0:
            self.player.add_note("Welcome to Monotony!", "In this game, you live the life of someone with a 9-5 job, "
                                                         "with every day being the same.\n\n"
                                                         "The most important boxes that you need to keep an eye on are"
                                                         " the lower-left and upper-right boxes.\n\n"
                                                         "The lower-left box will hold both your characters' thoughts "
                                                         "in the Log and any messages that you may want to refer back "
                                                         "to, such as this one, in the Inventory.\n\n"
                                                         "The upper-right box is where you will see the actions "
                                                         "available to you.")
            self.player.notes[0].display()
