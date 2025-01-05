from direct.showbase.DirectObject import DirectObject

from objects.notifier import Notifier
from objects.ui.action_bar import ActionBar

HOME = 0
WORK = 1


class Location(Notifier, DirectObject):
    def __init__(self):
        """
        Abstract Location object that holds the Player object, action bar, self portrait, actions
        and inner stage
        @param player: Player object
        """
        Notifier.__init__(self, "location")

        # Each list within self.actions is a different stage
        self.actions = []  # list of lists
        self.stage = 0  # starting stage is 0

        self.accept("set_stage", self.set_stage)

    def set_stage(self, stage):
        """
        Sets the inner stage [available actions] of the Location
        @param stage: Stage
        """
        if stage < len(self.actions):
            self.notify.debug(f"[set_stage] Setting stage to {stage}")
            self.stage = stage
            messenger.send("set_actions", [self.actions[stage]])
        else:
            self.notify.warning(f"[set_stage] Cannot set stage to {stage} (Out of index).")

    def destroy(self):
        self.ignore_all()


class LocationHandler(DirectObject):
    from objects.locations.home import Home
    from objects.locations.work import Work
    def __init__(self):
        self.action_bar = ActionBar()
        self.location_dict = {
            HOME: self.Home(),
            WORK: self.Work
        }
        self.location = self.location_dict[HOME]
        messenger.send("set_stage", [0])
        self.accept("head_to_location", self.head_to_location)

    def add_location(self, index, location):
        self.location_dict[index] = location

    def head_to_location(self, index, stage=0):
        if index in self.location_dict:
            self.location = self.location_dict[index]
        else:
            return False

        messenger.send("set_stage", [stage])

        return True

    def destroy(self):
        self.ignore_all()
