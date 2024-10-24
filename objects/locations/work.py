from objects.locations.location import Location
from objects.notifier import Notifier
from objects.ui.selfportrait import DRIVING


class Work(Location, Notifier):
    def __init__(self, player):
        super().__init__(player)
        self.notify.debug("[__init__] Creating Work location")
        self.player.self_portrait.update_state(DRIVING)
        self.actions = [
            [

            ]
        ]
