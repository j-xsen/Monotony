from objects.notifier import Notifier


class Location(Notifier):
    def __init__(self, action_bar):
        Notifier.__init__(self, "location")
        self.action_bar = action_bar
        self.actions = []  # list of lists
        self.stage = 0  # starting stage is 0

    def head_to(self):
        self.notify.warning("[head_to] NO head_to FOR LOCATION")
        self.set_stage(0)

    def set_stage(self, stage):
        if stage < len(self.actions):
            self.notify.debug(f"[set_stage] Setting stage to {stage}")
            self.stage = stage
            self.action_bar.set_actions(self.actions[self.stage])
        else:
            self.notify.warning(f"[set_stage] Cannot set stage to {stage} (Out of index).")
