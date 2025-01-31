from objects.locations.location import Location, WORK
from objects.ui.action import Action, DelayedAction
from objects.ui.note import Note
from objects.ui.selfportrait import PERSON


class WakeUp(Action):
    def __init__(self):
        Action.__init__(self, "Wake Up")

    def command(self):
        messenger.send("set_stage", [1])  # location
        messenger.send("update_state", [PERSON])  # portrait
        messenger.send("wake_up")  # player
        self.add_log("Good morning Me!")


class GoToWork(Action):
    def __init__(self):
        Action.__init__(self, "Go to Work")

    def command(self):
        messenger.send("head_to_location", [WORK])


class Eat(DelayedAction):
    def __init__(self):
        DelayedAction.__init__(self, "Eat")

    def command(self):
        messenger.send("feed", [1, 60, self.post])

    def post(self, e):
        self.add_log("Delicious!")


class Bathe(DelayedAction):
    def __init__(self, ):
        Action.__init__(self, "Bathe")

    def command(self):
        messenger.send("bathe", [2, 80, self.post])

    def post(self, e):
        self.add_log("All clean.")


class Home(Location):
    def __init__(self, action_bar):
        Location.__init__(self, action_bar, "Home")
        self.notify.debug("[__init__] Creating Home location")
        self.actions = [
            [
                WakeUp()
            ],
            [
                Eat(),
                Bathe(),
                GoToWork()
            ]
        ]

    def set_stage(self, stage=0):
        Location.set_stage(self, stage)
        if stage == 0:
            welcome_note = Note("Welcome to Monotony!",
                                   "In this game, you live the life of someone with a 9-5 job, "
                                   "with every day being the same.\n\n"
                                   "The most important boxes that you need to keep an eye on are"
                                   " the lower-left and upper-right boxes.\n\n"
                                   "The lower-left box will hold both your characters' thoughts "
                                   "in the Log and any messages that you may want to refer back "
                                   "to, such as this one, in the Inventory.\n\n"
                                   "The upper-right box is where you will see the actions "
                                   "available to you.")
            messenger.send("add_note", [welcome_note])
