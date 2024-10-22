from objects.notifier import Notifier


BED = 0
HOME = 1


class Location(Notifier):
    def __init__(self, player):
        """
        Abstract Location object that holds the Player object, action bar, self portrait, actions
        and inner stage
        @param player: Player object
        """
        Notifier.__init__(self, "location")
        self.player = player
        self.action_bar = player.action_bar
        self.self_portrait = player.self_portrait

        # Each list within self.actions is a different stage
        self.actions = []  # list of lists
        self.stage = 0  # starting stage is 0

    def set_stage(self, stage):
        """
        Sets the inner stage [available actions] of the Location
        @param stage: Stage
        """
        if stage < len(self.actions):
            self.notify.debug(f"[set_stage] Setting stage to {stage}")
            self.stage = stage
            self.action_bar.set_actions(self.actions[self.stage])
        else:
            self.notify.warning(f"[set_stage] Cannot set stage to {stage} (Out of index).")
