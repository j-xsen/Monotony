from locations.location import Location
from objects.notifier import Notifier


class Bed(Location, Notifier):
    def __init__(self, action_bar):
        Location.__init__(self, action_bar)
        Notifier.__init__(self, "bed")
        self.notify.debug("Creating Bed location")

    def head_to(self):
        self.notify.debug("Heading to Bed")
