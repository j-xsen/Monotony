from direct.showbase.DirectObject import DirectObject

from objects.notifier import Notifier
from objects.ui.actionbar import ActionBar

HOME_SETUP = -1
HOME = 0
WORK = 1


class Location(Notifier, DirectObject):
    def __init__(self, action_bar: ActionBar, name: str):
        """
        Abstract Location object that holds the actions available and current stage.
        :param action_bar: The Action Bar
        :type action_bar: ActionBar
        :param name: Name for Notifier
        :type name: str
        """
        Notifier.__init__(self, name)
        self.name = name
        self.action_bar = action_bar

        # Each list within self.actions is a different stage
        self.actions = []  # list of lists
        self.stage = 0  # starting stage is 0

        self.accept("set_stage", self.set_stage)

    def set_stage(self, stage: int):
        """
        Sets the stage of the Location.
        :param stage: Stage to go to
        :type stage: int
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
        DirectObject.__init__(self)
        self.action_bar = ActionBar()
        self.location_dict = {
            HOME: self.Home,
            WORK: self.Work
        }
        self.location = self.location_dict[HOME](self.action_bar) # Set location to Home
        messenger.send("set_stage", [HOME_SETUP])  # Set the initial stage to HOME_SETUP (Gives message)
        self.accept("head_to_location", self.head_to_location)

    def head_to_location(self, index: int, stage: int = 0) -> bool:
        """
        Switches the location
        :param index: Index of location to switch to
        :type index: int
        :param stage: Stage to start in (default: 0)
        :type stage: int
        :return: If successful
        :rtype: bool
        """
        self.location.destroy()
        if index in self.location_dict:
            self.location = self.location_dict[index](self.action_bar)
        else:
            return False

        messenger.send("set_stage", [stage])

        return True

    def destroy(self):
        self.ignore_all()
