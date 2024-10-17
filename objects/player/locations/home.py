from objects.player.locations.actions.home import WakeUp, Eat
from objects.player.locations.location import Location
from objects.notifier import Notifier


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
                Eat(player)
            ]
        ]
