from objects.locations.action import Action
from objects.locations.location import Location
from objects.notifier import Notifier
from objects.ui.selfportrait import PERSON


class WakeUp(Action):
    def __init__(self, player):
        Action.__init__(self, "Wake Up", player)

    def command(self):
        # change stage
        self.player.location.set_stage(1)
        # update portrait
        self.player.self_portrait.update_state(PERSON)
        # change player variable for deteriorate
        self.player.in_bed = False


class Eat(Action):
    def __init__(self, player):
        Action.__init__(self, "Eat", player)

    def command(self):
        self.player.feed(calories=60, daze_time=1)


class Bathe(Action):
    def __init__(self, player):
        Action.__init__(self, "Bathe", player)

    def command(self):
        self.player.bathe(duration=2, effect=80)


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
                Bathe(player)
            ]
        ]
