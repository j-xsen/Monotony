from locations.location import Location
from objects.notifier import Notifier
from locations.actions.bed import *


class Bed(Location, Notifier):
    def __init__(self, action_bar):
        Location.__init__(self, action_bar)
        Notifier.__init__(self, "bed")
        self.notify.debug("[__init__] Creating Bed location")

        self.actions = [
            [
                WakeUp(self)
            ]
        ]

    def head_to(self):
        self.notify.debug("[head_to] Heading to Bed")
        self.set_stage(0)
